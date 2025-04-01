import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '').strip()
                print(command)
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that")
        return ""
    except sr.RequestError:
        print("Error with speech recognition")
        return ""
    return command

def run_alexa():
    command = take_command()
    print(command)
    if not command:
        return
    
    if 'play' in command:
        song = command.replace('play', '').strip()
        talk('Playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        talk('Current time is ' + time)
    elif 'who is' in command or 'what is' in command or 'tell me about' in command:
        try:
            topic = command.replace('who is', '').replace('what is', '').replace('tell me about', '').strip()
            info = wikipedia.summary(topic, sentences=2)
            talk(info)
        except wikipedia.exceptions.DisambiguationError as e:
            talk("There are multiple results for this. Please be more specific.")
        except wikipedia.exceptions.PageError:
            talk("Sorry, I couldn't find information on that topic.")
    elif 'date' in command:
        talk('Sorry, I have a headache')
    elif 'are you single' in command:
        talk('I am in a relationship with WiFi')
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    else:
        try:
            info = wikipedia.summary(command, sentences=2)
            talk(info)
        except wikipedia.exceptions.DisambiguationError:
            talk("There are multiple results for this. Please be more specific.")
        except wikipedia.exceptions.PageError:
            talk("Sorry, I couldn't find an answer to that.")
        
while True:
    run_alexa()
