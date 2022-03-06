import discord
import json

from os.path import dirname, basename, isfile, join
from importlib import import_module
import glob

from command_tree import print_commands, find_command, find_reaction

# FIXME: all might be a bit dramatic, but need it for members.
# intents = discord.Intents(messages=True,members = True, reactions=True)
client = discord.Client(intents=discord.Intents.all())

with open("creds.json") as f:
    creds = json.load(f)


######
# FIXME: replace this with tinydb ?

with open("assets/db.json") as f:
    db = json.load(f)


def save_db():
    with open("assets/db.json", "w") as f:
        json.dump(db, f, indent=2)


##########################################################
# Discord Bot Interface


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel_name = "%s:%s" % (str(message.guild), str(message.channel))

    # FIXME: added this as a fast filter to reduce load on chatter
    # if message.content.startswith("!"):
    command = find_command(message.content)
    if command:
        await command(channel_name, message)
    else:
        pass
        # print ("Didnt match command")
        # print(message.content)


@client.event
async def on_raw_reaction_add(payload):
    print(payload)
    print(client.user.id)
    if not str(payload.user_id) == str(client.user.id):
        # print(type(payload.message_id))
        # print(db['reaction-hooks'].keys())
        if str(payload.message_id) in db["reaction-hooks"].keys():
            hook = db["reaction-hooks"][str(payload.message_id)]
            func = find_reaction(hook["hook"])
            await func(payload, hook, True, client)


@client.event
async def on_raw_reaction_remove(payload):
    # print(payload)
    # print(client.user.id)
    if not str(payload.user_id) == str(client.user.id):
        # print(type(payload.message_id))
        # print(db['reaction-hooks'].keys())
        if str(payload.message_id) in db["reaction-hooks"].keys():
            hook = db["reaction-hooks"][str(payload.message_id)]
            func = find_reaction(hook["hook"])
            await func(payload, hook, False, client)


# Main functions

if __name__ == "__main__":
    print(
        """
      _ __  __  ___  _   _ ____    ____   ___ _____ 
     | |  \/  |/ _ \| \ | / ___|  | __ ) / _ \_   _|
  _  | | |\/| | | | |  \| \___ \  |  _ \| | | || |  
 | |_| | |  | | |_| | |\  |___) | | |_) | |_| || |  
  \___/|_|  |_|\___/|_| \_|____/  |____/ \___/ |_|  
                                                    """
    )

    print("Importing modules dynamically")

    modules = glob.glob(join(dirname(__file__), "mods", "*.py"))

    for f in modules:
        if isfile(f) and not f.endswith("__init__.py"):
            print("   %s ... " % basename(f)[:-3], end="")
            module = import_module("mods." + basename(f)[:-3])
            module.initalise()
            print(" [OK]")

    print("")

    print("Commands loaded:")
    print_commands()
    print("\r\nRuntime:")

    client.run(creds["discord"]["token"])
