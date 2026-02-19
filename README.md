# El País Web Automation with Selenium & BrowserStack

This project demonstrates web scraping, API integration, text processing, and cross-browser parallel execution using Selenium and BrowserStack.

## Problem Statement

The script performs the following tasks:

1. Opens El País (Spanish news website)
2. Ensures content is displayed in Spanish
3. Navigates to the Opinion section
4. Scrapes first 5 articles:
   - Title (Spanish)
   - Content (Spanish)
   - Cover image (if available)
5. Translates article titles to English using Rapid Translate API(Rapid Translate API has a limited of 50 request per day.)
6. Finds repeated words across translated titles
7. Executes the same test in parallel across multiple browsers/devices using BrowserStack

## Tech Stack

- Python 3
- Selenium WebDriver
- BrowserStack Cloud Grid
- Rapid Translate Multi Traduction API
- Requests
- WebDriver Manager

## Project Structure
browserstack-el-pais/
├── main.py
├── browserstack_parallel.py
├── requirements.txt
├── README.md
└── images/

## Setup Instructions (Local Run)

1. Clone the repository  
inside bash
- git clone https://github.com/TanishaMaji/browserstack-el-pais.git
- cd browserstack-el-pais

2. Install dependencies
- pip install -r requirements.txt

3. Run the main script
- python main.py

## How to Run on BrowserStack Parallelly (Cross-Browser Testing)

1. BrowserStack credentials are required.
   
2. Set BrowserStack credentials as environment variables:
- setx BROWSERSTACK_USERNAME "your_username"
- setx BROWSERSTACK_ACCESS_KEY "your_access_key"
   
4. Run parallel tests:
- python browserstack_parallel.py 
