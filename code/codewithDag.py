from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import csv
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 5, 13),
    'catchup': False
}

# Function to extract data from a URL
def extract_data(url):
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

# Function to write data to a CSV file
def write_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Link', 'Title', 'Description'])
        for article in data['articles']:
            writer.writerow([data['links'][data['articles'].index(article)], article['title'], article['description']])

# Define the DAG
with DAG('data_extraction_dag', 
         default_args=default_args,
         schedule_interval='@daily',  # Run the DAG daily
         catchup=False) as dag:

    # Define the task to extract data from dawn.com
    extract_dawn_data = PythonOperator(
        task_id='extract_dawn_data',
        python_callable=extract_data,
        op_kwargs={'url': 'https://www.dawn.com/'}
    )

    # Define the task to extract data from bbc.com
    extract_bbc_data = PythonOperator(
        task_id='extract_bbc_data',
        python_callable=extract_data,
        op_kwargs={'url': 'https://www.bbc.com/'}
    )

    # Define the task to write dawn data to CSV
    write_dawn_to_csv = PythonOperator(
        task_id='write_dawn_to_csv',
        python_callable=write_to_csv,
        op_kwargs={'data': extract_dawn_data.output, 'filename': 'dawn_data.csv'}
    )

    # Define the task to write bbc data to CSV
    write_bbc_to_csv = PythonOperator(
        task_id='write_bbc_to_csv',
        python_callable=write_to_csv,
        op_kwargs={'data': extract_bbc_data.output, 'filename': 'bbc_data.csv'}
    )

    # Set task dependencies
    extract_dawn_data >> write_dawn_to_csv
    extract_bbc_data >> write_bbc_to_csv
