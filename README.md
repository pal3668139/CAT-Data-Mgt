This project automates steps needed to manage the data that we get from each 350 Seattle CAT Action Survey. The survey data is accessed as .CSV files downloaded from https://tally.so/ or possibly extracted using an integration with Tally. Using Python Pandas, the data for each survey is cleaned, transformed, and loaded to one or more Google BigQuery tables and views. The BigQuery tables and views will be accessible to the CAT team as Google Sheets using a Google Sheets data connector for BigQuery.

We may need to extract data for a particular survey more than once, which will require the project to merge new rows of survey data into the BigQuery tables using a Key ID.

Additional data sources related to this survey data including detailed user data from Action Network and bill data from Take Action Netork (TAN) that well need in related BigQuery tables.
