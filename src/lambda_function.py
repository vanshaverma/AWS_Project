import json
import boto3

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Employee')


def lambda_handler (event, context):
    
    try:
        # Get the S3 bucket name and key from the event
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        print(bucket_name)
        s3_file_name = event['Records'][0]['s3']['object']['key']
        
        response = s3_client.get_object(Bucket=bucket_name, Key=s3_file_name)
        
        file_content = response['Body'].read().decode('utf-8')
        employees = file_content.split("\n")
        for emp in employees:
            emp = emp.split(",")
            table.put_item(
                Item = {
                    "employeeId" : str(emp[0]),
                    "firstName" : str(emp[1]),
                    "lastName" : str(emp[2]),
                    "email" : str(emp[3]),
                    "phoneNo" : str(emp[4]),
                    "hireDate" : str(emp[5]),
                    "jobId" : str(emp[6]),
                    "salary" : str(emp[7])
                }
                )
    except Exception as err:
        print(err)
    
    return {
        'statusCode': 200,
        'body': json.dumps('File uploaded success')
    }
