#!/usr/bin/env python3

import json

import yt_dlp
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form["video_url"]
        thumbnail_urls = get_thumbnail_urls(video_url)
        return render_template("index.html", thumbnail_urls=thumbnail_urls)
    # else:
    return render_template("index.html")


def get_thumbnail_urls(video_url):
    ydl = yt_dlp.YoutubeDL()
    info = ydl.extract_info(video_url, download=False)
    json_data = json.dumps(info)
    data = json.loads(json_data)
    save_json_data(data)
    all_thumbnails = data["thumbnails"]
    thumbnails_with_size = []
    for tn in all_thumbnails:
        if "resolution" in tn.keys():
            if tn["resolution"] in ["1920x1080", "1280x720", "640x480", "320x180"]:
                thumbnails_with_size.append([tn["url"], tn["width"] * tn["height"]])
    thumbnails_with_size.sort(reverse=True, key=lambda x: x[1])
    thumbnails_to_show = [i[0] for i in thumbnails_with_size]
    return thumbnails_to_show


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
