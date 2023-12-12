# aws-portfolio
This repo has been set up to host my Python/Flask portfolio project.
The aim is for the end state to host a Flask application on AWS that allows for a personal portfolio dashboard, to visualise changes in the portfolio value and view an attribution. The aim is for the dashboard to be fed by an Amazon RDS which is automatically updated each day with the stock prices from the stocks that we're interested in. 

The plan is as follows:
- [ ] Plan the overall architecture of the application
- [ ] Design the database schema
- [X] Write Python script to scrape the prices from Yahoo Finance
- [ ] Store the data in the sqlite db locally
- [ ] 

I aim to try to use lots of AWS services to best get a feel for how they work, such as:
- AWS Lambda functions
- S3 bucket/RDS instance
- Simple Notification Service or Simple Email Service
- CloudWatch

The plan when migrating the source code (that runs successfully on my local machine) to AWS is:
- [X] Setup an AWS account & login to management console
- [X] Setup Simple Notification Service or Simple Email Service and configure it with my email credentials
- [X] Setup IAM user credentials (not root user)
- [ ] Create a storage solution on AWS -RDS instance (depending on type of data)
- [ ] Tweak the script to store price data either in S3 bucket or RDS instance
- [ ] Create AWS Lambda function
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
