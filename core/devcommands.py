import discord
from discord.ext import commands
from discord.ext.commands import command

from core.bot import Bot


class DevCommands(commands.Cog):
    """
    Cog containing all owner-only commands. These are classic commands instead of slash commands, and
    only work for the user that registers and deploys the bot. Besides !activate_guild, these should
    almost never need to be used outside of development.

    Classic command reference:
    https://discordpy.readthedocs.io/en/stable/ext/commands/api.html?highlight=commands#decorators
    """
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name='activate')
    @commands.is_owner()
    async def activate_guild(self, ctx: commands.Context):
        """ Only bot owner can use. Set current guild as bot's active guild and sync app commands. """
        msg = await ctx.send('Activating...')
        self.bot.config.guild_id = ctx.guild.id
        self.bot.update_config()
        await msg.edit(content='Set active guild to this server.')
        await self.sync_app_commands(ctx)


    @command(name='sync')
    @commands.is_owner()
    async def sync_app_commands(self, ctx: commands.Context):
        """ Only bot owner can use. Sync application commands to current guild. """
        msg = await ctx.send('Syncing...')
        synced = await self.bot.tree.sync(guild=ctx.guild)
        await msg.edit(content=f'Synced {len(synced)} app commands.')


    @command(name='get-config')
    @commands.is_owner()
    async def get_config(self, ctx: commands.Context):
        """ Only bot owner can use. Send config.json file for debugging. """
        await ctx.send(file=discord.File(self.bot.configpath))


    @command(name='set-config')
    @commands.is_owner()
    async def set_config(self, ctx: commands.Context):
        """ Only bot owner can use. Overwrite config.json with given file. """
        if not ctx.message.attachments:
            await ctx.send('Missing attachment')
            return
        await ctx.send(content='Old config:', file=discord.File(self.bot.configpath))
        # noinspection PyTypeChecker
        await ctx.message.attachments[0].save(fp=self.bot.configpath)
        self.bot.load_config()
        await ctx.send('Successfully updated config')
