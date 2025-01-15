import json
import boto3
import os 
import uuid
import base64
import pathlib

import librosa
import soundfile

from configparser import ConfigParser

def lambda_handler(event, context):
    try:
        print("**STARTING**")
        print("**lambda: final_project_manipulate**")

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
        if "pitch" not in body:
            raise Exception("event has a body but no pitch")

        filename = body["filename"]
        datastr = body["data"]
        pitch = int(body["pitch"])

        extension = pathlib.Path(filename).suffix

        if extension != ".wav":
            raise Exception("expecting filename to have .wav extension")
        
        if not(pitch >= -5 and pitch <= 5):
            raise Exception("expecting correct pitch range")

        base64_bytes = datastr.encode()
        bytes = base64.b64decode(base64_bytes)

        print("**Writing Local Data File**")
        local_filename = "/tmp/data.wav"
        file = open(local_filename, "wb")
        file.write(bytes)
        file.close()

        print("**Performing Data Augmentation**")
        new_local_filename = "/tmp/new_data.wav"
        y, rate = librosa.load(local_filename)
        new_y = librosa.effects.pitch_shift(y, sr=rate, n_steps=pitch)
        soundfile.write(new_local_filename, new_y, rate)

        print("**Uploading local file to S3**")
        basename = pathlib.Path(filename).stem

        bucketkey = "data_augmentation/" + basename + "-" + str(uuid.uuid4()) + ".wav"
        print("S3 bucketkey:", bucketkey)

        bucket.upload_file(new_local_filename, 
                            bucketkey, 
                            ExtraArgs={
                                'ACL': 'public-read',
                                'ContentType': 'application/wav'
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
