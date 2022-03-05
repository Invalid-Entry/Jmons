import discord
import json

from os.path import dirname, basename, isfile, join
from importlib import import_module
import glob

from command_tree import add_command, print_commands, find_command

client = discord.Client()

with open("creds.json") as f:
    creds = json.load(f)


######
# FIXME: replace this with tinydb ?

with open("assets/db.json") as f:
    db = json.load(f)


def save_db():
    with open("assets/db.json", "w") as f:
        json.dump(db, f)


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
    if message.content.startswith("!"):
        command = find_command(message.content)
        await command(channel_name, message)


# Main functions

if __name__ == "__main__":
    print("Importing modules dynamically")

    modules = glob.glob(join(dirname(__file__), "mods", "*.py"))

    for f in modules:
        if isfile(f) and not f.endswith("__init__.py"):
            print("   %s ... " % basename(f)[:-3], end="")
            module = import_module("mods." + basename(f)[:-3])
            module.initalise()
            print(" [OK]")

    print("Commands loaded:")
    print_commands()

    client.run(creds["discord"]["token"])
