# aws-portfolio
This repo has been set up to host Python files that will be run via AWS daily (during weekdays) to provide updates on mutual fund prices and listed stock prices.

It will utilise the following services on AWS:
- AWS Lambda functions
- S3 bucket/RDS instance
- Simple Notification Service or Simple Email Service
- CloudWatch

The plan is as follows:
- [ ] Setup an AWS account & login to management console
- [ ] Write Python script to scrape somewhere/use a trusted source
- [ ] Create AWS Lambda function
- [ ] Create a storage solution on AWS - either S3 bucket or RDS instance (depending on type of data)
- [ ] Update Python script in Lambda to store price data either in S3 bucket or RDS instance
- [ ] Setup Simple Notification Service or Simple Email Service and configure it with my email credentials
- [ ] Setup AWS CloudWatch/trigger Lambda function
- [ ] Test the setup
- [ ] Monitor the setup - can use X-Ray for this
