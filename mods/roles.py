# This module is to handle roles, via reaction commands
from runbot import creds, db, save_db
from command_tree import add_command, add_reaction_register

from discord.utils import get


async def message_hook(channel_name, message):
    if str(message.author) in creds["discord"]["admins"]:
        #
        print("Role Message Hook")
        reactions = {}

        for line in message.content.split("\n"):
            parts = line.strip().split(" ")
            if (
                len(parts) == 3
                and parts[1] == "for"
                and parts[2].startswith("<")
                and parts[2].endswith(">")
            ):
                role_id = parts[2][3:-1]
                reactions[parts[0]] = role_id

        for key, val in reactions.items():
            await message.add_reaction(key)

        definition = {"hook": "role-message", "roles": reactions}

        db["reaction-hooks"][message.id] = definition
        save_db()


async def reaction_happened(payload, hook, added, client):
    # print(payload)
    if payload.emoji.name in hook["roles"].keys():
        if added:
            role = payload.member.guild.get_role(int(hook["roles"][payload.emoji.name]))
            print("Want to add %s to %s" % (payload.user_id, hook["roles"][payload.emoji.name]))
            print(role)
            await payload.member.add_roles(
                role, reason="Added by Jmons due to a click on a reaction"
            )
            await payload.member.send("You've been given %s" % role.name)
        else:
            # On a remove, you don't have a member, so have to fetch it
            # Note this requires more intents in the client in runbot.py
            guild = await client.fetch_guild(str(payload.guild_id))
            role = guild.get_role(int(hook["roles"][payload.emoji.name]))
            member = await guild.fetch_member(payload.user_id)

            # member = client.get_user(payload.user_id)

            print("Member -> %s" % member)
            print("Role   -> %s" % role)

            print("Want to remove %s from %s" % (payload.user_id, hook["roles"][payload.emoji.name]))

            await member.remove_roles(role, reason="Removed by Jmons due to a click on a reaction")
            await member.send("You've been removed from %s" % role.name)


def initalise():
    add_command("! jmon-role listen", message_hook)
    add_reaction_register("role-message", reaction_happened)
