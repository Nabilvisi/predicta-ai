"""Capture screenshots of all 7 tabs for visual QA."""
import time
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 850})
        page = context.new_page()
        page.goto("http://localhost:8501", wait_until="domcontentloaded")
        page.wait_for_selector("h1")
        time.sleep(2)
        
        tabs = ["Overview", "Sensor Explorer", "RUL Prediction", "Maintenance Planner", "Sensitivity Lab", "Model Diagnostics", "Data Contract"]
        for i, tab_name in enumerate(tabs):
            tab_locator = page.get_by_role("tab", name=tab_name)
            tab_locator.click()
            time.sleep(1.5)
            filename = f"docs/tab_{i}_{tab_name.lower().replace(' ', '_')}.png"
            page.screenshot(path=filename)
            print(f"Captured {filename}")
            
        browser.close()

if __name__ == "__main__":
    main()
