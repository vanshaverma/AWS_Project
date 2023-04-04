import json
import boto3
import csv

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sns_client = boto3.client('sns')

def lambda_handler(event, context):
    try:
        # Get the S3 bucket name and key from the event
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        s3_file_name = event['Records'][0]['s3']['object']['key']
        
        response = s3_client.get_object(Bucket=bucket_name, Key=s3_file_name)
        
        file_content = response['Body'].read().decode('utf-8')
        # Convert the CSV file contents to a list of lists
        csv_rows = csv.reader(file_content.splitlines())
        
        table = dynamodb.Table('Employee')
        with table.batch_writer() as batch:
            for row in csv_rows:
                batch.put_item(Item={
                    "employeeId": str(row[0]),
                    "firstName": str(row[1]),
                    "lastName": str(row[2]),
                    "email": str(row[3]),
                    "phoneNo": str(row[4]),
                    "hireDate": str(row[5]),
                    "jobId": str(row[6]),
                    "salary": str(row[7])
                })
                
    except Exception as err:
        print(err)
    
    # Send status notification using SNS
    message = "Records processed successfully"
    subject = f"File processed - {s3_file_name}"
    sns_client.publish(
        TopicArn='arn:aws:sns:us-east-1:054746321232:my-lambda-notification',
        Subject=subject,
        Message=message
    )
    

    return {
        'statusCode': 200,
        'body': json.dumps('File uploaded successfully')
    }