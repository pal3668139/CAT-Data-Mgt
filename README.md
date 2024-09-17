This project automates steps needed to manage the data that we get from each 350 Seattle CAT Action Survey. The approach provides a fully automated pipeline that:
 - Tally will automatically store action survey responses in Google Sheets using a free integration.
 - Ingests Action Survey data directly from Google Sheets integrated with Tally.
 - Cleans and transforms the data using Python Pandas.
 - Efficiently loads new rows into BigQuery with upsert functionality.
 - Automates the entire process using Google Cloud Functions and Cloud Scheduler, respecting your predictable data schedule.
 - Provides access to the CAT team in Google Sheets using a Google Sheets data connector for BigQuery.

PLEASE NOTE: Please find the Python Pandas code in the 'notebooks' folder, and find relevant .CSVs in the 'data' folder. Please ignore the files in the 'src' and 'tests' folders.

Here's a more detailed project description.

1. Extract: Data Ingestion from Google Sheets
Using the Tally Google Sheets integration (https://tally.so/help/google-sheets-integration), our raw Action Survey data will be stored in Google Sheets files on our Google Drive. The first step is to automate the extraction of these Google Sheets directly into a Pandas DataFrame. 
 - Identify new Google Sheets files based on the naming convention (e.g., 'Week 05, Wednesday February 5, 2025').
 - Use Google Drive API and Google Sheets API to fetch Google Sheets programmatically.
 - Use Google Cloud Functions to periodically check for new sheets and pull the data into a Pandas DataFrame.
 - Store sheet metadata (file name, last processed timestamp) in a tracking system BigQuery table.

2. Transform: Data Cleaning and Transformation
Once the data is ingested, Pandas scripts will clean and normalize the raw Action Survey data.
 - Remove duplicates, handle missing values, and apply necessary validations.
 - Transform data into a normalized format.
 - Calculate new columns to facilitate data analysis.
 - NOTE: This process used to take the Data/Ops team over 30 minutes for each survey. The vastly improved process takes 1 second.

3. Load: Storing Processed Data into Google BigQuery
Pandas scripts will then automatically load the transformed data for the Action Survey into a Google BigQuery table (or tables).
 - Our Action Takers complete each action survey over a period of days.
 - For this reason, we will load data from each survey once per day for a period of 10 days after the Action Survey is published.
 - The Pandas script will load the DataFrame into a temporary table in BigQuery then, using a Key ID, merge new rows of data into the final BigQuery table.

4. Automation: Orchestration with Cloud Functions and Cloud Scheduler
CAT has a very predictable schedule for publishing Action Surveys twice per week during the legislative session. 
 - Each Action Survey also uses a standard naming convention such as "Week 05, Wednesday February 5, 2025." 
 - Using this schedule and standard naming conventions, we will define an ingestion schedule for each Action Survey: Once per day for 10 days after the survey is published.

Based on our ingestion schedule for each Action Surveys, we will:
 - Create a separate Cloud Scheduler job for each Action Survey (once per day for 10 days after the survey is published)
 - Setup the Cloud Scheduler jobs to trigger the Pandas script, which ingests, cleans and transforms, and loads our Action Survey data in BigQuery
 - For the long legislative session, there will be about 30 Cloud Scheduler jobs to manage

5. Data Availability and Analysis
The final BigQuery tables will be accessible via Google Sheets using the BigQuery data connector (https://support.google.com/docs/topic/9699960). This provides easy access for team members to analyze the data in real-time from Google Sheets.
 - Instruct team members on how to connect Google Sheets to BigQuery using the Data > Data connector > BigQuery feature.
 - Use this to query the BigQuery tables directly from Google Sheets for analysis.

There are additional data sources related to Action Survey data including detailed user data from Action Network and bill data from Take Action Netork (TAN). Time permitting, we will load these data sources in related BigQuery tables.
