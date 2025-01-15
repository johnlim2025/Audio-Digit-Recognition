How to Install the Application

1. If you want to create your own inference endpoint on Sagemaker, go to Amazon Sagemaker and upload the jupyter notebook in the jupyter file, along with other files in the jupyter file. Execute the notebook and you will be able to get an endpoint with a trained model (dataset is included in the zip file). Currently, my endpoint only allows s3readwrite IAM profile (in audio-classifier-config.ini in final-audio-predict file) to use. There is a spot to put the name of the endpoint in the .ini file. 

2. Create docker images of each lambda functions with the Dockerfile in each files. Upload each images to ECR. Create lambda functions using these images. For all of the lambda functions, set the runtime to be 5 mins, memory to 1024 MB, and Ephemeral storage to 1024 MB. Also, go to environment variables in configuration and add key = NUMBA_CACHE_DIR and value = /tmp for all functions. 

3. If you wish to use your own bucket and users, change the .ini files in the lambda function files accordingly. 

3. Go to API Gateway and create the APIs. The http verb should be POST for all APIs. 

4. To use the server, first set the .ini accordingly to your created API Gateway. Use the files in the final_project_client to run and test the APIs (CHMOD the .bash files, run docker-build, run docker-run. and python main.py). Put the files you want to use inside final_project_client (some data is provided).

5. Since my bucket is public and url is provided after getting response from manipulate and analyze, you should be able to simply run the client side files and test (if the endpoint and server is running). They will be up until the grading period. 


