import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from fake_useragent import UserAgent
import os

class IndiaMartScraper:
    def __init__(self, search_query, max_pages=3):
        self.base_url = "https://dir.indiamart.com/search.mp"
        self.search_query = search_query
        self.max_pages = max_pages
        self.ua = UserAgent()
        self.data = []

    def get_headers(self):
        return {
            'User-Agent': self.ua.random,
            'Accept-Language': 'en-US,en;q=0.9',
        }

    def parse_product(self, card):
        """Extract details from a single product card HTML element."""
        try:
            # Note: Selectors (.class_names) depend on current IndiaMART DOM. 
            # You may need to inspect element on the site if these change.
            
            # 1. Product Name
            title_tag = card.find('span', class_='p-title') or card.find('h4')
            title = title_tag.text.strip() if title_tag else "N/A"

            # 2. Price
            price_tag = card.find('span', class_='prc')
            price = price_tag.text.strip() if price_tag else "Ask for Price"

            # 3. Supplier Name
            supplier_tag = card.find('h5', class_='cust-name') or card.find('span', class_='cust-name')
            supplier = supplier_tag.text.strip() if supplier_tag else "N/A"

            # 4. Location
            loc_tag = card.find('span', class_='loc-name') or card.find('p', class_='sm-cl')
            location = loc_tag.text.strip() if loc_tag else "N/A"

            return {
                "Product Name": title,
                "Price": price,
                "Supplier": supplier,
                "Location": location,
                "Category": self.search_query
            }
        except Exception as e:
            # Fail silently for single card to prevent crawler crash
            return None

    def crawl(self):
        print(f"🚀 Starting crawl for: {self.search_query}")
        
        for page in range(1, self.max_pages + 1):
            url = f"{self.base_url}?ss={self.search_query}&mcatid=&catid=&prod_serv=P&pg={page}"
            print(f"   ...Scraping page {page}")

            try:
                response = requests.get(url, headers=self.get_headers())
                
                if response.status_code != 200:
                    print(f"   Blocked or Error on page {page}: {response.status_code}")
                    break

                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Container for product cards (Inspect element to confirm class)
                # IndiaMART often uses 'm-p' or similar for card containers
                product_cards = soup.find_all('div', class_='clg') 
                
                # Fallback if class changed
                if not product_cards:
                     product_cards = soup.find_all('div', class_='lst_cl')

                for card in product_cards:
                    item = self.parse_product(card)
                    if item:
                        self.data.append(item)

                # Politeness Delay (2 to 5 seconds)
                time.sleep(random.uniform(2, 5))

            except Exception as e:
                print(f"Error on page {page}: {e}")

    def save_data(self, filename="data/raw_data.csv"):
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        df = pd.DataFrame(self.data)
        
        # Basic Cleanup before saving
        df.drop_duplicates(inplace=True)
        
        df.to_csv(filename, index=False)
        print(f"✅ Data saved to {filename} ({len(df)} records)")

if __name__ == "__main__":
    # Example: Scraping Industrial Pumps
    scraper = IndiaMartScraper(search_query="industrial pumps", max_pages=2)
    scraper.crawl()
    scraper.save_data()