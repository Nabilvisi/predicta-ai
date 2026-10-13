"""Rendered 3D lifecycle and accessibility checks against an actual Streamlit URL."""
import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    out = ROOT / args.output
    out.mkdir(parents=True, exist_ok=True)
    report = {'url': args.url, 'headless': True, 'started_utc': datetime.now(timezone.utc).isoformat(), 'checks': [], 'page_errors': []}

    def require(ok, message):
        if not ok:
            raise AssertionError(message)

    def check(name, action):
        try:
            detail = action()
            report['checks'].append({'name': name, 'status': 'PASS', 'detail': detail})
            print('PASS:', name, flush=True)
        except Exception as exc:
            report['checks'].append({'name': name, 'status': 'FAIL', 'detail': str(exc)})
            print('FAIL:', name, str(exc)[:250], flush=True)

    def frames(page):
        deadline = time.monotonic() + 90
        while time.monotonic() < deadline:
            app = next((f for f in page.frames if f.get_by_role('heading', name='PREDICTA AI', exact=True).count()), None)
            scene = next((f for f in page.frames if f.locator('.scene').count()), None)
            if app and scene:
                app.get_by_role('button', name='Stop', exact=True).wait_for(state='hidden', timeout=90000)
                scene.locator('.scene').wait_for()
                return app, scene
            page.wait_for_timeout(250)
        raise AssertionError('App and illustration did not render')

    def state(scene):
        return scene.locator('.scene').evaluate('(el) => ({...el.dataset})')

    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        context = browser.new_context(viewport={'width':1440, 'height':950})
        page = context.new_page()
        page.on('pageerror', lambda e: report['page_errors'].append(str(e)))
        try:
            page.goto(args.url, wait_until='domcontentloaded', timeout=90000)
            app, scene = frames(page)
            scene.locator('.scene[data-animation="paused"]').wait_for(timeout=15000)
            check('real WebGL geometry rendered', lambda: require(state(scene)['renderer'] == 'webgl', 'No WebGL rendering'))
            scene.locator('#engine').screenshot(path=out / 'turbine-canvas.png')
            page.screenshot(path=out / 'overview-desktop.png')

            def rotate_pause():
                initial = int(state(scene)['frames'])
                scene.get_by_role('button', name='Rotate', exact=True).click()
                page.wait_for_timeout(450)
                running = int(state(scene)['frames'])
                require(running > initial + 3, 'Rotation did not render frames')
                scene.get_by_role('button', name='Pause', exact=True).click()
                stopped = int(state(scene)['frames'])
                page.wait_for_timeout(450)
                require(int(state(scene)['frames']) == stopped, 'Paused graphic still renders')
                return {'initial_frames':initial, 'rotating_frames':running, 'paused_frames':stopped}
            check('rotation works and pause stops the frame loop', rotate_pause)

            def explode():
                scene.get_by_role('button', name='Explode', exact=True).click()
                scene.locator('.scene[data-spread="1.000"]').wait_for(timeout=10000)
                page.screenshot(path=out / 'overview-exploded-desktop.png')
                scene.get_by_role('button', name='Assemble', exact=True).click()
                scene.locator('.scene[data-spread="0.000"]').wait_for(timeout=10000)
                return {'exploded_spread':1, 'assembled_spread':0}
            check('animated explode and assemble complete', explode)

            def keyboard():
                before = float(state(scene)['yaw'])
                scene.locator('#engine').focus()
                scene.locator('#engine').press('ArrowRight')
                after = float(state(scene)['yaw'])
                require(after > before, 'Keyboard did not rotate the view')
                focus = scene.locator('#engine').evaluate('(el) => getComputedStyle(el).outlineStyle')
                require(focus == 'solid', 'Keyboard focus ring missing')
                scene.get_by_role('button', name='Turn turbine left').click()
                require(abs(float(state(scene)['yaw']) - before) < .002, 'Tap alternative did not reverse turn')
                return {'yaw_before':before, 'yaw_after':after, 'focus_outline':focus}
            check('keyboard, focus and tap alternatives', keyboard)

            def hidden():
                scene.get_by_role('button', name='Rotate', exact=True).click()
                app.get_by_role('tab', name='Sensor Explorer', exact=True).click()
                page.wait_for_timeout(600)
                before = int(state(scene)['frames'])
                page.wait_for_timeout(450)
                require(int(state(scene)['frames']) == before, 'Hidden graphic keeps rendering')
                app.get_by_role('tab', name='Overview', exact=True).click()
                scene.locator('#engine').scroll_into_view_if_needed()
                page.wait_for_timeout(350)
                require(int(state(scene)['frames']) > before, 'Visible rotation did not resume')
                scene.get_by_role('button', name='Pause', exact=True).click()
            check('offscreen loop pauses and resumes on return', hidden)

            def context_recovery():
                supported = scene.locator('#engine').evaluate("el => !!el.getContext('webgl').getExtension('WEBGL_lose_context')")
                require(supported, 'Context-loss test extension unavailable')
                scene.locator('#engine').evaluate("el => { window.auditLossExtension=el.getContext('webgl').getExtension('WEBGL_lose_context'); window.auditLossExtension.loseContext(); }")
                scene.locator('.fallback.visible').wait_for()
                require(state(scene)['renderer'] == 'fallback', 'Fallback not enabled')
                page.wait_for_timeout(300)
                scene.evaluate("() => window.auditLossExtension.restoreContext()")
                scene.locator('.scene[data-renderer="webgl"]').wait_for(timeout=15000)
                require(not scene.get_by_role('button', name='Rotate', exact=True).is_disabled(), 'Restored controls disabled')
                return {'fallback_visible':True, 'restored_renderer':'webgl'}
            check('WebGL context loss has static fallback and recovers', context_recovery)

            def fonts():
                app.evaluate('() => document.fonts.ready')
                loaded = app.evaluate('() => [...document.fonts].map(f => ({family:f.family,status:f.status}))')
                require(any(f['family'] == 'Instrument Serif' and f['status']=='loaded' for f in loaded), 'Display font not loaded')
                require(any(f['family'] == 'IBM Plex Sans' and f['status']=='loaded' for f in loaded), 'UI font not loaded')
                return loaded
            check('local licensed fonts load without a runtime CDN', fonts)

            mobile_context = browser.new_context(viewport={'width':375,'height':812}, reduced_motion='reduce')
            mobile = mobile_context.new_page()
            mobile.on('pageerror', lambda e: report['page_errors'].append('mobile: ' + str(e)))
            mobile.goto(args.url, wait_until='domcontentloaded', timeout=90000)
            mobile_app, mobile_scene = frames(mobile)

            def reduced():
                require(state(mobile_scene)['renderer']=='webgl', 'Mobile WebGL missing')
                require(mobile_scene.get_by_role('button', name='Rotate', exact=True).is_disabled(), 'Reduced-motion rotation enabled')
                mobile_scene.locator('#engine').scroll_into_view_if_needed()
                mobile.wait_for_timeout(250)
                before = int(state(mobile_scene)['frames'])
                mobile.wait_for_timeout(450)
                require(int(state(mobile_scene)['frames']) == before, 'Reduced-motion autoplay detected')
                mobile_scene.get_by_role('button', name='Explode', exact=True).click()
                require(state(mobile_scene)['spread']=='1.000', 'Reduced-motion explode not immediate')
                mobile_scene.get_by_role('button', name='Assemble', exact=True).click()
                require(state(mobile_scene)['spread']=='0.000', 'Reduced-motion assemble not immediate')
                return {'automatic_frames_during_idle':0, 'transitions':'immediate'}
            check('mobile reduced motion disables autoplay and transitions', reduced)

            def mobile_layout():
                mobile_scene.locator('#engine').scroll_into_view_if_needed()
                metrics = mobile_scene.evaluate('() => ({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,dpr:devicePixelRatio,canvasWidth:document.querySelector("canvas").width,canvasCSSWidth:document.querySelector("canvas").clientWidth})')
                require(metrics['scrollWidth'] <= metrics['width'], '3D iframe horizontal overflow')
                require(metrics['canvasWidth'] <= metrics['canvasCSSWidth']*1.5+1, 'Unbounded rendering pixel ratio')
                for name in ['Turn turbine left','Turn turbine right','Rotate','Explode']:
                    box = mobile_scene.get_by_role('button', name=name, exact=True).bounding_box()
                    require(box['x'] >= 0 and box['x']+box['width'] <= 375 and box['height'] >= 40, 'Control outside viewport or too short')
                mobile.screenshot(path=out / 'overview-3d-mobile.png')
                return metrics
            check('375x812 3D layout, touch controls and bounded resolution', mobile_layout)
            mobile_context.close()

            fallback_context = browser.new_context(viewport={'width':1280,'height':850})
            fallback_context.add_init_script("const original=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(type,...args){return type==='webgl'?null:original.call(this,type,...args)};")
            fallback_page = fallback_context.new_page()
            fallback_page.goto(args.url, wait_until='domcontentloaded', timeout=90000)
            _, fallback_scene = frames(fallback_page)
            check('WebGL unavailable shows accessible static illustration', lambda: require(state(fallback_scene)['renderer']=='fallback' and fallback_scene.locator('.fallback.visible').is_visible(), 'Missing static fallback'))
            fallback_page.screenshot(path=out / 'overview-static-fallback.png')
            fallback_context.close()
            check('no uncaught illustration JavaScript errors', lambda: require(not report['page_errors'], str(report['page_errors'])))
        except Exception as exc:
            report['checks'].append({'name':'audit execution', 'status':'FAIL', 'detail':str(exc)})
        finally:
            context.close()
            browser.close()
    report['passed'] = bool(report['checks']) and all(c['status']=='PASS' for c in report['checks'])
    report['finished_utc'] = datetime.now(timezone.utc).isoformat()
    (out / 'motion-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('MOTION AUDIT:', 'PASS' if report['passed'] else 'FAIL', flush=True)
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
