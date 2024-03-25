from flask import Flask, request, jsonify
import json
import webbrowser
import speech_recognition as sr

app = Flask(__name__)
site_map = {}

def read_site_map(json_data):
    try:
        site_map = json.loads(json_data)
        return site_map
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return {}

def get_voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say the path of the page you want to visit:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        print("Sorry, I could not understand your command.")
        return ""
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return ""

def open_requested_page(site_map, voice_command):
    if voice_command in site_map:
        url = site_map[voice_command]
        webbrowser.open(url)
        print(f"Opening {url}")
        return jsonify({"status": "success", "message": f"Opening {url}"})
    else:
        print("Requested page not found.")
        return jsonify({"status": "error", "message": "Requested page not found."})

@app.route('/receive_json', methods=['POST'])
def receive_json():
    global site_map
    json_data = request.get_data(as_text=True)
    site_map = read_site_map(json_data)
    return jsonify({"status": "success", "message": "JSON received successfully"})

@app.route('/get_page', methods=['GET'])
def get_page():
    global site_map
    voice_command = get_voice_command()
    return open_requested_page(site_map, voice_command)

if __name__ == '__main__':
    app.run(debug=True)
