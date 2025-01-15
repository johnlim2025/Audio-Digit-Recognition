import requests
import jsons

import pathlib
import logging
import sys
import os
import time
import base64

from configparser import ConfigParser

#############################################################################
# requests

def web_service_get(url):
    try:
        retries = 0
        while True:
            response = requests.get(url)
            if response.status_code in [200, 400, 480, 481, 482, 500]:
                break
            retries += 1
            if retries < 3:
                time.sleep(retries)
                continue
            break
        return response
    except Exception as e:
        print("**ERROR**")
        logging.error("web_service_get() failed:")
        logging.error("url: ", url)
        logging.error(e)
        return None

def web_service_post(url, object):
    try:
        retries = 0
        while True:
            response = requests.post(url, json=object)
            if response.status_code in [200, 400, 480, 481, 482, 500]:
                break
            retries += 1
            if retries < 3:
                time.sleep(retries)
                continue
            break
        return response
    except Exception as e:
        print("**ERROR**")
        logging.error("web_service_post() failed:")
        logging.error("url: ", url)
        logging.error(e)
        return None

#############################################################################
# commands

def predict(baseurl):
    try:
        print("Enter WAV filename>")
        local_filename = input()

        if not pathlib.Path(local_filename).is_file():
            print("WAV file '", local_filename, "' does not exist...")
            return
        
        
        infile = open(local_filename, "rb")
        bytes = infile.read()
        infile.close()

        
        data = base64.b64encode(bytes)
        datastr = data.decode('utf-8')

        data = {"filename": local_filename, "data": datastr}

        res = None

        api = '/predict'

        url = baseurl + api

        res = web_service_post(url, data)


        if res.status_code == 200: #success
            pass
        else:
            # failed:
            print("Failed with status code:", res.status_code)
            print("url: " + url)
            body = res.json()
            print("Error message:", body)
            return

        #
        # success, extract jobid:
        #
        body = res.json()

        print("Prediction Complete")
        print("Prediction: ", body)
        return

    except Exception as e:
        logging.error("**ERROR: predict() failed:")
        logging.error("url: " + url)
        logging.error(e)
        return


def manipulate(baseurl):
    try:
        print("Enter WAV filename>")
        local_filename = input()
        print()
        print("Enter the number of steps to shift pitch from -5 to 5:")
        shift = int(input())

        if not pathlib.Path(local_filename).is_file():
            print("WAV file '", local_filename, "' does not exist...")
            return
        
        
        infile = open(local_filename, "rb")
        bytes = infile.read()
        infile.close()

        
        data = base64.b64encode(bytes)
        datastr = data.decode('utf-8')

        data = {"filename": local_filename, "data": datastr, "pitch": shift}

        res = None

        api = '/manipulate'

        url = baseurl + api

        res = web_service_post(url, data)


        if res.status_code == 200: #success
            pass
        else:
            # failed:
            print("Failed with status code:", res.status_code)
            print("url: " + url)
            body = res.json()
            print("Error message:", body)
            return

        #
        # success, extract jobid:
        #

        print("Manipulation Complete")
        print("Manipulated WAV file uploaded to S3 Bucket")
        print("URL: ", res.json())
        return

    except Exception as e:
        logging.error("**ERROR: manipulate() failed:")
        logging.error("url: " + url)
        logging.error(e)
        return
    

def analyze(baseurl):
    try:
        print("Enter WAV filename>")
        local_filename = input()
        print()
        print(">> Enter the operation you want to start:")
        print("     1 => Waveform")
        print("     2 => Spectrogram")
        op = int(input())

        if not pathlib.Path(local_filename).is_file():
            print("WAV file '", local_filename, "' does not exist...")
            return
        
        
        infile = open(local_filename, "rb")
        bytes = infile.read()
        infile.close()

        
        data = base64.b64encode(bytes)
        datastr = data.decode('utf-8')

        data = {"filename": local_filename, "data": datastr, "op": op}

        res = None

        api = '/analyze'

        url = baseurl + api

        res = web_service_post(url, data)


        if res.status_code == 200: #success
            pass
        else:
            # failed:
            print("Failed with status code:", res.status_code)
            print("url: " + url)
            body = res.json()
            print("Error message:", body)
            return

        #
        # success, extract jobid:
        #

        print("Analyzation Complete")
        print("Analysis uploaded to S3 Bucket")
        print("URL: ", res.json())
        return

    except Exception as e:
        logging.error("**ERROR: analyze() failed:")
        logging.error("url: " + url)
        logging.error(e)
        return










#############################################################################
# main

def prompt():
    try:
        print()
        print(">> Enter a Command:")
        print("     0 => end")
        print("     1 => predict")
        print("     2 => manipulate")
        print("     3 => analyze")

        cmd = input()

        if cmd == "":
            cmd = -1
        elif not cmd.isnumeric():
            cmd = -1
        else:
            cmd = int(cmd)
        
        return cmd 
    except Exception as e:
        print("**ERROR: invalid input**") 
        return -1 

try:
    print()
    print()
    print("------------------------------------------")
    print("------------------------------------------")
    print("Welcome to Spoken Digit Recognition Agent!")
    print("------------------------------------------")
    print("------------------------------------------")
    print()
    print()

    sys.tracebacklimit = 0
    config_file = 'spoken_digit_config.ini'

    configur = ConfigParser()
    configur.read(config_file)
    baseurl = configur.get('client', 'webservice')

    cmd = prompt()

    while cmd != 0:
        if cmd == 1:
            predict(baseurl)
        elif cmd == 2:
            manipulate(baseurl)
        elif cmd == 3:
            analyze(baseurl)
        else:
            print("** Unknown Command, Please Try Again**")
        
        cmd = prompt()

    print()
    print("**DONE**")
    sys.exit(0)

except Exception as e:
  logging.error("**ERROR: main() failed:")
  logging.error(e)
  sys.exit(0)







