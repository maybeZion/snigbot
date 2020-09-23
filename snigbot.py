import discord
from discord.ext import commands
import json
import jsonpickle

def save(_input, _file):
    with open(_file, 'w', encoding='utf-8') as f:
        try:
            json.dump(_input, f, ensure_ascii=False, indent=4)
        except TypeError:
            json.dump(jsonpickle.encode(_input), f, ensure_ascii=False, indent=4)
        print('Saved data to {}'.format(_file))

def load(_output, _file, decode=False):
    try:
        with open(_file, 'r', encoding='utf-8') as f:
            if decode:
                return jsonpickle.decode(json.load(f))
            else:
                return json.load(f)
            print('loaded data from {}'.format(f))
    except FileNotFoundError:
        print('File "{}" not found.'.format(_file))

bot = commands.Bot(command_prefix='snig')

snigboard_setting = None
snigboard_setting = load(snigboard_setting, 'snigboard_setting')

snigged_messages = {}
snigged_messages = load(snigged_messages, 'snigged_messages')

@bot.event
async def on_ready():
    print('Logged in.\n----------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="snig help"))

@bot.event
async def on_reaction_add(payload):
	snigboard = bot.fetch_channel(snigboard_setting)
	message = bot.fetch_message(payload.message_id)
	if message not in snigged_messages:
		for reaction in message.reactions:
			if reaction.emoji.name == 'snig' and reaction.count == 5:
				try:
					snigboard.send('message snigged')
				except discord.NotFound:
					return
				snigged_messages[message.name] = True

def has_role(user, role):
    for item in user.roles:
        if item.name = role:
            return True
    return False

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def board(self, ctx, snigboard_channel):
        """Sets which channel to post snigboard content to. Pass 'disable' as the channel name to disable this feature."""
        if has_role(ctx.message.author, 'Moderator'):
            if snigboard_channel == 'disable':
                snigboard_setting = None
                save(snigboard_setting)
                await ctx.send('Snigboard disabled.')
            for channel in ctx.guild.channels:
                if channel.name == snigboard_channel:
                    snigboard_setting = channel
                    save(snigboard_setting)
                    await ctx.send('Snigboard channel updated.')
                    return
            await ctx.send('Unrecognized channel.')
        else:
            await ctx.send('Missing permissions.')

if __name__ == '__main__':
    bot.add_cog(Commands(bot))
    bot.run('token')
