import requests, os
from flask import Flask, request, Response

app = Flask(__name__)

TOKEN = os.environ["TOKEN"]

# Replace YOUR_ACCESS_KEY with your actual Unsplash API access key
access_key = "YOUR_ACCESS_KEY"

input_Urls=[]

def unsplashApi(query):

  # Make the API request
  response = requests.get(f"https://api.unsplash.com/search/photos?query={query}", headers={
      "Authorization": f"Client-ID {access_key}"
  })

  # Get the JSON data from the response
  data = response.json()

  # Print the URLs of the first 10 results
  for i in range(10):
      input_Urls.push(data['results'][i]['urls']['raw'])
      
  return input_Urls
    
    
import telegram
from telegram import InputMediaPhoto

def telegramImageSender(inputUrls,chat_id):
  bot = telegram.Bot(token='YOUR_BOT_TOKEN')

  image_urls = inputUrls

  media = []
  for url in image_urls:
      media.append(InputMediaPhoto(url))

  bot.send_media_group(chat_id='@mychannel', media=media)

      # Create a list of InputMediaPhoto objects
      media = [InputMediaPhoto(open(image, 'rb')) for image in images]

      # Send the images to the chat
      context.bot.send_media_group(chat_id, media=media)

  # Add the command handler to the dispatcher
  send_images_handler = CommandHandler('send_images', send_images)
  dispatcher.add_handler(send_images_handler)

  # Start the bot
  updater.start_polling()
  updater.idle()



@app.post("/")
def telegramBot():
    msg = request.get_json()
    chat_id = msg['message']['chat']['id']
    text = msg['message']['text']
    telegramImageSender(unsplashApi(text), chat_id)
    return Response('ok', status=200)


app.run(host="0.0.0.0")
