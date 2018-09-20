
import json
import urllib.parse
import boto3
import os

import pykintone # https://github.com/icoxfog417/pykintone
from pykintone import model

s3 = boto3.client('s3')

class Soracom(model.kintoneModel):
    def __init__(self, data, label=""):
        super(Soracom, self).__init__()
        self.label = label
        self.date = data['payloads']['date']
        self.deveui = data['payloads']['deveui']
        self.tmpc = data['payloads']['tmpc']
        self.prsp = data['payloads']['prsp']

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        json_stream = response['Body'].read()
        json_stream = json_stream.decode('utf-8')
        decoder = json.JSONDecoder()

        while len(json_stream) > 0:
            record, index = decoder.raw_decode(json_stream)
            json_stream = json_stream[index:]
            print (record)

            soracom = Soracom(data=record)
            app = pykintone.app(os.environ['KINTONE_SUBDOMAIN'], os.environ['KINTONE_APP_ID'], os.environ['KINTONE_API_TOKEN'])
            r = app.create(soracom)
            if r.ok:
                created_id = r.record_id
                print(created_id)

        response = {
            "statusCode": 200,
            "body": {json.dumps({"id": created_id})}
        }
        return response 
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
        response = {
            "statusCode": 500,
            "body": json.dumps(e)
        }
        return response