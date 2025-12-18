from flask import Flask, render_template, request, session, redirect, url_for
import os
import time
import requests
from urllib.parse import quote
from PIL import Image, ImageTk
from io import BytesIO
from dotenv import load_dotenv
from get_image import get_random_image_url
from fix_text import fix

app = Flask(__name__)
app.secret_key = os.getenv("appsecretKey")

# ——————————— Home Page ———————————
@app.route("/")
def home():
    return render_template("home.html")

# ——————————— Start: Choose topic → show image ———————————
@app.route("/start", methods=["POST"])
def start():
    topic = request.form["topic"]

    if topic == "random":
        image_url = get_random_image_url()  # no keyword = truly random
    else:
        image_url = get_random_image_url(topic)  # e.g. "airport runways"

    session["current_image"] = image_url
    return render_template("describe.html", image_url=image_url)

# ——————————— Check description ———————————
@app.route("/check", methods=["POST"])
def check():
    user_text = request.form["description"]
    corrected = fix(user_text)
    image_url = session.get("current_image", "")

    return render_template("result.html",
                           image_url=image_url,
                           user_text=user_text,
                           corrected=corrected)

if __name__ == "__main__":
    app.run(debug=True)