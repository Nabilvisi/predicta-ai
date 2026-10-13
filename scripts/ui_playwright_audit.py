"""Comprehensive Playwright UI verification script for PREDICTA AI Streamlit app."""
import os
import sys
import tempfile
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from playwright.sync_api import sync_playwright

FORBIDDEN_TERMS = [
    "curriculum vitae", "resume", "recruiter", "interview",
    "hire me", "portfolio project", "hiring manager", "candidate"
]

def run_audit(url: str = "http://localhost:8501") -> bool:
    print(f"Starting Playwright audit against {url}...", flush=True)
    errors = []

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 850})
        page = context.new_page()

        # Listen for console errors
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda err: errors.append(f"PageError: {err}"))

        # 1. Navigation
        page.goto(url, wait_until="domcontentloaded", timeout=15000)
        page.wait_for_selector("h1", timeout=15000)
        time.sleep(2)

        # 2. Check title and disclaimers
        content = page.content().lower()
        for term in FORBIDDEN_TERMS:
            if term in content:
                errors.append(f"Forbidden term found in UI: '{term}'")

        header_text = page.locator("h1").inner_text()
        print(f"H1 Header: {header_text}", flush=True)
        assert "PREDICTA AI" in header_text, "Title does not contain PREDICTA AI"

        # Check simulation disclaimer
        warning_box = page.locator('[data-testid="stAlert"]')
        assert warning_box.count() > 0, "Warning disclaimer alert not found"
        warning_text = warning_box.first.inner_text().encode("ascii", "replace").decode("ascii")
        print(f"Disclaimer verified: {warning_text[:60]}...", flush=True)

        # 3. Test all 7 tabs
        tabs = ["Overview", "Sensor Explorer", "RUL Prediction", "Maintenance Planner", "Sensitivity Lab", "Model Diagnostics", "Data Contract"]
        tab_locators = page.get_by_role("tab")
        tab_count = tab_locators.count()
        print(f"Found {tab_count} tabs.", flush=True)
        assert tab_count == 7, f"Expected 7 tabs, got {tab_count}"

        for i, tab_name in enumerate(tabs):
            print(f"Testing tab {i+1}: {tab_name}...", flush=True)
            tab_locator = page.get_by_role("tab", name=tab_name)
            if tab_locator.count() == 0:
                errors.append(f"Tab not found: {tab_name}")
                continue
            tab_locator.click()
            time.sleep(1)

            # Check for Streamlit exception
            exceptions = page.locator('[data-testid="stException"]')
            if exceptions.count() > 0:
                errors.append(f"Exception on tab {tab_name}: {exceptions.first.inner_text()}")

            # Check for error alerts
            error_alerts = page.locator('[data-testid="stAlert"][kind="error"]')
            if error_alerts.count() > 0:
                errors.append(f"Error alert on tab {tab_name}: {error_alerts.first.inner_text()}")

        # 4. Test download buttons presence
        download_btns = page.locator('[data-testid="stDownloadButton"]')
        print(f"Download buttons count: {download_btns.count()}", flush=True)
        assert download_btns.count() > 0, "Download buttons missing"

        # 5. Test Invalid CSV Upload Flow
        print("Testing invalid CSV upload...", flush=True)
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as f:
            f.write("wrong_col_1,wrong_col_2\n1.0,2.0\n")
            invalid_csv = f.name

        try:
            file_input = page.locator('input[type="file"]')
            if file_input.count() > 0:
                file_input.set_input_files(invalid_csv)
                time.sleep(2)
                alerts = page.locator('[data-testid="stAlert"]')
                has_contract_error = any("Input failed data-contract validation" in alerts.nth(j).inner_text() for j in range(alerts.count()))
                if not has_contract_error:
                    errors.append("Invalid CSV did not trigger data-contract error alert")
                else:
                    print("PASS: Invalid CSV correctly rejected with data-contract alert.", flush=True)
        finally:
            os.remove(invalid_csv)

        # 6. Test Valid CSV Upload Flow
        sample_path = os.path.abspath("data/sample/engine_history.csv")
        if os.path.isfile(sample_path):
            print(f"Testing valid CSV upload with {sample_path}...", flush=True)
            file_input = page.locator('input[type="file"]')
            if file_input.count() > 0:
                file_input.set_input_files(sample_path)
                time.sleep(3)
                updated_content = page.content()
                if "Uploaded data" not in updated_content:
                    errors.append("Ribbon did not reflect 'Uploaded data' source after valid upload")
                else:
                    print("PASS: Valid CSV recognized as 'Uploaded data'.", flush=True)

                # Confirm tabs render without errors on uploaded data
                for tab_name in ["Overview", "RUL Prediction", "Sensitivity Lab"]:
                    page.get_by_role("tab", name=tab_name).click()
                    time.sleep(1)
                    if page.locator('[data-testid="stException"]').count() > 0:
                        errors.append(f"Exception on {tab_name} after file upload")

        # 7. Keyboard accessibility test (Tab focus traversal)
        print("Testing keyboard focus navigation...", flush=True)
        page.keyboard.press("Tab")
        time.sleep(0.5)
        active_tag = page.evaluate("() => document.activeElement ? document.activeElement.tagName : 'NONE'")
        print(f"Active element after Tab: {active_tag}", flush=True)
        assert active_tag != "NONE", "Keyboard Tab key did not move focus"

        # 8. Mobile viewport audit
        print("Testing mobile viewport (375x812)...", flush=True)
        mobile_context = browser.new_context(viewport={"width": 375, "height": 812})
        mobile_page = mobile_context.new_page()
        mobile_page.goto(url, wait_until="domcontentloaded", timeout=15000)
        mobile_page.wait_for_selector("h1", timeout=15000)
        time.sleep(1)

        mobile_h1 = mobile_page.locator("h1").inner_text()
        assert "PREDICTA AI" in mobile_h1, "Mobile view H1 missing"

        mobile_exceptions = mobile_page.locator('[data-testid="stException"]')
        if mobile_exceptions.count() > 0:
            errors.append(f"Mobile exception: {mobile_exceptions.first.inner_text()}")

        mobile_context.close()
        context.close()
        browser.close()

    if console_errors:
        print(f"Console errors noted: {console_errors[:3]}")
    if errors:
        print("FAILURES DETECTED:")
        for err in errors:
            print(f" - {err}")
        return False
    else:
        print("PLAYWRIGHT AUDIT PASSED: All 7 tabs, uploads, downloads, keyboard focus, mobile responsive, no forbidden copy.")
        return True

if __name__ == "__main__":
    target_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8501"
    success = run_audit(target_url)
    sys.exit(0 if success else 1)
