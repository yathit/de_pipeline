## Section 3: System Design

You are designing data infrastructure on the cloud for a company whose main business is in processing images. 

The company has a web application which collects images uploaded by customers. The company also has a separate web application which provides a stream of images using a Kafka stream. The company’s software engineers have already some code written to process the images. The company  would like to save processed images for a minimum of 7 days for archival purposes. Ideally, the company would also want to be able to have some Business Intelligence (BI) on key statistics including number and type of images processed, and by which customers.

Produce a system architecture diagram (e.g. Visio, Powerpoint) using any of the commercial cloud providers' ecosystem to explain your design. Please also indicate clearly if you have made any assumptions at any point.

## Solution

Workflow:

1. AWS API Gateway serves as entry point for uploaded images from web application as well as sink for Kafka stream for other web application. 
2. AWS API Gateway post images along with metadata to Lambda function
3. Lambda function will
* process metadata and write statistic to Amazon Kinesis Data Stream which eventually insert to RedShift database 
* put the image to S3 with 7-day lifecycle policy

Assumptions:
* Security details are not addressed
* Cost is not a concern




