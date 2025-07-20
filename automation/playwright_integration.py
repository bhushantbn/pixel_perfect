from compare import compare_images
from playwright.sync_api import sync_playwright

def capture_and_compare():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://example.com")
        page.screenshot(path="tests/test_screenshots/test_image.png")
        browser.close()

    baseline = "tests/test_screenshots/baseline_image.png"
    test = "tests/test_screenshots/test_image.png"
    score, diff_path = compare_images(baseline, test)
    print(f"SSIM Score: {score}")
    print(f"Diff saved at: {diff_path}")