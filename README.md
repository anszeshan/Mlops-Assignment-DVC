# Mlops-Assignment-DVC
**Mlops Assignment**
This repository contains the code and documentation for a data pipeline implemented for the purpose of automating data extraction, transformation, and storage using Apache Airflow, web scraping techniques, and Data Version Control (DVC).

**Workflow Overview:**
    Data Extraction:
      Web scraping techniques were employed to extract data from dawn.com and bbc.com. Links from the landing pages were gathered, and titles and descriptions from articles displayed on their homepages were extracted.
    Data Transformation:
      The extracted data underwent preprocessing steps including HTML tag removal, punctuation removal, stopwords removal, lowercase conversion, and tokenization to prepare it for further analysis.
    Data Storage and Version Control (DVC):
      Processed data was stored in CSV files, and Data Version Control (DVC) was implemented to track versions of the data. Metadata was versioned against each DVC push to the GitHub repository to ensure accurate recording of changes.
    Apache Airflow DAG Development:
      An Apache Airflow DAG script was developed to automate the data pipeline. Tasks for data extraction, transformation, and storage were defined, and task dependencies were established to ensure proper execution order.
      
**Challenges Encountered:**
  Challenges included adapting to changes in website structures for effective web scraping and managing task dependencies and error handling within the Apache Airflow DAG.

**Repository Structure:**
code/: Contains Python scripts for data extraction, transformation, and storage, as well as the Apache Airflow DAG script.
documentation/: Includes documentation of the data preprocessing steps and DVC setup, as well as a brief report detailing the workflow and challenges encountered.
data/: Stores processed data CSV files.

**Usage:**
Clone the repository: git clone https://github.com/anszeshan/Mlops-Assignment-DVC.git
Navigate to the project directory: cd your-repository
Execute the Python scripts for data extraction, transformation, and storage.
Access the processed data CSV files in the data/ directory.
Explore the documentation in the documentation/ directory for detailed information on the project workflow and implementation.
