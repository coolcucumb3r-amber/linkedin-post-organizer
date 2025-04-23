import pandas as pd
import aiohttp
import asyncio

# Read the CSV file
df = pd.read_csv('Saved_Items.csv')
links = df['savedItem'].tolist()  # List of links to check
valid_links = []  # To store valid links

# Asynchronous function to check a single link
async def check_link(session, url):
    try:
        # Asynchronously send a HEAD request
        async with session.head(url, allow_redirects=True, timeout=5) as response:
            if response.status == 200:
                valid_links.append(url)  # Add valid link to the list
            else:
                print(f"❌ Broken link: {url} (Status: {response.status})")
    except Exception as e:
        print(f"⚠️ Error checking link: {url} - {e}")

# Main coroutine to manage the session and tasks
async def main():
    async with aiohttp.ClientSession() as session:  # Create an async HTTP session
        # Create a list of tasks for all links
        tasks = [check_link(session, url) for url in links]
        await asyncio.gather(*tasks)  # Run all tasks concurrently

# Run the main coroutine
asyncio.run(main())

# Save the valid links to a new Excel file
new_df = pd.DataFrame({'Working Links': valid_links})
new_df.to_excel('working_links.xlsx', index=True)

print("✅ Valid links saved to working_links.xlsx")