# aws-portfolio
This repo has been set up to host my Python/Flask portfolio project.
The scope of this project has changed, instead of running the Flask application on AWS, I will instead use a 
serverless architecture, consisting of using the Lambda, Simple Queue Service, Simple
Email Service and API Gateway service, in addition to Relational Database Service
(PostgreSQL) for the database.

The deployment steps are as follows (updated 29 Jan 2024):
- 1. Create the RDS PostgreSQL instance with the schema as below
- 2. Setup the Lambda functions for running the stock price update
- 3. Implement IAM roles and policies for Lambda functions and RDS, API Gateway.
- 4. Setup the SQS queue and grant the necessary permissions to the Lambda functions 
to process messages.
- 5. Setup Simple Email Service for email notifications.
- 6. Define the API Gateway to route requests to the Lambda functions
- 7. Implement CloudWatch Logs and Alarms for monitoring.

- [ ] Setup AWS CloudWatch/trigger Lambda function
- [ ] Test the setup
- [ ] Monitor the setup - can use X-Ray for this

Example Portfolio - 5 stocks & their tickers
- Tesla - TSLA
- Microsoft - MSFT
- Berkshire Hathaway - BRK-B
- Nvidia - NVDA
- Alphabet - GOOGL


Database Schema Plan - This is an outline of the db schema
- User Table:
    - User ID (Primary Key) 
    - Username
    - Email
    - Password (Hashed and salted)
- Stocks Table:
    - Stock ID (Primary Key)
    - Ticker Symbol
    - Company Name
- Transactions Table:
    - Transaction ID (Primary Key)
    - User ID (Foreign Key)
    - Stock ID (Foreign Key)
    - Is Purchase (1 for Buy, 0 for Sell)
    - Number of Shares
    - Transaction Date
- Portfolio Table:
    - Portfolio ID (Primary Key)
    - User ID (Foreign Key)
    - Stock ID (Foreign Key)
    - Number of Shares
- Stock Prices Table:
    - Price ID (Primary Key)
    - Stock ID (Foreign Key)
    - Date
    - Close Price
