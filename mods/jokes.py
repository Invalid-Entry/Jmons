# This is a joke generator class as per the christmas advent video
# https://youtu.be/7caCXRLmUJw

import random
from runbot import creds, db, save_db
from command_tree import add_command


class JokeFinished(Exception):
    pass


class JokeEngine:

    corpus = None

    def load_corpus(self, filename):
        with open(filename) as f:
            self.corpus = f.read()

    def _choose_char(self, target, target_length):
        options = []
        corp_length = len(self.corpus)

        index = 0
        try:
            while index < corp_length:
                index = self.corpus.index(target, index) + target_length
                if index < corp_length:
                    options.append(self.corpus[index])

        except ValueError:
            pass

        if len(options) > 0:
            choice = random.choice(options)
        else:
            raise JokeFinished()

        if choice == "\n":
            raise JokeFinished()
        else:
            return choice

    def generate_joke(self, text, target_length=5, max_len=150):

        try:
            while max_len > 0:
                max_len -= 1

                x = text[-target_length:]
                next_char = self._choose_char(x, target_length)
                text += next_char

        except JokeFinished:
            pass

        return text


async def enable_jokes(channel_name, message):
    if str(message.author) in creds["discord"]["admins"]:

        if channel_name not in db["jokes"]["enabled_channels"]:
            db["jokes"]["enabled_channels"].append(channel_name)
            save_db()
            await message.channel.send("Jokes Enabled. ho ho ho")
        else:
            await message.channel.send("Jokes are already enabled? Aren't you having fun?")


async def disable_jokes(channel_name, message):
    if str(message.author) in creds["discord"]["admins"]:
        if channel_name in db["jokes"]["enabled_channels"]:
            db["jokes"]["enabled_channels"].remove(channel_name)
            save_db()
            await message.channel.send("Jokes Disabled. </humor>")
        else:
            await message.channel.send(
                "Jokes are already disabled? Is there a problem - see Dansan!"
            )


async def joke(channel_name, message):

    if channel_name in db["jokes"]["enabled_channels"]:
        joke = je.generate_joke("What ")
        await message.channel.send(joke)


je = JokeEngine()

# Now register.
def initalise():
    je.load_corpus("assets/christmas_jokes.txt")

    add_command("^! enable jokes$", enable_jokes)
    add_command("^! disable jokes$", disable_jokes)
    add_command("^! make me laugh$", joke)
