from playwright.sync_api import sync_playwright

def get_linkedin_post_text(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=20000)

        # Optional: wait for post text to appear (can be improved later)
        page.wait_for_timeout(5000)

        # Get all visible text (not perfect but works for now)
        text = page.inner_text("body")

        browser.close()
        return text

# Example
print(get_linkedin_post_text("https://www.linkedin.com/feed/update/urn:li:activity:7254461502756151299/"))
