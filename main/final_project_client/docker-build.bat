@echo off
REM
REM Windows BATCH script to build docker container
REM
@echo on
docker rmi final-project-client
docker build -t final-project-client .