"""
Advanced Voice Assistant with Wake Word Activation

This script implements a modular voice assistant that responds to various commands
and is activated by a customisable wake word. The assistant can perform tasks such as:
- Searching Wikipedia
- Telling the time and date
- Opening web searches
- Telling jokes and quotes
- Answering simple questions

"""

import speech_recognition as sr
import pyttsx3
import wikipedia
import datetime
import webbrowser
import random
import time
import json
import os

class VoiceAssistant:
    """
    A voice assistant class that handles speech recognition, text-to-speech,
    and various commands through a modular, wake-word activated system.
    """
    
    def __init__(self, wake_word="hey assistant", timeout=60, voice_index=None):
        """
        Initialize the voice assistant with customisable settings.
        
        Args:
            wake_word (str): The phrase that activates the assistant
            timeout (int): Number of seconds to listen for a command before timing out
            voice_index (int, optional): Index of the voice to use (None for default)
        """
        # Initialize speech recognition components
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1)
        
        # Configure voice if specified
        if voice_index is not None:
            voices = self.engine.getProperty('voices')
            if 0 <= voice_index < len(voices):
                self.engine.setProperty('voice', voices[voice_index].id)
        
        # Set wake word and parameters
        self.wake_word = wake_word.lower()
        self.timeout = timeout
        self.is_active = False
        self.last_activation_time = 0
        
        # Load config and response data
        self.config = self._load_config()
        self.responses = self._load_responses()
    
    def _load_config(self):
        """
        Load configuration settings from a file or use defaults.
        
        Returns:
            dict: Configuration dictionary
        """
        try:
            with open('assistant_config.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Default configuration
            return {
                "language": "en-US",
                "log_commands": True,
                "max_wikipedia_sentences": 2
            }
    
    def _load_responses(self):
        """
        Load response templates for various interactions.
        
        Returns:
            dict: Dictionary of response types and their templates
        """
        try:
            with open('assistant_responses.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Default responses
            return {
                "greetings": [
                    "I'm doing well, thank you!",
                    "I'm just a program, but thanks for asking!",
                    "Doing great! How about you?"
                ],
                "jokes": [
                    "Why do programmers prefer dark mode? Because light attracts bugs!",
                    "I told my computer I needed a break, and now it won't stop sending me vacation ads.",
                    "What's a computer's favorite snack? Microchips!",
                    "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
                    "Why was the JavaScript developer sad? Because he didn't know how to Object.create(happiness);"
                ],
                "quotes": [
                    "The greatest glory in living lies not in never falling, but in rising every time we fall.",
                    "The way to get started is to quit talking and begin doing.",
                    "Your time is limited, so don't waste it living someone else's life.",
                    "If life were predictable it would cease to be life, and be without flavor.",
                    "Spread love everywhere you go. Let no one ever come to you without leaving happier.",
                    "When you reach the end of your rope, tie a knot in it and hang on."
                ],
                "preferences": [
                    "I enjoy helping you with your questions.",
                    "I love learning new things from you.",
                    "I like to keep you entertained!"
                ],
                "unknown_command": [
                    "I'm sorry, I can't perform that command.",
                    "I don't understand that instruction.",
                    "That's beyond my capabilities right now."
                ]
            }
    
    def speak(self, text):
        """
        Convert text to speech.
        
        Args:
            text (str): The text to be spoken
        """
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen_for_wake_word(self):
        """
        Continuously listen for the wake word.
        
        Returns:
            bool: True if wake word detected, False on error
        """
        print("Listening for wake word...")
        
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                try:
                    text = self.recognizer.recognize_google(audio, language=self.config["language"])
                    text = text.lower()
                    print(f"Heard: {text}")
                    
                    if self.wake_word in text:
                        print("Wake word detected!")
                        return True
                except sr.UnknownValueError:
                    # Speech not understood - continue listening
                    pass
                except sr.RequestError:
                    print("Speech recognition service unavailable")
                    return False
                
                # Check for timeout
                if self.is_active and time.time() - self.last_activation_time > self.timeout:
                    print("Session timed out")
                    self.is_active = False
                    self.speak("Timing out due to inactivity.")
                
                return False
            except sr.WaitTimeoutError:
                # Timeout occurred during listening - continue
                return False
    
    def listen_for_command(self):
        """
        Listen for a command after wake word is detected.
        
        Returns:
            str: The recognized command or empty string on error
        """
        self.speak("How can I help you?")
        print("Listening for command...")
        
        with self.mic as source:
            try:
                audio = self.recognizer.listen(source, timeout=5)
                try:
                    query = self.recognizer.recognize_google(audio, language=self.config["language"])
                    query = query.lower()
                    print(f"Command: {query}")
                    return query
                except sr.UnknownValueError:
                    self.speak("Sorry, I could not understand that.")
                    return ""
                except sr.RequestError:
                    self.speak("Sorry, there was an error with the speech recognition service.")
                    return ""
            except sr.WaitTimeoutError:
                self.speak("I didn't hear a command.")
                return ""
    
    def process_command(self, query):
        """
        Process and execute the given command.
        
        Args:
            query (str): The command to process
        
        Returns:
            bool: True to continue, False to exit
        """
        self.last_activation_time = time.time()
        
        # Log command if enabled
        if self.config["log_commands"]:
            self._log_command(query)
        
        # Process commands
        if "exit" in query or "goodbye" in query or "bye" in query:
            self.speak("Goodbye!")
            self.is_active = False
            return True
        
        elif "sleep" in query or "deactivate" in query:
            self.speak("Going to sleep. Say the wake word to activate me again.")
            self.is_active = False
            return True
        
        elif "wikipedia" in query:
            self.speak("What would you like to search on Wikipedia?")
            topic = self.listen_for_command()
            if topic:
                self._search_wikipedia(topic)
            return True
        
        elif "time" in query:
            self._tell_time()
            return True
        
        elif "date" in query:
            self._tell_date()
            return True
        
        elif "how are you" in query:
            self.speak(random.choice(self.responses["greetings"]))
            return True
        
        elif "what is your name" in query or "who are you" in query:
            self.speak("I am your voice assistant, activated by saying the wake word.")
            return True
        
        elif "search" in query:
            self.speak("What do you want to search for on Google?")
            search_query = self.listen_for_command()
            if search_query:
                self._web_search(search_query)
            return True
        
        elif "tell me a joke" in query or "joke" in query:
            self.speak(random.choice(self.responses["jokes"]))
            return True
        
        elif "give me a quote" in query or "quote" in query:
            self.speak(random.choice(self.responses["quotes"]))
            return True
        
        elif "what do you like to do" in query or "your hobbies" in query:
            self.speak(random.choice(self.responses["preferences"]))
            return True
        
        elif "change wake word" in query:
            self._change_wake_word()
            return True
        
        else:
            self.speak(random.choice(self.responses["unknown_command"]))
            return True
    
    def _search_wikipedia(self, topic):
        """
        Search for a topic on Wikipedia and speak the summary.
        
        Args:
            topic (str): The topic to search for
        """
        try:
            summary = wikipedia.summary(
                topic, 
                sentences=self.config["max_wikipedia_sentences"]
            )
            self.speak(summary)
        except wikipedia.exceptions.DisambiguationError:
            self.speak("The topic is ambiguous, please be more specific.")
        except wikipedia.exceptions.PageError:
            self.speak("Unfortunately, there is no page with that title.")
        except Exception:
            self.speak("Sorry, something went wrong with the Wikipedia search.")
    
    def _tell_time(self):
        """Tell the current time."""
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        self.speak(f"The current time is {current_time}.")
    
    def _tell_date(self):
        """Tell today's date."""
        today = datetime.date.today()
        self.speak(f"Today's date is {today}.")
    
    def _web_search(self, query):
        """
        Perform a web search.
        
        Args:
            query (str): The search query
        """
        self.speak(f"Searching for {query} on Google.")
        webbrowser.open(f"https://www.google.com/search?q={query}")
        self.speak("Here are the search results.")
    
    def _change_wake_word(self):
        """Allow the user to change the wake word."""
        self.speak("What would you like to set as the new wake word?")
        new_wake_word = self.listen_for_command()
        if new_wake_word:
            self.wake_word = new_wake_word.lower()
            self.speak(f"Wake word changed to {new_wake_word}")
    
    def _log_command(self, command):
        """
        Log commands to a file for analysis.
        
        Args:
            command (str): The command to log
        """
        try:
            with open('command_log.txt', 'a') as f:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"{timestamp}: {command}\n")
        except Exception:
            # Silently fail if logging isn't possible
            pass
    
    def run(self):
        """
        Main method to run the voice assistant.
        """
        self.speak(f"Voice assistant initialized. Say '{self.wake_word}' to activate me.")
        
        try:
            while True:
                # Check for wake word if not active
                if not self.is_active:
                    if self.listen_for_wake_word():
                        self.is_active = True
                        self.last_activation_time = time.time()
                
                # Process commands when active
                if self.is_active:
                    command = self.listen_for_command()
                    if command:
                        self.process_command(command)
                
                # Small pause to prevent high CPU usage
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("Program terminated by user")
            self.speak("Goodbye!")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.speak("I encountered an error and need to shut down.")


def main():
    """
    Main function to set up and run the voice assistant.
    """
    # Create the assistant with default settings
    # Customize these parameters as needed
    assistant = VoiceAssistant(
        wake_word="hey assistant",
        timeout=60,  # Timeout after 60 seconds of inactivity
        voice_index=None  # Use default voice
    )
    
    # Run the assistant
    assistant.run()


if __name__ == "__main__":
    main()
