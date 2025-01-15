import json
import boto3
import os 
import uuid
import base64
import pathlib

import librosa
import matplotlib.pyplot as plt
import numpy as np

from configparser import ConfigParser

def lambda_handler(event, context):
    try:
        print("**STARTING**")
        print("**lambda: final_project_analyze**")

        config_file = 'audio-classifier-config.ini'
        os.environ['AWS_SHARED_CREDENTIALS_FILE'] = config_file

        configur = ConfigParser()
        configur.read(config_file)

        s3_profile = 's3readwrite'
        boto3.setup_default_session(profile_name=s3_profile)

        bucketname = configur.get('s3', 'bucket_name')
    
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucketname)

        # get data 
        print("**Accessing Request Body**")

        if "body" not in event:
            raise Exception("event has no body")
        
        body = json.loads(event["body"])

        if "filename" not in body:
            raise Exception("event has a body but no filename")
        if "data" not in body:
            raise Exception("event has a body but no data")
        if "op" not in body:
            raise Exception("event has a body but no op")

        filename = body["filename"]
        datastr = body["data"]
        op = int(body["op"])

        extension = pathlib.Path(filename).suffix

        if extension != ".wav":
            raise Exception("expecting filename to have .wav extension")
        
        print(op)

        if op != 1 and op != 2:
            raise Exception("expecting op to be either 1 or 2")
        

        base64_bytes = datastr.encode()
        bytes = base64.b64decode(base64_bytes)

        print("**Writing Local Data File**")
        local_filename = "/tmp/data.wav"
        file = open(local_filename, "wb")
        file.write(bytes)
        file.close()

        print("**Performing Data Analysis")
        audio_data, rate = librosa.load(local_filename)

        plt.figure()

        if op == 2:
            transformed = librosa.stft(audio_data)
            db = librosa.amplitude_to_db(np.abs(transformed), ref= np.max)
            #plt.figure(figsize=(6, 4))
            plt.title("Spectrogram of Data")
            librosa.display.specshow(db, x_axis='time', y_axis='log', sr=rate)
            new_filename = "/tmp/spectrogram.jpg"
        elif op == 1:
            librosa.display.waveshow(audio_data, sr=rate)
            new_filename = "/tmp/waveform.jpg"
        

        
        plt.savefig(new_filename)
        plt.close()
        print("**Uploading local file to S3")
        basename = pathlib.Path(filename).stem

        bucketkey = "data_representation/" + basename + "-" + str(uuid.uuid4()) + ".jpg"
        print("S3 bucketkey:", bucketkey)

        bucket.upload_file(new_filename, 
                            bucketkey, 
                            ExtraArgs={
                                'ACL': 'public-read',
                                'ContentType': 'application/jpg'
                            })

        print("**DONE, Augmented Data Uploaded to S3**")

        return {
            'statusCode': 200,
            'body': json.dumps("https://photoapp-johnlim-nu-cs310.s3.us-east-2.amazonaws.com/" + bucketkey)
        }


    except Exception as err:
        print("**ERROR**")
        print(str(err))
        
        return {
            'statusCode': 500,
            'body': json.dumps(str(err))
        }
