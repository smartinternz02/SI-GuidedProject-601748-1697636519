from flask import Flask, render_template, request
import joblib
import webbrowser
import keyboard

app = Flask(__name__)

# Load the model
rf_model = joblib.load("model_rf_new.pkl")

# Function to open the default web browser
def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000')

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/carprediction")
def carprediction():
    return render_template("carprediction.html")

@app.route("/predict", methods=["POST"])
def predict():
    gender_str = str(request.form.get("gender"))
    if gender_str.lower() == "male":
        gender = 0
    else:
        gender = 1
    age = int(request.form.get("age"))
    annual_salary = int(request.form.get("annualSalary"))
    age_salary_interact = age * annual_salary
    prediction = rf_model.predict([[gender, age, annual_salary, age_salary_interact]])
    return render_template("carprediction.html", prediction=prediction)

if __name__ == "__main__":
    open_browser()
    app.run(host='127.0.0.1', port=5000, debug=True)

def detect_q_key(event):
    if event.event_type == keyboard.KEY_DOWN and event.name == 'q':
        print("Terminating the server...")
        keyboard.unhook_all()  # Unhook all keyboard events
        exit()  # Terminate the serverq

# Hook the "q" key event
keyboard.hook(detect_q_key)