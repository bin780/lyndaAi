# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 11:29:22 2020

@author: Jibin
"""






import speech_recognition as sr
import os
import sys
import re
import webbrowser
import smtplib
import requests
import subprocess
from pyowm import OWM
import youtube_dl
import vlc
import urllib
import urllib.request
import json
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import wikipedia
import random
from time import strftime
import pyttsx3
import io
import Train



GUI=None

def getValue(entities,key):
    if key in entities:
        return entities[key]
    else:
        return ""                                                          # function to extract value from the returned entity

def extractEntity(parsing):
    d={}
    for i in parsing:                                                       #function to extrat entity from the value returned
        d[i["slotName"]]=i["value"]["value"]
    return d

class Lynda():                                                             #Lynda Ai class which contains various apis and call function
    def __init__(self,gui=None):
        self.gui=gui
        self.model=Train.load_model()                                        #constructor loading the model
        self.lyndaResponse(
            'Hi User, I am Lynda and I am your personal voice assistant, Please give a command or say "help me" and I will tell you what all I can do for you.')

    def myCommand(self):
        "listens for commands"
        # print("here")
        r = sr.Recognizer()
        with sr.Microphone() as source:                                   #function to listen to the user voice and get commmand
            print('Say something...')
            r.pause_threshold = 0.7
            r.adjust_for_ambient_noise(source, duration=0.7)
            audio = r.listen(source)
        try:
            print("here")
            command = r.recognize_google(audio).lower()
            print("here1")
            print('You said: ' + command + '\n')
        # loop back to continue to listen for commands if unrecognizable speech is received
        except sr.UnknownValueError:
            print('....')
            command = self.myCommand()
        return command

    def lyndaResponse(self, audio):
        "speaks audio passed as argument"                                #function to give the voiced response
        eng = pyttsx3.init()
        p=str(audio)
        if self.gui != None:
            self.gui.Message1.configure(text=audio)

        # GUI.changeText(audio)
        # print(audio.splitlines())
        for line in range(0, 1):
            eng.say(audio)
            eng.runAndWait()

    def assistant(self,command=None):
        "if statements for executing commands"

        # open subreddit Reddit
                                                                                                #function to get the classified intent and getting theier entitires/slot va;ues
        if command==None:
            command=self.myCommand()

        parsing = self.model.parse(command)
        # print(parsing[0]["slotName"],parsing[1]["slotName"],parsing[0]["value"]["value"],parsing[1]["value"]["value"])
        print(json.dumps(parsing, indent=2))

        intents = self.model.get_intents(command)
        print(intents[0]["intentName"])
        # print(parsing)
        # res=json.dumps(intents, indent=2)

        intent = intents[0]["intentName"]

        parsing = self.model.get_slots(command, intent)

        entities = extractEntity(parsing)

        self.callApi(intent, entities)

    def openWeb(self,entities):
        # reg_ex = re.search('open (.+)', command)
        domain = getValue(entities, "name")
        print(domain)
        if domain:
            # domain = reg_ex.group(1)
            print(domain)
            url=""
            if '.'not  in domain:
                url = 'https://www.' + domain + '.com'
            else:
                url='https://www.'+domain
            webbrowser.open(url)
            try:
                self.gui.web.load(QUrl("https://www.google.com"))
                self.lyndaResponse('The website you have requested has been opened for you Sir.')
            except Exception as e:
                print(e)
        else:
            self.lyndaResponse("i didn't find anything")

    def greeting(self,command):
        day_time = int(strftime('%H'))
        if day_time < 12:
            self.lyndaResponse('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            self.lyndaResponse('Hello Sir. Good afternoon')
        else:
            self.lyndaResponse('Hello Sir. Good evening')

    def getWeather(self,entities):
        # reg_ex = re.search('current weather in (.*)', command)
        print(entities)
        try:
            city = getValue(entities, "city")
            state = getValue(entities, "state")
            time = getValue(entities, "time")
            owm = OWM(API_key='2e50289c3dac66bcb86d009dabfc4e66')
            print(city)
            obs = owm.weather_at_place(city + "," + state)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit='celsius')
            self.lyndaResponse(
                'Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (
                city, k, x['temp_max'], x['temp_min']))
        except Exception as e:
            print(e)

    def getNews(self,entities):
        try:
            news_url = "https://news.google.com/news/rss"
            Client = urlopen(news_url)
            xml_page = Client.read()
            Client.close()
            soup_page = soup(xml_page, "xml")
            news_list = soup_page.findAll("item")
            for news in news_list[:10]:
                self.lyndaResponse(news.title.text.encode('utf-8'))
        except Exception as e:
            print(e)

    def email(self,entites):
        # lyndaResponse('Who is the recipient?')
        recipient = getValue(entites, "res")
        subject = getValue(entites, "res")
        contacts = {'jibin': 'joytom780@gmail.com'}
        if recipient == "":
            self.lyndaResponse("who shall i mail to?")
            recipient = self.myCommand()
        self.lyndaResponse("what is the email address of " + recipient)
        recipient = self.myCommand()
        if subject == "":
            self.lyndaResponse('What should I say to him?')
            subject = self.myCommand()
        try:
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('myt94458@gmail.com', 'qwerty@780')
            mail.sendmail('myt94458@gmail.com', recipient, subject)
            mail.close()
            self.lyndaResponse('Email has been sent successfuly. You can check your inbox.')
        except Exception as e:
            print(e)
            self.lyndaResponse('something went wrong ....please bare with me')

    def launch(self,entites):
        # reg_ex = re.search('launch (.*)', command)
        try:
            appname = getValue(entites, "app")
            appname1 = appname + ".exe"
            subprocess.call('media/' + appname1)

            self.lyndaResponse('I have launched the desired application')
        except Exception as e:
            print(e)
            self.lyndaResponse("i cannot find the application")

    def playMusic(self,entities):
        path = 'media'
        folder = path
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        mysong = getValue(entities, "name")
        artist = getValue(entities, "artist")
        album = getValue(entities, "album")
        if mysong == "":
            self.lyndaResponse('What song shall I play Sir?')
            mysong = self.myCommand()
        print(os.listdir(path))
        if mysong + '.mp4' not in os.listdir(path):
            try:

                query_string = urllib.parse.urlencode({"search_query": mysong})
                html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
                search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
                print("http://www.youtube.com/watch?v=" + search_results[0])

                print(search_results)
                # if url_list!=[]:
                url = search_results[0]
                ydl_opts = {}

                os.chdir(path + "/")
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                result = ydl.extract_info(url, download=False)
                outfile = ydl.prepare_filename(result).split('.')[0]
                print("we are at", os.curdir)
                print(outfile)
                # os.chdir('./media/')
                print(os.curdir)

                os.rename(outfile + '.mp4', mysong + '.mp4')
                mysong = mysong + ".mp4"

                import time
                vlc_instance = vlc.Instance()
                player = vlc_instance.media_player_new()
                media = vlc_instance.media_new(mysong)
                player.set_media(media)
                player.play()
                next=self.myCommand()
                if "stop" in next.split():
                    player.stop()
                player.stop()
            except Exception as e:
                print(e)
                self.lyndaResponse("something happended ...plaease bear with me")



    def getSearch(self,entitites):
        # reg_ex = re.search('tell me about (.*)', command)

        query = getValue(entitites, "query")
        try:
            if query:
                topic = query
                ny = wikipedia.search(topic)
                self.lyndaResponse(wikipedia.summary(ny[0]).encode('utf-8'))
        except Exception as e:
            from googlesearch import search
            self.lyndaResponse("here are the top result")

            for j in search(query, tld="co.in", num=10, stop=1, pause=2):
                self.lyndaResponse(j)

    def getTime(self,command):
        import datetime
        now = datetime.datetime.now()
        self.lyndaResponse('Current time is %d hours %d minutes' % (now.hour, now.minute))

    def helpMe(self,command):
        self.lyndaResponse("""
           Currently I can do :

           
           1. Open any website
           2. Send email/email : Follow up questions such as recipient name, content will be asked in order.
           3. Current weather in any city.
           4. Greetings
           5. play any music video
           6. read the news for today
           7. read the current time
           8 launch a local program
           9. ask about any topic """)

    def shutdown(self,command):
        self.lyndaResponse('Bye bye Sir. Have a nice day')
        sys.exit()


    def last(self,query):
        self.lyndaResponse("i can't find what are you looking ...")
        self.lyndaResponse("let me search the web")
        webbrowser.open("https://www.google.com/search?=")









    def callApi(self,intent, entities):

        if intent == 'getWeather':
            self.getWeather(entities)
        elif intent == 'playMusic':
            self.playMusic(entities)
        elif intent == 'getTime':
            self.getTime(entities)
        elif intent == 'getNews':
            self.getNews(entities)
        elif intent == "openWeb":
            self.openWeb(entities)
        elif intent == "getSearch":
            self.getSearch(entities)
        elif intent == "getGreeting":
            self.greeting(entities)                                                           # function to call API's according to intent and passing the entities to them
        elif intent == "shutdown":
            self.shutdown(entities)
        elif intent == "helpme":
            self.helpMe(entities)
        elif intent == "launchApp":
            self.launch(entities)
        elif intent == 'email':
            self.email(entities)
        else:
            self.last(entities)






def start():
    import Train as m

    nlu_engine = m.load_model()

    # lyndaResponse("start speeaking")


    # loop to continue executing multiple commands

    lynda=Lynda(nlu_engine)

    while True:
        lynda.assistant()

if __name__ == '__main__':

    start()



