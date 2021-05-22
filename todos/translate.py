import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')
translate = boto3.client(service_name='translate')


def getTranslate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    result['Item']['text'] = translate.translate_text(Text=result['Item']['text'], SourceLanguageCode="auto", TargetLanguageCode=event['pathParameters']['language'])['TranslatedText']
    
    #result = translate.translate_text(Text=result['Item'].get('text'), SourceLanguageCode="auto", TargetLanguageCode=event['pathParameters']['language'])

    # create a response
    response = {
        "statusCode": 200,
        #"body": json.dumps(result.get('TranslatedText'),
         #                  cls=decimalencoder.DecimalEncoder)
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    result['Item']

    return response
