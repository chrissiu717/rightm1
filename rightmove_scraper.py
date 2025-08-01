from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv
from datetime import datetime
import math

# --- Setup headless browser ---
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

# --- Base URL ---
base_url = (
    "https://www.rightmove.co.uk/property-for-sale/find.html?"
    "locationIdentifier=REGION%5E87490"
    "&radius=40"
    "&minBedrooms=2"
    "&maxBedrooms=3"
    "&minPrice=300000"
    "&maxPrice=425000"
    "&displayPropertyType=detached"
    "&displayPropertyType=semi-detached"
    "&displayPropertyType=terraced"
    "&mustHave=freehold"
    "&dontShow=retirement,sharedOwnership,auction"
    "&sortType=6"
    "&maxDaysSinceAdded=1"
)

# --- Load first page and detect total ---
driver.get(base_url)
time.sleep(5)

try:
    total_text = driver.find_element(By.CLASS_NAME, "searchHeader-resultCount").text
    total_listings = int(total_text.replace(",", ""))
except:
    print("Could not detect total listings.")
    total_listings = 24  # default fallback

results = []
pages = math.ceil(total_listings / 24)

for i in range(pages):
    page_url = base_url + f"&index={i * 24}"
    driver.get(page_url)
    time.sleep(3)
    cards = driver.find_elements(By.CLASS_NAME, "l-searchResult")

    for card in cards:
        try:
            title = card.find_element(By.CLASS_NAME, "propertyCard-title").text
            price = card.find_element(By.CLASS_NAME, "propertyCard-priceValue").text
            link = card.find_element(By.CLASS_NAME, "propertyCard-link").get_attribute("href")
            address = card.find_element(By.CLASS_NAME, "propertyCard-address").text
            summary = card.find_element(By.CLASS_NAME, "propertyCard-description").text.lower()

            if "bed" in summary:
                bed_text = summary.split("bed")[0].strip()
                bedrooms = ''.join(filter(str.isdigit, bed_text))
            else:
                bedrooms = "unknown"

            if "detached" in summary:
                prop_type = "Detached"
            elif "semi-detached" in summary:
                prop_type = "Semi-detached"
            elif "terraced" in summary:
                prop_type = "Terraced"
            else:
                prop_type = "Other"

            try:
                added = card.find_element(By.CLASS_NAME, "propertyCard-branchSummary-addedOrReduced").text
            except:
                added = "unknown"

            results.append({
                "Title": title,
                "Price": price,
                "Address": address,
                "Bedrooms": bedrooms,
                "Property Type": prop_type,
                "URL": link,
                "Added": added
            })

        except Exception as e:
            print("Error parsing card:", e)

driver.quit()

# --- Save to CSV ---
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
filename = f"rightmove_full_{timestamp}.csv"
with open(filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print(f"✅ Saved {len(results)} listings to {filename}")