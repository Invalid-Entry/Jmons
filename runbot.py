import discord
import json


from jokes import JokeEngine

client = discord.Client()

with open("creds.json") as f:
    creds = json.load(f)

with open("assets/db.json") as f:
    db = json.load(f)


def save_db():
    with open("assets/db.json", "w") as f:
        json.dump(db,f)

# Discord Bot Interface

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel_name = "%s:%s" % (str(message.guild), str(message.channel))

    if str(message.author) in creds['discord']['admins']:
        if message.content.startswith("! enable jokes"):
            if channel_name not in db['jokes']['enabled_channels']:
                db['jokes']['enabled_channels'].append(channel_name)
                save_db()
                await message.channel.send("Jokes Enabled. ho ho ho")
            else:
                await message.channel.send("Jokes are already enabled? Aren't you having fun?")
            
        if message.content.startswith("! disable jokes"):
            if channel_name in db['jokes']['enabled_channels']:
                db['jokes']['enabled_channels'].remove(channel_name)
                save_db()
                await message.channel.send("Jokes Disabled. </humor>")
            else:
                await message.channel.send("Jokes are already disabled? Is there a problem - see Dansan!")
             

    # big if statement
    if channel_name in db['jokes']['enabled_channels'] and message.content.startswith('! make me laugh'):
        joke = je.generate_joke("What ")
        await message.channel.send(joke)

# Main functions

je = JokeEngine()
je.load_corpus("assets/christmas_jokes.txt")

client.run(creds['discord']['token'])