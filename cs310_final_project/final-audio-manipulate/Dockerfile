FROM public.ecr.aws/lambda/python:3.11

COPY *.py ${LAMBDA_TASK_ROOT}/
COPY *.ini ${LAMBDA_TASK_ROOT}/

RUN pip3 install librosa
RUN pip3 install soundfile

CMD [ "lambda_function.lambda_handler" ]