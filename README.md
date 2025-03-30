# 🎤 Voice Assistant with Wake Word Activation

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Speech Recognition](https://img.shields.io/badge/SpeechRecognition-Latest-green)
![pyttsx3](https://img.shields.io/badge/pyttsx3-Latest-orange)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

A modular voice assistant application that responds to spoken commands after being activated with a customisable wake word. This project demonstrates object-oriented programming in Python, speech recognition, and text-to-speech capabilities.

## 📋 Table of Contents
- [Features](#-features)
- [Technologies Used](#-technologies-used)
- [System Architecture](#%EF%B8%8F-system-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Command Examples](#-command-examples)
- [Future Improvements](#-future-improvements)
- [License](#-license)

## ✨ Features

- **Wake Word Activation**: Assistant only responds after hearing a customisable wake phrase
- **Speech Recognition**: Converts spoken commands to text for processing
- **Text-to-Speech**: Provides audible responses using the pyttsx3 engine
- **Wikipedia Integration**: Searches and summarises Wikipedia articles
- **Web Search**: Opens Google searches in the default browser
- **Time and Date**: Provides current time and date information
- **Entertainment**: Tells jokes and inspirational quotes
- **Extensible Design**: Easily add new commands and capabilities
- **Configurable Settings**: Adjust timeout, voice, and other parameters
- **Command Logging**: Optional logging of commands for analysis

## 🔧 Technologies Used

- **Python 3.7+**: Core programming language
- **SpeechRecognition**: Library for converting speech to text
- **pyttsx3**: Text-to-speech conversion engine
- **Wikipedia API**: For retrieving article summaries
- **webbrowser**: For opening web searches
- **JSON**: For configuration storage and retrieval

## 🏗️ System Architecture

The voice assistant follows an object-oriented architecture with these key components:

- **VoiceAssistant Class**: Main class handling all functionality
- **Speech Recognition Module**: Handles wake word detection and command input
- **Text-to-Speech Engine**: Converts responses to spoken audio
- **Command Processor**: Routes commands to appropriate handlers
- **Configuration Management**: Handles settings and response templates

## 📥 Installation

1. Clone this repository:
```
git clone https://github.com/husskhosravi/voice-assistant-python.git
cd voice-assistant
```

2. Install required dependencies:
```
pip install SpeechRecognition pyttsx3 wikipedia pyaudio
```

3. (Optional) Create configuration files:
```
# assistant_config.json and assistant_responses.json
# Will be created automatically if not present
```

## 🚀 Usage

Run the assistant using Python:
```
python voice-assistant-code.py
```

The assistant will start listening for the wake word (default: "hey assistant"). After the wake word is detected, you can issue commands. The assistant will automatically time out after a period of inactivity.

### Customisation Options

You can customise the assistant by modifying these parameters in the code:

```python
assistant = VoiceAssistant(
    wake_word="hey assistant",  # Change to your preferred wake phrase
    timeout=60,                 # Seconds before timing out
    voice_index=None            # Set to an integer to change voice
)
```

## 💬 Command Examples

After saying the wake word, try these commands:

- "What time is it?"
- "What's today's date?"
- "Search for Python programming tutorials"
- "Tell me a joke"
- "Give me a quote"
- "Wikipedia artificial intelligence"
- "How are you?"
- "Change wake word"
- "Sleep" or "Exit" (to deactivate)

## 🔮 Future Improvements

- Add more advanced natural language processing
- Implement smart home device control
- Add weather information retrieval
- Create a GUI for easier configuration
- Add multi-language support
- Implement custom skills via plugins

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
