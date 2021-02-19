# Speakup Elastic Bean Stalk App

This is the structured folder to deploy the fastapi app in Elastic Bean Stalk. 

(Spoiler alert: the python deployment on EBS would not work due to incomptibility between ASGI and WSGI web servers)

## Environment
* fastapi==0.63.0
* librosa==0.8.0
* matplotlib==3.1.2
* numpy==1.19.5
* Pillow==8.1.0
* pydantic==1.7.3
* pypesq==1.2.4
* pystoi==0.3.3
* starlette==0.13.6
* torch==1.7.1
* torchaudio==0.7.2
* tqdm==4.47.0
* uvicorn==0.13.3
* Werkzeug==1.0.1

## EBS Set up
AWS Elastic Beanstalk provides a suitable environment for a number fo different deployments.
The python environment requires a certain structure which is what we have implemented here.

## Atempts to use ASGI with WSGI
This implementation did not work as expected on EBS because of the incompatibility between ASGI and WSGI.

We are working on the following solutions to implement this app.
1. Use gunicorn server with uvicorn workers (first effort failed).
2. Use docker env instead as the container will be able to run regardless of the EBS (at least in theory)
