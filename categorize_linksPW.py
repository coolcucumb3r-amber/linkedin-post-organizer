import pandas as pd
from playwright.sync_api import sync_playwright
import time

# Load working links
df = pd.read_excel('working_links.xlsx')
links = df['Working Links'].tolist()

# Define categories
categories = {
    "Programming Roadmaps and Learning": ["python", "roadmap", "learn", "tutorial"],
    "Coding/Tech Projects": ["project", "portfolio", "build", "github"],
    "Job Search": ["job", "career", "resume", "interview", "linkedin"],
    "AI/ML": ["ai", "ml", "artificial intelligence", "machine learning"],
}

# Garbage cleanup list
garbage_phrases = [
    "Sign in to view more", "Sign in to see more", "Join now to see more",
    "We use cookies", "Accept cookies", "Reject all",
    "By using this site you agree to our"
]

# Scrape and categorize one link
def scrape_and_categorize(page, url):
    try:
        page.goto(url, timeout=15000)
        time.sleep(3)  # Let JS load
        text = page.inner_text("body")

        # Clean garbage
        for phrase in garbage_phrases:
            text = text.replace(phrase, "")
        text = text.lower()

        # Categorize
        found_category = "Uncategorized"
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword.lower() in text:
                    found_category = category
                    break
            if found_category != "Uncategorized":
                break

        return (url, found_category)
    except Exception as e:
        print(f"⚠️ Error scraping {url}: {e}")
        return (url, "Uncategorized")

# Run scraping in batches using Playwright
def run_in_batches(links, batch_size=10):
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for i in range(0, len(links), batch_size):
            batch = links[i:i + batch_size]
            context = browser.new_context()
            page = context.new_page()

            for url in batch:
                result = scrape_and_categorize(page, url)
                results.append(result)

            context.close()
        browser.close()
    return results

# Run it
categorized_data = run_in_batches(links, batch_size=10)

# Save results
output_df = pd.DataFrame(categorized_data, columns=["Link", "Category"])
output_df.to_excel("categorized_links_playwright.xlsx", index=False)

print("✅ Scraping & categorization complete (Playwright-based)")
