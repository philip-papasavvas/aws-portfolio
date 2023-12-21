# aws-portfolio
This repo has been set up to host my serverless event-driven microservices app (Python/Flask), which is a portfolio project.
The end state aims to host a Flask application on AWS that allows a personal portfolio dashboard to visualise changes in the portfolio value and view an attribution. The dashboard is to be fed by an Amazon RDS, which is automatically updated daily with the stock prices of the stocks we're interested in (defined in a config file). 

The plan is as follows (updated on 12 Dec 2023)
- [X] Plan the overall architecture of the application
- [X] Design the database schema
- [X] Write Python script to scrape the prices from Yahoo Finance - utils/price_scraping.py
- [X] Massage the data into an suitable format for stocks - utils/prep_data.py
- [X] Write the stock data to the Stock db table locally
- [X] Placeholders for the dashboard, layout, login, and register HTML pages
- [ ] Populate the transactions table with some dummy transactions per user
- [ ] Calculate the overall portfolio amount per stock for each user based on the number of transactions
- [ ] Write unit tests for these functions defined above - tests/test_price_scraping.py & tests/test_prep_data.py


Use the following AWS applications 
- AWS Lambda functions (serverless architecture)
- RDS instance (use postgreSQL here)
- Simple Notification Service
- CloudWatch (to monitor how the app is performing)

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
