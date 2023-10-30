from bs4 import BeautifulSoup
import justext
import pandas as pd
import csv
import requests
from requests.exceptions import Timeout
import re
import time
from list_ignored import ignored_words
from urllib.parse import urljoin, urlparse
import warnings
import datetime
warnings.filterwarnings("ignore")

def crawl_and_scrape(url, level, max_level, sentences, main_url, visited_urls,depth_list): 
    if level > max_level: 
        return
    if level > depth_list[0]:
        depth_list[0] = level
    # Add the current URL to the visited URLs set
    visited_urls.add(url)

    try:
        # Make an HTTP GET request to the current URL with a 5-second timeout
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
        response = requests.get(url, timeout=20,  verify=False, headers=headers)
    except Timeout:
        print(f"Timeout when requesting: {url}")
        return # Skip this page and continue with the next one
    except Exception as e:
        print(f"Error when requesting: {url} - {e}")
        return # Skip this page and continue with the next one

    if response.status_code == 200:
        print(f"Scraping: {url}")

        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = justext.justext(response.content, justext.get_stoplist("English"))

            for paragraph in paragraphs:
              if not paragraph.is_boilerplate:
                sentences.append(paragraph.text)

        except Exception as e:
            print(f"Error parsing the page: {e}")
            return # Skip this page and continue with the next one

        # Sleep to be considerate to the website
        time.sleep(1)

        # Find and scrape links to other pages on the current page
        links = soup.find_all('a', href=True)
        for link in links:
            next_url = link['href']

            # Handle relative URLs and ensure they are within the same domain as the main URL
            next_url = urljoin(main_url, next_url)

            if next_url.startswith(main_url) and next_url not in visited_urls:
            #if next_url not in visited_urls:
                # Recursively crawl and scrape the next URL
                crawl_and_scrape(next_url, level + 1, max_level, sentences, main_url, visited_urls,depth_list)

    else:
        print(f"Failed to retrieve: {url}")
        print(f"Response Code - {response.status_code}")
        depth_list[1]=depth_list[1]+1
    return

# Define the path to the CSV file
csv_file = "clients1.csv"
max_crawl_level = 6
columns = ['Index No', 'Main URL', 'Visited Links','Duration','Depth','Number of Lines','False Links']
df = pd.DataFrame(columns=columns)
count=1

# Initialize a set to store unique domains
unique_domains = set()

# Read the CSV file to get a list of domains
with open(csv_file, "r") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        if "company_domain" in row:
            domain = row["company_domain"]
            # Check if the domain is not empty
            if domain:
                # Add "https://" if not already present
                if not domain.startswith("http://") and not domain.startswith("https://"):
                    domain = "https://" + domain
                # Add the domain to the set
                unique_domains.add(domain)

# Iterate through the list of domains and crawl each one
for main_url in unique_domains:
    print(f"Scraping: {main_url}")
    start_time = datetime.datetime.now()
    # Parse the domain name from the main URL
    parsed_url = urlparse(main_url)
    domain_name = parsed_url.netloc
    if domain_name.startswith('www.') :
        domain_name = domain_name[4:]
    else:
        # Remove TLD and anything after the first dot
        domain_name = re.sub(r'\..*', '', domain_name)
    # Create a list to store sentences
    sentences = []

    # Create a set to keep track of visited URLs
    visited_urls = set()
    depth_list = [1,0]
    # Start crawling and scraping
    crawl_and_scrape(main_url, 1, max_crawl_level, sentences, main_url, visited_urls, depth_list)
    depth = depth_list[0]  # Retrieve the updated depth
    # Construct the output file name using the domain name
    output_file = f"./JusText_Clients/{domain_name}.txt"
    if sentences:
        # Open the file for writing
        with open(output_file, "w") as file:
            # Write sentences to the file
            for sentence in sentences:
                file.write(sentence + '\n')
        # Record the end time
        end_time = datetime.datetime.now()
        # Calculate the scraping duration
        scraping_duration = round((end_time - start_time).total_seconds(),2)
        # Add data to the DataFrame
        data = {
            "Index No": [count],
            "Main URL": [main_url],
            "Visited Links": [len(visited_urls)],
            "Duration":[scraping_duration],
            "Depth": [depth_list[0]],
            "Number of Lines":[len(sentences)],
            "False Links":[depth_list[1]]
        }
        count+=1
        df = pd.concat([df, pd.DataFrame(data)])
        print(df)
        # Specify the file path where you want to save the Excel file
        file_path = "jusText_clients_status.xlsx"

        # Save the DataFrame to the Excel file
        df.to_excel(file_path ,index=False)
        print("Status Updated!")
    else :
        # Open the file for writing
        with open(output_file, "w") as file:
            # Write sentences to the file
            file.write("Nothing was scraped!" + '\n')    
    print(f"File has been saved to {output_file}")
print("Scraping Completed!")
