from discord.ext import commands


class Create(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Create(bot))
