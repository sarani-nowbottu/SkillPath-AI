"""
capture_real_screenshots.py - Uses Playwright with local Microsoft Edge
to capture 100% genuine, authentic screenshots of the running Streamlit and web UI.
"""

import time
import os
from playwright.sync_api import sync_playwright

def capture():
    os.makedirs("docs", exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            headless=True
        )
        context = browser.new_context(viewport={"width": 1366, "height": 850})
        page = context.new_page()

        # 1. Capture Streamlit User Input
        print("Navigating to Streamlit at http://localhost:8501 ...")
        page.goto("http://localhost:8501", wait_until="networkidle")
        time.sleep(3) # Ensure full websocket hydration

        page.screenshot(path="docs/streamlit_user_input.png", full_page=False)
        print("Saved docs/streamlit_user_input.png")

        # 2. Click Generate Learning Path Button & Tab 2
        print("Clicking Generate Learning Path ...")
        # Click the button
        generate_btn = page.locator("button:has-text('Generate Learning Path')")
        if generate_btn.count() > 0:
            generate_btn.first.click()
            time.sleep(2)

        # Switch to Generated Roadmap tab
        roadmap_tab = page.locator("text=Generated Learning Roadmap")
        if roadmap_tab.count() > 0:
            roadmap_tab.first.click()
            time.sleep(2)

        page.screenshot(path="docs/streamlit_generated_result.png", full_page=False)
        print("Saved docs/streamlit_generated_result.png")

        browser.close()

if __name__ == "__main__":
    capture()
