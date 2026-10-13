"""Headless public acceptance with real CSV downloads and local inference parity."""
import argparse
import hashlib
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from playwright.sync_api import sync_playwright
from predicta.core import predict_assets, assign_priority

ROOT = Path(__file__).resolve().parents[1]
TABS = ['Overview', 'Sensor Explorer', 'RUL Prediction', 'Maintenance Planner',
        'Sensitivity Lab', 'Model Diagnostics', 'Data Contract']
HEADINGS = [None, 'Historical sensor behavior', 'Remaining useful life estimates',
            'Maintenance decision support', 'Controlled model sensitivity',
            'Model validation and interpretability', None]
FORBIDDEN = re.compile(r'\b(cv|curriculum vitae|resume|recruiter|interview|portfolio|hire me|hiring manager)\b', re.I)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('--output', default='docs/audit/2026-10-13/live')
    args = parser.parse_args()
    out = ROOT / args.output
    out.mkdir(parents=True, exist_ok=True)
    report = {'url': args.url, 'started_utc': datetime.now(timezone.utc).isoformat(),
              'headless': True, 'checks': [], 'console_errors': [], 'page_errors': []}
    sample = ROOT / 'data/sample/engine_history.csv'
    data = pd.read_csv(sample)
    bundle = joblib.load(ROOT / 'artifacts/predicta_fd001_model.joblib')
    report['trusted_model_name'] = bundle.get('model_name')
    report['model_sha256'] = hashlib.sha256((ROOT / 'artifacts/predicta_fd001_model.joblib').read_bytes()).hexdigest()

    def check(name, action):
        try:
            detail = action()
            report['checks'].append({'name': name, 'status': 'PASS', 'detail': detail})
            print('PASS:', name, flush=True)
        except Exception as exc:
            report['checks'].append({'name': name, 'status': 'FAIL', 'detail': str(exc)})
            print('FAIL:', name, str(exc)[:350], flush=True)

    def require(condition, message):
        if not condition:
            raise AssertionError(message)

    def app_frame(page):
        deadline = time.monotonic() + 90
        while time.monotonic() < deadline:
            for frame in page.frames:
                if frame.get_by_role('heading', name='PREDICTA AI', exact=True).count():
                    frame.get_by_role('tab', name='Overview', exact=True).wait_for(timeout=90000)
                    frame.get_by_role('button', name='Stop', exact=True).wait_for(state='hidden', timeout=90000)
                    return frame
            page.wait_for_timeout(500)
        raise AssertionError('PREDICTA heading/tabs not rendered; final URL: ' + page.url)

    def healthy(frame):
        frame.get_by_role('button', name='Stop', exact=True).wait_for(state='hidden', timeout=90000)
        require(frame.locator('[data-testid="stException"]').count() == 0, 'Streamlit exception')
        require('Input failed data-contract validation' not in frame.locator('body').inner_text(), 'Unexpected contract error')
        selected = frame.get_by_role('tab', selected=True).inner_text().strip()
        if selected in ['Overview', 'Sensor Explorer', 'RUL Prediction', 'Maintenance Planner', 'Model Diagnostics']:
            panel = frame.get_by_role('tabpanel', name=selected, exact=True)
            panel.locator('[data-testid="stPlotlyChart"]').first.scroll_into_view_if_needed(timeout=30000)
            panel.locator('.js-plotly-plot .main-svg').first.wait_for(state='visible', timeout=90000)

    def copy_check(frame):
        text = frame.locator('body').inner_text()
        require(not FORBIDDEN.search(text), 'Forbidden public copy: ' + str(FORBIDDEN.findall(text)))
        return {'characters_scanned': len(text)}

    def download(page, frame, label, filename):
        with page.expect_download(timeout=30000) as event:
            frame.get_by_role('button', name=label, exact=True).click()
        event.value.save_as(out / filename)
        require(event.value.failure() is None, 'Download failed')
        return out / filename

    def parity(path, source, planner=False):
        got = pd.read_csv(path).sort_values('engine_id').reset_index(drop=True)
        expected, _ = predict_assets(source, bundle)
        if planner:
            expected = assign_priority(expected, critical=30, watch=60)
        expected = expected.sort_values('engine_id').reset_index(drop=True)
        require(len(got) == len(expected), 'Unexpected engine count')
        for col in ['engine_id', 'cycle', 'rul_estimate', 'rul_lower', 'rul_upper']:
            np.testing.assert_allclose(got[col], expected[col], rtol=1e-8, atol=1e-8)
        require(np.isfinite(got[['rul_estimate', 'rul_lower', 'rul_upper']]).all().all(), 'Nonfinite inference')
        if planner:
            require(got.priority.tolist() == expected.priority.tolist(), 'Planner priority mismatch')
        return {'rows': len(got), 'columns': list(got.columns), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'local_model_parity': True}

    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 850}, accept_downloads=True)
        page = context.new_page()
        page.on('console', lambda msg: report['console_errors'].append({'text':msg.text, 'location':msg.location}) if msg.type == 'error' else None)
        page.on('pageerror', lambda err: report['page_errors'].append(str(err)))
        try:
            response = page.goto(args.url, wait_until='domcontentloaded', timeout=90000)
            frame = app_frame(page)
            report['main_http_status'] = response.status
            report['final_url'] = page.url
            report['app_frame_url'] = frame.url
            check('public availability and Champion identity', lambda: require(response.status == 200 and 'random forest' in frame.locator('body').inner_text().lower(), 'Public HTTP/model identity incorrect'))
            check('public model release identity', lambda: frame.get_by_text('SHA256 ' + report['model_sha256'][:12], exact=True).wait_for(timeout=90000))
            require(frame.get_by_role('tab').count() == 7, 'Expected exactly seven tabs')
            for name, heading in zip(TABS, HEADINGS):
                def navigate(name=name, heading=heading):
                    tab = frame.get_by_role('tab', name=name, exact=True)
                    tab.click()
                    require(tab.get_attribute('aria-selected') == 'true', 'Tab not selected')
                    if heading:
                        frame.get_by_role('heading', name=heading, exact=True).wait_for()
                    healthy(frame)
                    result = copy_check(frame)
                    page.screenshot(path=out / (name.lower().replace(' ', '-') + '-desktop.png'), full_page=True)
                    (out / (name.lower().replace(' ', '-') + '.yaml')).write_text(frame.locator('body').aria_snapshot(), encoding='utf-8')
                    return result
                check('desktop tab: ' + name, navigate)
            def sample_download():
                path = download(page, frame, 'Download example engine history', 'downloaded-engine-history.csv')
                pd.testing.assert_frame_equal(pd.read_csv(path), data)
                require(path.read_text().replace('\r\n','\n') == sample.read_text().replace('\r\n','\n'), 'Example content differs beyond newline normalization')
                return {'rows':len(data), 'sha256':hashlib.sha256(path.read_bytes()).hexdigest(), 'newline_normalized_source_match':True}
            check('example CSV download matches real source', sample_download)
            frame.get_by_role('tab', name='RUL Prediction', exact=True).click()
            check('Champion inference and RUL CSV download', lambda: parity(download(page, frame, 'Export RUL predictions', 'default-rul.csv'), data))
            frame.get_by_role('tab', name='Maintenance Planner', exact=True).click()
            check('maintenance report download and policy parity', lambda: parity(download(page, frame, 'Export prioritized worklist', 'default-worklist.csv'), data, True))
            subset = data[data.engine_id.isin(sorted(data.engine_id.unique())[:2])]
            valid = out / 'valid-real-two-engines.csv'
            subset.to_csv(valid, index=False)
            upload = frame.locator('input[type="file"]')
            def valid_upload():
                upload.set_input_files(valid)
                frame.get_by_text('Uploaded data', exact=True).wait_for(timeout=30000)
                healthy(frame)
                frame.get_by_role('tab', name='RUL Prediction', exact=True).click()
                return parity(download(page, frame, 'Export RUL predictions', 'uploaded-rul.csv'), subset)
            check('valid real CSV upload and changed-input inference', valid_upload)
            invalids = {'missing-columns': pd.DataFrame({'wrong_col':[1]}),
                        'duplicate-cycle': pd.concat([subset, subset.iloc[[0]]], ignore_index=True),
                        'nonfinite-sensor': subset.assign(sensor_1=np.inf)}
            expected_errors = {'missing-columns':'Missing required columns', 'duplicate-cycle':'Duplicate', 'nonfinite-sensor':'non-finite'}
            for label, invalid in invalids.items():
                path = out / ('invalid-' + label + '.csv')
                invalid.to_csv(path, index=False)
                def reject(path=path, label=label):
                    upload.set_input_files(path)
                    frame.get_by_text(re.compile('Input failed data-contract validation: .*' + expected_errors[label], re.I)).wait_for(timeout=30000)
                    require(frame.locator('[data-testid="stException"]').count() == 0, 'Invalid upload crashed app')
                    require(frame.get_by_role('button', name='Export RUL predictions').count() == 0, 'Invalid input retained prediction export')
                    return frame.locator('[data-testid="stAlert"]').all_text_contents()
                check('invalid CSV rejected: ' + label, reject)
            check('recovery after invalid upload', valid_upload)
            frame.get_by_role('tab', name='Overview', exact=True).click()
            def keyboard():
                tab = frame.get_by_role('tab', name='Overview', exact=True)
                tab.focus()
                tab.press('ArrowRight')
                target = frame.get_by_role('tab', name='Sensor Explorer', exact=True)
                require(target.evaluate('(el) => el === document.activeElement'), 'ArrowRight did not focus next tab')
                target.press('Enter')
                require(target.get_attribute('aria-selected') == 'true', 'Keyboard tab activation failed')
            check('keyboard navigation and activation', keyboard)
            mobile_context = browser.new_context(viewport={'width':375,'height':812}, reduced_motion='reduce')
            mobile = mobile_context.new_page()
            mobile.on('pageerror', lambda err: report['page_errors'].append('mobile: ' + str(err)))
            mobile.goto(args.url, wait_until='domcontentloaded', timeout=90000)
            mf = app_frame(mobile)
            for name in TABS:
                def mobile_tab(name=name):
                    mf.get_by_role('tab', name=name, exact=True).click()
                    healthy(mf)
                    copy_check(mf)
                    metrics = mf.evaluate('''() => ({viewport:innerWidth, document:document.documentElement.scrollWidth, background:getComputedStyle(document.querySelector('[data-testid="stAppViewContainer"]')).backgroundImage, color:getComputedStyle(document.querySelector('h1')).color, accent:getComputedStyle(document.querySelector('[role="tab"][aria-selected="true"]')).color, reduced:matchMedia('(prefers-reduced-motion: reduce)').matches})''')
                    require(metrics['document'] <= metrics['viewport'] + 1, 'Mobile document horizontal overflow: ' + str(metrics))
                    require(metrics['color'] == 'rgb(23, 41, 45)' and metrics['accent'] == 'rgb(35, 79, 204)', 'Approved Paper Atlas DESIGN color mismatch: ' + str(metrics))
                    require(metrics['reduced'], 'Reduced motion not active')
                    mobile.screenshot(path=out / (name.lower().replace(' ', '-') + '-mobile.png'), full_page=True)
                    return metrics
                check('mobile 375x812 / design: ' + name, mobile_tab)
            mobile_context.close()
            check('no uncaught JavaScript errors', lambda: require(not report['page_errors'], str(report['page_errors'])))
            known_platform = [e for e in report['console_errors'] if ('heap-' in e['location'].get('url','') or '/api/v2/user/details' in e['location'].get('url',''))]
            report['platform_console_errors'] = known_platform
            app_errors = [e for e in report['console_errors'] if e not in known_platform]
            check('no application console errors (Cloud wrapper errors recorded separately)', lambda: require(not app_errors, str(app_errors)))
        except Exception as exc:
            report['checks'].append({'name':'audit execution', 'status':'FAIL', 'detail':str(exc)})
        finally:
            context.close()
            browser.close()
    report['finished_utc'] = datetime.now(timezone.utc).isoformat()
    report['passed'] = bool(report['checks']) and all(c['status']=='PASS' for c in report['checks'])
    (out / 'report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    print('PUBLIC AUDIT:', 'PASS' if report['passed'] else 'FAIL', flush=True)
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
