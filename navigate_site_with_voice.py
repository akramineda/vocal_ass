import speech_recognition as sr
import webbrowser

import json

def read_site_map(json_file):
    site_map = {}
    try:
        with open(json_file, 'r') as f:
            site_map = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.")
    
    return site_map

# Function to recognize speech input
def get_voice_command():
    r = sr.Recognizer()
    print(sr.Microphone())
    menu_item = None

    with sr.Microphone() as source:
        print("Please say the name of the menu item:")
        audio = r.listen(source)

    try:
        menu_item = r.recognize_google(audio).lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand your voice.")
    except sr.RequestError:
        print("Sorry, I could not request results from Google Speech Recognition service.")

    return menu_item

def open_requested_page(site_map, voice_command):
    if voice_command in site_map:
        url = site_map[voice_command]
        webbrowser.open(url)
        print(f"Opening {url}")
    else:
        print("Requested page not found.")


if __name__ == "__main__":
    # Path to your JSON file containing the site map
    json_file = 'site_map.json'
    
    # Read site map from JSON file
    site_map = read_site_map(json_file)

    # Get voice command from the user
    voice_command = get_voice_command()

    # Open the requested page
    open_requested_page(site_map, voice_command)


# EXample
'''
site_map = {
    "home": "https://www.example.com",
    "about": "https://www.example.com/about",
    "services": "https://www.example.com/services",
    "contact": "https://www.example.com/contact"
}

'''    
