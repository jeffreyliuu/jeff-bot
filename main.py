import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

db["cringe"] = 0

starter_encouragements = [
  "NO",
  "Hang in there lil man",
  "You are a great person!",
  "heehee",
  "F"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements

def update_triggers(trigger_message):
  if "triggers" in db.keys():
    triggers = db["triggers"]
    triggers.append(trigger_message)
    db["triggers"] = triggers
  else:
    db["triggers"] = [trigger_message]

def delete_trigger(index):
  triggers = db["triggers"]
  if len(triggers) > index:
    del triggers[index]
  db["triggers"] = triggers



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content
  
    if message.content.startswith('j!inspire'):
      quote = get_quote()
      await message.channel.send(quote)

    if db["responding"]:
      if "triggers" in db.keys():
        sad_stuff = db["triggers"]

      if "encouragements" in db.keys():
        options = db["encouragements"]

    
    if any(word in msg.lower() for word in sad_stuff):
      await message.channel.send(random.choice(options))  

    if msg.startswith("j!new"): 
      second = msg.split("j!new ", 1)[1]
      types = second.split(" ", 1)
      if(types[0] == "message"):
        update_encouragements(types[1])
        await message.channel.send("New message added.")
      elif(types[0] == "trigger"):
        update_triggers(types[1])
        await message.channel.send("New trigger added.")
      

    if msg.startswith("j!del"):
      second = msg.split("j!del ", 1)[1]
      types = second.split()
      if(types[0] == "message"):
        encouragements = []
        if "encouragements" in db.keys():
          index = int(types[1]) - 1
          encouragements = db["encouragements"]
          deleted_word = encouragements[index]
          delete_encouragement(index)
          encouragements = db["encouragements"]
          await message.channel.send("Deleted: " + deleted_word)
      elif(types[0] == "trigger"): 
        if "triggers" in db.keys():
          index = int(types[1]) - 1
          triggers = db["triggers"]
          deleted_word = triggers[index]
          delete_trigger(index)
          triggers = db["triggers"]
          await message.channel.send("Deleted: " + deleted_word)
    
    if msg.startswith("j!messages"):
      encouragements = []
      if "encouragements" in db.keys():
        encouragements = db["encouragements"]
      if(len(encouragements) == 0):
        await message.channel.send("empty")
      else:
        messages = ""
        for i in range(len(encouragements)):
          messages += str(i + 1) + ". " + encouragements[i] + "\n"
        
        await message.channel.send(messages)
    
    if msg.startswith("j!triggers"):
      triggers = []
      if "triggers" in db.keys():
        triggers = db["triggers"]
      if(len(triggers) == 0):
        await message.channel.send("empty")
      else:
        messages = ""
        for i in range(len(triggers)):
          messages += str(i + 1) + ". " + triggers[i] + "\n"
        
        await message.channel.send(messages)   
        
    if msg.startswith("j!responding"):
      value = msg.split("j!responding ",1)[1]

      if value.lower() == "on":
        db["responding"] = True
        await message.channel.send("Responding is on.")
      else:
        db["responding"] = False
        await message.channel.send("Responding is off.")

    if msg.startswith("j!flip"):
      await message.channel.send(random.choice(["heads", "tails"]))
    
    if msg.startswith("j!choose"):
      second = msg.split("j!choose ", 1)[1]
      msgs = second.split(" or ")
        
      await message.channel.send(random.choice(msgs))

    if msg.startswith("j!rng"):
      await message.channel.send(random.randint(1, 10))

    if msg.startswith("j!cringe"):
      words = msg.split()
      if(len(words) == 1):
          db["cringe"] = db["cringe"] + 1
          cringe_counter = db["cringe"]
          message1 = "You have cringed " + str(cringe_counter)
          if(cringe_counter == 1):
            message1 += " time."
          else:
            message1 += " times."
          await message.channel.send(message1)

      elif(words[1] == "clear") :
        if "cringe" in db.keys():
          db["cringe"] = 0
        await message.channel.send("Cringes cleared.")
    

    

  

keep_alive()
client.run(os.getenv('TOKEN'))
