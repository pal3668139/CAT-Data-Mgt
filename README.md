This project automates steps needed to manage the data that we get from each 350 Seattle CAT Action Survey. The approach provides a fully automated pipeline that will:
 - Automatically store Action Survey responses in Google Sheets using a free integration in Tally.
 - Ingest the raw Action Survey data directly from each Google Sheet file.
 - Clean, transform, and normalize the raw data using Python Pandas scripts.
 - Load the normalized Action Survey data into Google BigQuery tables.
 - Automate the ingest, transform, and load process using Google Cloud Functions and Cloud Scheduler.
 - Provide the CAT team access to our survey data in Google Sheets using a Google Sheets data connector for BigQuery.

PLEASE NOTE: Brief description of files in each folder.
 - data - Prototype normalized data structure, downloaded Tally .CSVs from 2024 legislative session, and more.
 - notebooks - Functioning Python Pandas code that ingests, cleans, and transforms Tally .CSVs
 - src - Early draft Python files that represent the end-state application

Here's a more detailed project description.

### 1. Extract: Data Ingestion from Google Sheets
Using the Tally Google Sheets integration (https://tally.so/help/google-sheets-integration), our raw Action Survey data will be stored in Google Sheets files on our Google Drive. The first step is to automate the extraction of these Google Sheets directly into a DataFrame. 
 - Identify new Google Sheets files based on the naming convention (e.g., 'Week 05, Wednesday February 5, 2025').
 - Use Google Drive API and Google Sheets API to fetch Google Sheets programmatically and pull the data into a DataFrame

### 2. Transform: Data Cleaning and Transformation
Once the data is ingested, Cloud Functions will clean and normalize the raw Action Survey data.
 - Remove duplicates, handle missing values, and apply necessary validations to the data.
 - Transform DataFrame into a normalized format.
 - Calculate new columns to facilitate data analysis.
 - NOTE: This process used to take the Data/Ops team over 30 minutes for each survey.

### 3. Load: Storing Processed Data into Google BigQuery
A Cloud Function will then automatically load the transformed DataFrame into a Google BigQuery table (or tables).
 - Our Action Takers complete each action survey over a period of days.
 - For this reason, we will process data from each Action Survey once per day for 10 days after it is published.
 - The Cloud Function will load the DataFrame into a temporary table in BigQuery.
 - Using a Key ID, the function will then merge rows (new rows only) from the temporary table into a final BigQuery table.

### 4. Automation: Orchestration with Cloud Functions and Cloud Scheduler
CAT has a very predictable schedule for publishing Action Surveys twice per week during the legislative session. 
 - Each Action Survey also uses a standard naming convention such as "Week-05-Sun" and "Week-05-Wed."
 - Using this schedule and standard naming conventions, we will define an ingestion schedule for each Action Survey.
 - The ingestion schedule: Process data from each Action Survey once per day for 10 days after it is published.

Based on our ingestion schedule for each Action Survey, we will:
 - Create a separate Cloud Scheduler job.
 - Setup the Cloud Scheduler jobs to trigger Cloud Functions that ingest, transform, and load our survey data in BigQuery.
 - For the long legislative session, there will be about 32 Cloud Scheduler jobs to manage.

### 5. Data Availability and Analysis
The final BigQuery tables will be accessible via Google Sheets using the BigQuery data connector (https://support.google.com/docs/topic/9699960). 
 - CAT team members will be able to view and analyze the data in real-time from Google Sheets.

There are additional data sources related to Action Survey data including detailed user data from Action Network and bill data from Take Action Netork (TAN). Time permitting, we will load these data sources in related BigQuery tables.