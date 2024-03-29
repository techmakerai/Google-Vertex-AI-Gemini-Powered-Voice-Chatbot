# Google-Vertex-AI-Gemini-Powered-Voice-Chatbot

A voice assistant (chatbot) built with Google Vertex AI's version of Gemini Pro and Python. 

This repository includes a Python program that can call Google Vertex AI's version of Gemini Pro API to obtain a response for any request from a user and then convert the text response to an audio response. This version has been tested on Windows 10.

Please watch this YouTube video tutorial to learn more about this code:    
https://youtu.be/owlminpxSaw   

You will need to install the following packages on your computer to run this code:

```console
pip install --upgrade google-cloud-aiplatform   
pip install speechrecognition openai pyttsx3 pyaudio pygame
```
If you have Python 3.12 or newer, also install the "setuptools" package,    

```console
pip install setuptools
```
You also need to have authenticated Vertex AI SDK on your computer, see instructions here, 
https://cloud.google.com/vertex-ai/docs/generative-ai/multimodal/sdk-for-gemini/gemini-sdk-overview
