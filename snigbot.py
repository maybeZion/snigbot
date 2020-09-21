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

if __name__ == '__main__':
	bot.run('token')
