import os
from flask import Flask, render_template, url_for, request
# from model.spotify_search_result_item import *
from models.spotifyapi import SpotifyAPI

app = Flask(__name__)


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

        search_type = spotify.get_search_type(query)
        result = spotify.search(query)

        return render_template('searchresult.html', result=result, search_type=search_type, query=query)


if __name__ == '__main__':
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    spotify = SpotifyAPI(client_id, client_secret)
    spotify.perform_auth()
    app.run(debug=True)
