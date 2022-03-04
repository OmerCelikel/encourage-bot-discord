import discord
import json
# api json http 
import requests
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "miserable", "depressing", ":("]

starter_encouragements = [
  "Cheer up!",
  "Hang in there",
  "You are a great person!"
]

welcomeText = [
  "Hello :)",
  "Hi :D",
  "Heey :D",
  "Welcome :)",
  "Hey there :)"
]

welcomeTextPerson = [
  "Hello",
  "Hi",
  "Heey",
  "hello",
  "hi",
  "heey",
]

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements
  
  return
# inspiration quotes
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]["q"] + " -" + json_data[0]["a"]
  return (quote) 

db["key"] = "value"
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

#interaction with the bot
@client.event 
async def on_message(message):
  msg = message.content
  if message.author == client.user:
    return
  if any(word in msg for word in welcomeTextPerson):
    await message.channel.send(random.choice(welcomeText))
  if message.content.startswith("$inspire"):
    quote = get_quote()
    await message.channel.send(quote)
  
  options = starter_encouragements
  
  if "encouragements" in db.keys():
    options = options + list(db["encouragements"])
    print(options)
    
  if any(word in msg for word in sad_words):
    #await message.channel.send(random.choice(starter_encouragements))  
    await message.channel.send(random.choice(options)) 
  if msg.startswith("new"):
    print("new list will added")
    encouraging_message = msg.split("new",1)[1]
    print("encouraging_message = ",encouraging_message)

    update_encouragements(encouraging_message)
    await message.channel.send("New enc message added.")

  if msg.startswith("del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
      
"""  else:
    await message.channel.send("Anlamadım?")
"""

keep_alive()
client.run("your TOKEN must be in there")
