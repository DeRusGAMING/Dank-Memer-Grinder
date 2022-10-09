import threading
import json

from discord.ext import commands

search_priority = [
    "phoenix pits",
    "aeradella's home",
    "soul's chamber",
    "god's own place",
    "dog",
    "grass",
    "air",
    "kitchen",
]
second_search_priority = ["who asked", "fridge"]
search_avoid = ["area51", "bank"]


def update():
    global config_dict
    threading.Timer(1, update).start()
    with open("config.json", "r") as config_file:
        config_dict = json.load(config_file)


update()


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            message.channel.id != self.bot.channel_id
            or config_dict[self.bot.account_id]["state"] is False
            or config_dict[self.bot.account_id]["commands"]["search"] is False
        ):
            return

        for embed in message.embeds:
            try:
                if "to search?" in embed.to_dict()["description"]:
                    for count, i in enumerate(message.components[0].children):
                        if i.label in search_priority:
                            await self.bot.click(message, 0, count)
                            return
                    for count, i in enumerate(message.components[0].children):
                        if i.label in second_search_priority:
                            await self.bot.click(message, 0, count)
                            return
                    for count, i in enumerate(message.components[0].children):
                        if i.label not in search_avoid:
                            await self.bot.click(message, 0, count)
                            return
            except KeyError:
                pass


async def setup(bot):
    await bot.add_cog(Search(bot))
