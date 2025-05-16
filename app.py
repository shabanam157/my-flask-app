from flask import Flask, render_template, request, jsonify
import datetime
import webbrowser
import wikipedia
import os

try:
    import pyttsx3  # For text-to-speech
except ImportError:
    print("Please ensure pyttsx3 is installed and accessible.")

app = Flask(__name__)

def speak(audio):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 175)
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        return "Good Morning!"
    elif 12 <= hour < 18:
        return "Good Afternoon!"
    else:
        return "Good Evening!"

@app.route('/')
def home():
    """Render the main page."""
    greeting = wishMe()
    return render_template("index.html", greeting=greeting)

@app.route('/process', methods=['POST'])
def process():
    """Process POST requests (text or voice)."""
    query = request.form['query'].lower()

    if 'exit' in query or 'quit' in query or 'goodbye' in query:
        message = "Goodbye! Have a great day!"
        speak(message)
        return jsonify({'response': message, 'exit': True})

    elif 'wikipedia' in query:
        try:
            search_term = query.replace("wikipedia", "").strip()
            results = wikipedia.summary(search_term, sentences=2)
            return jsonify({'response': f"According to Wikipedia: {results}"})
        except Exception as e:
            return jsonify({'response': "Sorry, I couldn't find anything on Wikipedia."})

    elif 'open youtube' in query:
        webbrowser.open("https://youtube.com")
        return jsonify({'response': "Opening YouTube in your browser."})

    elif 'the time' in query:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return jsonify({'response': f"The time is {current_time}."})

    else:
        return jsonify({'response': "Sorry, I couldn't understand your command."})

if __name__ == "__main__":
    app.run(debug=True)