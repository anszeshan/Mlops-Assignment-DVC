import requests
from bs4 import BeautifulSoup
import csv
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')

def extract_data(url):
    """Extracts links, titles, and descriptions from a website's homepage.

    Args:
        url (str): The URL of the website to scrape.

    Returns:
        dict: A dictionary containing extracted data, or None if an error occurs.
    """

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extracting links
        links = [a.get('href') for a in soup.find_all('a', href=True)]

        # Extracting articles
        articles = soup.find_all('article')

        extracted_data = []
        for article in articles:
            title = article.find('h2')
            if title:
                title = title.text.strip()

            description_element = article.find('p')
            if description_element:
                description = description_element.text.strip()
            else:
                description = ""

            # Data transformation: Removing HTML tags, punctuation, and stopwords
            clean_description = re.sub('<[^<]+?>', '', description)  # Remove HTML tags
            clean_description = re.sub(r'[^\w\s]', '', clean_description)  # Remove punctuation
            clean_description = clean_description.lower()  # Convert to lowercase
            stop_words = set(stopwords.words('english'))
            word_tokens = word_tokenize(clean_description)
            filtered_description = [word for word in word_tokens if word not in stop_words]

            extracted_data.append({'title': title, 'description': ' '.join(filtered_description)})

        return {'links': links, 'articles': extracted_data}

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching data from {url}: {e}")
        return None

def write_to_csv(data, filename):
    """Writes extracted data to a CSV file.

    Args:
        data (dict): Extracted data containing links and articles.
        filename (str): Name of the CSV file to write.
    """
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Link', 'Title', 'Description'])
        for article in data['articles']:
            writer.writerow([data['links'][data['articles'].index(article)], article['title'], article['description']])

# Example usage (replace with actual URLs)
dawn_data = extract_data('https://www.dawn.com/')
bbc_data = extract_data('https://www.bbc.com/')

if dawn_data:
    print("Extracted data from dawn.com:")
    print(dawn_data)
    write_to_csv(dawn_data, 'dawn_data.csv')
    print("Data written to dawn_data.csv")

if bbc_data:
    print("Extracted data from BBC.com:")
    print(bbc_data)
    write_to_csv(bbc_data, 'bbc_data.csv')
    print("Data written to bbc_data.csv")