import os
import discord
from datetime import datetime
from dotenv import load_dotenv

from core.bot import Bot
from core.slashcommands import SlashCommands
from core.devcommands import DevCommands
from core.listeners import Listeners


def main():
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    CONFIGPATH = os.path.join(os.path.dirname(__file__), os.getenv('CONFIGPATH'))

    bot = Bot(
        CONFIGPATH,
        command_prefix='!',
        intents=discord.Intents.all(),
        help_command=None
    )

    @bot.event
    async def on_ready():
        bot.load_config()
        await bot.add_cog(DevCommands(bot))
        await bot.add_cog(SlashCommands(bot))
        await bot.add_cog(Listeners(bot))
        print(f'Connected: {datetime.now().strftime("%m/%d/%Y %H:%M:%S")}')

    bot.run(TOKEN)


if __name__ == '__main__':
    main()
