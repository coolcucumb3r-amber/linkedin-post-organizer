# LinkedIn Saved Posts Organizer
**In Progress** 

This project is a Python-based tool designed to help you organize your LinkedIn saved posts into categories. Currently, it processes a CSV file of saved LinkedIn posts, checks the validity of the links, and outputs a list of working links in an Excel file. More features to be added soon.

## Features
- **Asynchronous Link Validation:** Uses `aiohttp` and `asyncio` to check the validity of saved LinkedIn post links concurrently, making the process faster.
- **Output to Excel:** Saves the list of valid links to an Excel file for easy access and organization.


## How It Works
1. The tool reads a CSV file (`Saved_Items.csv`) containing LinkedIn saved post links, that can be downloaded from your LinkedIn profile
2. It validates each link asynchronously to ensure it is still accessible.
3. Valid links are saved to an Excel file (`working_links.xlsx`).

## Future 
1. The tool will allow you to categorize your saved posts, in pre-built categories, and user-created categories 
2. The tool will connect to your LinkedIn account to allow you to create categories when you're saving posts
3. The tool will have a graphical interface to be more user-friendly 


## Prerequisites
- Python 3.8 or higher
- Required Python libraries:
  - `pandas`
  - `aiohttp`
  - `asyncio`
- A CSV file named `Saved_Items.csv` with a column named `savedItem` containing the LinkedIn post links.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/linkedin-saved-posts-organizer.git
   cd linkedin-saved-posts-organizer