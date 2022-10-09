import json
import sys
import os
import random
import re
import threading

from discord.ext import commands


def update():
    global config_dict
    threading.Timer(1, update).start()
    with open("config.json", "r") as config_file:
        config_dict = json.load(config_file)


update()


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        # noinspection PyProtectedMember
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


with open(resource_path("resources/trivia.json")) as file:
    trivia_dict = json.load(file)


class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chance = config_dict[self.bot.account_id]["trivia_correct_chance"]

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            message.channel.id != self.bot.channel_id
            or config_dict[self.bot.account_id]["state"] is False
            or config_dict[self.bot.account_id]["commands"]["trivia"] is False
        ):
            return

        for embed in message.embeds:
            try:
                if embed.to_dict()["fields"][0]["name"] == "Difficulty":
                    category = embed.to_dict()["fields"][1]["value"][1:-1]
                    question = re.search(
                        "\*\*(.*?)\*\*", embed.to_dict()["description"]
                    ).group(1)
                    try:
                        answer = trivia_dict[category][question]
                    except:
                        await self.bot.click(message, 0, 0)
                        return
                    if random.random() <= self.chance:
                        if message.components[0].children[0].label == answer:
                            await self.bot.click(message, 0, 0)
                        elif message.components[0].children[1].label == answer:
                            await self.bot.click(message, 0, 1)
                        elif message.components[0].children[2].label == answer:
                            await self.bot.click(message, 0, 2)
                        elif message.components[0].children[3].label == answer:
                            await self.bot.click(message, 0, 3)
                    else:
                        if message.components[0].children[0].label != answer:
                            await self.bot.click(message, 0, 0)
                        else:
                            await self.bot.click(message, 0, 1)
            except KeyError:
                pass


async def setup(bot):
    await bot.add_cog(Trivia(bot))
