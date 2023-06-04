#!/usr/bin/env python3

import json

import requests
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form["video_url"]
        thumbnail_urls = get_thumbnail_urls(video_url)
        return render_template("index.html", thumbnail_urls=thumbnail_urls)
    return render_template("index.html")


def get_thumbnail_urls(video_url):
    video_id = extract_video_id(video_url)
    if video_id:
        api_url = f"https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v={video_id}&format=json"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = json.loads(response.text)
            save_json_data(data)
            thumbnail_urls = [data["thumbnail_url"]]
            return thumbnail_urls
    return None


def save_json_data(data):
    with open("youtube_data.json", "w") as file:
        json.dump(data, file)


def extract_video_id(video_url):
    video_id = None
    if "youtube.com" in video_url:
        video_id = video_url.split("v=")[1]
    elif "youtu.be" in video_url:
        video_id = video_url.split("/")[-1]
    return video_id


if __name__ == "__main__":
    app.run()
