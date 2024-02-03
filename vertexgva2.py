# A Voice Chatbot built with Vertex Gemini Pro and Python
# Tested and working on Windows 10. 
# By TechMakerAI on YouTube
# 
import speech_recognition as sr
import pyttsx3
import os
import pyaudio
from datetime import date
import time
import pygame 

import vertexai 

from vertexai.preview.generative_models import GenerativeModel, ChatSession 

vertexai.init(project="vxgva1", location="us-central1")

model = GenerativeModel("gemini-pro")  
chat = model.start_chat()

# for OpenAI TTS model
from openai import OpenAI
client = OpenAI()

pygame.mixer.init()
#os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

today = str(date.today())

engine = pyttsx3.init()
engine.setProperty('rate', 190) # speaking rate 
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[1].id) # 0 for male; 1 for female

# define a chat function to interact with AI model
def chatfun(chat: ChatSession, prompt: str) -> str:
    response = chat.send_message(prompt)
    return response.text

# select to use OpenAI's text to speech API
openaitts = False    
def speak_text(text):
    global openaitts, pvoice 

    if openaitts:

        response = client.audio.speech.create(
            model="tts-1",
            # alloy: man; nova: woman
            voice="nova",
            input= text )
        
        fname = 'output.mp3'
        mp3file =open(fname, 'w+') 

        #if os.path.exists(fname):
        #    os.remove(fname)    
                      
        response.write_to_file(fname)

        try: 
            # pygame.mixer.init()
            pygame.mixer.music.load(mp3file)
            pygame.mixer.music.play()
        
            while pygame.mixer.music.get_busy():
                #
                time.sleep(0.2)
            
            pygame.mixer.music.stop()    
            mp3file.close()
        
        except KeyboardInterrupt:
            pygame.mixer.music.stop()
            mp3file.close()
            #print("\nAudio playback stopped.")
    else:
        engine.say(text)
        # print("AI: " + text)
        engine.runAndWait()

# save conversation to a log file 
def append2log(text):
    global today
    fname = 'chatlog-' + today + '.txt'
    with open(fname, "a") as f:
        f.write(text + "\n")

# Main function  
def main():
    global today, chat
    
    rec = sr.Recognizer()
    mic = sr.Microphone()
    rec.dynamic_energy_threshold=False
    rec.energy_threshold = 400    
    
    sleeping = True 
    # while loop for conversation 
    while True:     
        
        with mic as source1:            
            rec.adjust_for_ambient_noise(source1, duration= 0.5)

            print("Listening ...")
            
            try: 
                audio = rec.listen(source1, timeout = 20, phrase_time_limit = 20)
               
                text = rec.recognize_google(audio)
                
                # AI is in sleeping mode 
                if sleeping == True:
                    # User must start the conversation with the wake word "Jack"
                    # This word can be chagned by the user. 
                    if "jack" in text.lower():
                        request = text.lower().split("jack")[1]
                        
                        sleeping = False
                        # AI is awake now, 
                        # start a new conversation 

                        today = str(date.today()) 
                        append2log(f"_"*40)

                        # if the user's question is none or too short, skip 
                        if len(request) < 5:
                            speak_text("Hi, there, how can I help?")
                            append2log(f"AI: Hi, there, how can I help? \n")
                            continue                      

                    # if user did not say the wake word, nothing will happen 
                    else:
                        continue
                      
                # AI is awake         
                else: 
                    
                    request = text.lower()
                    
                    if "jack" in request:
                        request = request.split("jack")[1]   
                        
                    if "that's all" in request:
                                               
                        append2log(f"You: {request}\n")
                        
                        speak_text("Bye now")
                        
                        append2log(f"AI: Bye now. \n")                        

                        print('Bye now')
                        
                        sleeping = True
                        # AI goes back to speeling mode
                        continue

                
                # process user's request (question)
                append2log(f"You: {request}\n ")

                print(f"You: {request}\n AI: " )
                
                response = chatfun(chat, request #, stream=True
                                   )
              
                print(response)

                speak_text(response.replace("*", "")) 

                append2log(f"AI: {response } \n")
 
            except Exception as e:
                continue 
 
if __name__ == "__main__":
    main()



