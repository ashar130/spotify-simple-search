import os
from flask import Flask, render_template, url_for, request
# from model.spotify_search_result_item import *
from models.spotifyapi import SpotifyAPI

app = Flask(__name__)

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
spotify = SpotifyAPI(client_id, client_secret)
spotify.perform_auth()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/searchresult", methods=['POST'])
def handle_search():
    if request.method == 'POST':
        query = request.form.to_dict()

    for k, v in query.items():
        v = v.strip()
        if v == '':
            query[k] = None

    result = spotify.search(query)

    name = result[0].name
    return name


if __name__ == '__main__':
    app.run(debug=True)
