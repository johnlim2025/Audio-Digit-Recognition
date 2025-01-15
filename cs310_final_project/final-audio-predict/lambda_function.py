import json
import boto3
import os 
import uuid
import base64
import pathlib

import librosa
import numpy as np

from configparser import ConfigParser

def lambda_handler(event, context):
    try:
        print("**STARTING**")
        print("**lambda: final_project_predict**")

        config_file = 'audio-classifier-config.ini'
        os.environ['AWS_SHARED_CREDENTIALS_FILE'] = config_file

        configur = ConfigParser()
        configur.read(config_file)

        s3_profile = 's3readwrite'
        boto3.setup_default_session(profile_name=s3_profile)

        region_name = configur.get(s3_profile, 'region_name')
    
        # get data 
        print("**Accessing Request Body**")

        if "body" not in event:
            raise Exception("event has no body")
        
        body = json.loads(event["body"])

        if "filename" not in body:
            raise Exception("event has a body but no filename")
        if "data" not in body:
            raise Exception("event has a body but no data")

        filename = body["filename"]
        datastr = body["data"]

        extension = pathlib.Path(filename).suffix

        if extension != ".wav":
            raise Exception("expecting filename to have .wav extension")

        base64_bytes = datastr.encode()
        bytes = base64.b64decode(base64_bytes)

        print("**Writing Local Data File**")
        local_filename = "/tmp/data.wav"
        file = open(local_filename, "wb")
        file.write(bytes)
        file.close()


        print("**Processing Input Data**")
        data, sample_rate = librosa.load(local_filename)
        features = librosa.feature.mfcc(y = data, sr = sample_rate, n_mfcc = 40)
        features = np.mean(features.T, axis = 0)

        input = features.tolist()

        print("**Performing Prediction**")

        runtime_client = boto3.client('runtime.sagemaker', region_name = region_name)
        endpoint_name = configur.get('sagemaker', 'endpoint')

        input_data = json.dumps(input)
        response = runtime_client.invoke_endpoint(EndpointName = endpoint_name, ContentType='application/json',Body=input_data)


        response_body = response['Body'].read()
        result = json.loads(response_body)
        predictions = np.argmax(result['predictions'][0])


        print("**DONE, Predicted!**")
        print()
        print("**PREDICTED VALUE: ", int(predictions), "**")
        print()


        return {
            'statusCode': 200,
            'body': json.dumps(int(predictions)),
        }

    except Exception as err:
        print("**ERROR**")
        print(str(err))
        
        return {
            'statusCode': 500,
            'body': json.dumps(str(err))
        }
