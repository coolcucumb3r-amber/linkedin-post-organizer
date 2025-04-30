import pandas as pd
import asyncio
import aiohttp
#import requests
from bs4 import BeautifulSoup

df = pd.read_excel('working_links.xlsx')
links = df['Working Links'].tolist()

garbage_phrases = [
            "Sign in to view more",
            "Sign in to see more",
            "Join now to see more",
            "We use cookies",
            "Accept cookies",
            "Reject all",
            "By using this site you agree to our"
        ]

# Dictionary to store categorized links
# 2. Define categories
categories = {
    "Programming Roadmaps and Learning": ["python", "roadmap", "learn", "tutorial"],
    "Coding/Tech Projects": ["project", "portfolio", "build", "github"],
    "Job Search": ["job", "career", "resume", "interview", "linkedin"]
}

async def scrape_and_categorize(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            if response.status != 200:
                raise Exception(f"HTTP error {response.status}")
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')


        # Remove unwanted elements
        for tag in soup(["script", "style", "nav", "footer", "noscript", "header", "aside"]):
            tag.decompose()  # Completely remove the tag and its content

       # Step 2: Try to scrape just the <main> content
        main_section = soup.find("main")
        if main_section:
            text = main_section.get_text(separator=' ', strip=True)
        else:
            text = soup.get_text(separator=' ', strip=True)

        # Step 3: Remove duplicate or useless text (optional filtering)
       
        for phrase in garbage_phrases:
            if phrase in text:
                text = text.replace(phrase, "")

        # Normalize text for matching
            text = text.lower()

        #Step 4: Categorize the link
        found_category = "Uncategorized"  # Default value

        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in text:
                    found_category = category #I don't understand
                    break
            if found_category != "Uncategorized":
                break
        return (url, found_category)
        
    except Exception as e:
        print(f"⚠️ Error scraping {url}: {e}")
        return (url, "Uncategorized")


#<----
async def main():
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in links:
            task = scrape_and_categorize(session, url)
            tasks.append(task)
        results = await asyncio.gather(*tasks)
    return results

# Run and get categorized results
categorized_data = asyncio.run(main())

# Create DataFrame
df = pd.DataFrame(categorized_data, columns=["Link", "Category"])

# Save to Excel
df.to_excel('categorized_links.xlsx', index=True)

print("✅ Categorized links saved to categorized_links.xlsx")

