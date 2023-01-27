import requests, os
from flask import Flask, request, Response

app = Flask(__name__)

Token = os.environ['TOKEN']

access_key = os.environ["access_Key"]
per_page = 10

def unsplashApi(query):

    # Make the API request
    response = requests.get(
        f"https://api.unsplash.com/search/photos?query={query}&per_page={per_page}",
        headers={"Authorization": f"Client-ID {access_key}"})

    # Get the JSON data from the response
    data = response.json()
    input_Urls = []
    # Print the URLs of the first 10 results
    for i in range(per_page):
        input_Urls.append(data['results'][i]['urls']['regular'])

    return input_Urls


def imageAsDict(imageURL):
    return {"type": "photo", "media": imageURL}


def sendMediaGroup(chatid, allImages):
    url = f"https://api.telegram.org/bot{Token}/sendMediaGroup"
    media = [imageAsDict(allImages[i]) for i in range(len(allImages))]
    payload = {"chat_id": chatid, "media": media}
    r = requests.post(url, json=payload)
    return r


@app.post("/")
def telegramBot():
    msg = request.get_json()
    chat_id = msg['message']['chat']['id']
    text = msg['message']['text']
    sendMediaGroup(chat_id, unsplashApi(text))
    return Response('ok', status=200)


app.run(host="0.0.0.0")
