import pandas as pd
from playwright.sync_api import sync_playwright
from tqdm import tqdm
import time

# Load links
df = pd.read_excel('working_links.xlsx')
links = df['Working Links'].tolist()

# Categories
categories = {
    "Programming Roadmaps and Learning": ["python", "roadmap", "learn", "tutorial"],
    "Coding/Tech Projects": ["project", "portfolio", "build", "github"],
    "Job Search": ["job", "career", "resume", "interview", "linkedin"],
    "AI/ML": ["ai", "ml", "artificial intelligence", "machine learning"],
}

# Garbage phrases to clean
garbage_phrases = [
    "Sign in to view more", "Sign in to see more", "Join now to see more",
    "We use cookies", "Accept cookies", "Reject all",
    "By using this site you agree to our"
]

# Track failed links
failed_links = []

def scrape_and_categorize(page, url):
    try:
        page.goto(url, timeout=15000)
        time.sleep(3)  # Optional: wait for JS

        # You can fine-tune this selector if needed
        text = page.inner_text("body")

        # Remove junk
        for phrase in garbage_phrases:
            text = text.replace(phrase, "")
        text = text.lower()

        # Categorization
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
        failed_links.append(url)
        return (url, "Uncategorized")

def run_in_batches(links, batch_size=10):
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # Loop through links in chunks, show progress bar
        for i in tqdm(range(0, len(links), batch_size), desc="🔍 Scraping LinkedIn"):
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

# Save to Excel
df = pd.DataFrame(categorized_data, columns=["Link", "Category"])
df.to_excel("categorized_links_playwright.xlsx", index=True)

# Save failed links
if failed_links:
    fail_df = pd.DataFrame({"Failed Links": failed_links})
    fail_df.to_excel("failed_links.xlsx", index=True)
    print(f"⚠️ {len(failed_links)} links failed. Saved to failed_links.xlsx")

print("✅ Scraping & categorization complete.")
