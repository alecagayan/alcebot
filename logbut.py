import os
import discord

#important Variables Do Not Touch
client = discord.Client()
BotID = "NjY4OTY4OTE3OTIxODI0Nzk1.XiZSjg.QSr1d--d9PVptehJira10Rnlx3M" #string
currentChannels = {1:1}

#values to modify according to Server
guildName = "Bot Testing"
adminRoleID = 635793044029046795 #int
categoryName = "Herndon ModMail"
welcomeTitle = "Welcome to the Herndon Robotics Discord server!"
welcomeMessage = "Before you get started chatting, take a second to look through <#655122182610878504> to get set up within the server."
welcomeImage = ""
requestResponse = "Your message has been received by the Herndon Robotics staff team!"
requestResolvedMessage = "The Herndon Robotics staff team has marked your issue as resolved."
closeCommand = "!close"
logChannelName = "modmail"

#Event that is called when the bot goes online
@client.event
async def on_ready():
	FindGuild()
	await InitializeSection()

#Event called when a new member joins the Server
@client.event
async def on_member_join(member):
	embed=discord.Embed(title=welcomeTitle, description=welcomeMessage)
	embed.set_image(url = welcomeImage)
	await member.send(embed=embed)

#Event called when a message is sent
@client.event
async def on_message(message):
	#Makes sure im not looking at my own messages
	if message.author == client.user:
		return

	#Checks if its a private message
	if isinstance(message.channel, discord.DMChannel):
		#Creates a text channel in the server with the user's name
		text_channel = await create_text_channel(message.author)

		#If this is the first message in the conversation, add it to the dictionary and send a few messages
		if currentChannels.get(text_channel.id) == None:
			currentChannels.update({text_channel.id:message.author.id})
			await text_channel.send(client.guilds[0].get_role(adminRoleID).mention)
			await text_channel.send("**" + message.author.name + "#" + message.author.discriminator + " Requires your assistance with the following:**")
			await text_channel.send(message.author.mention + ": " + message.content)
			await message.author.send(requestResponse)
		else:
			await text_channel.send(message.author.mention + ": " + message.content)
	#Otherwise, if the message comes from a channel inside the modmail category
	elif message.channel.category_id == category.id:
		#If its a close command, add everything to the logs channel, and delete the channel
		if message.content == closeCommand:
			await client.get_user(currentChannels[message.channel.id]).send(requestResolvedMessage)
			await log_conversation(client.get_user(currentChannels[message.channel.id]), await message.channel.history(limit=100).flatten())
			del currentChannels[message.channel.id]
			await message.channel.delete()
		#Otherwise just send our response to the receipient as a private message
		else:
			await client.get_user(currentChannels[message.channel.id]).send("**" + message.author.name + ":** " + message.content)

#Finds the guild with the appropriate name
def FindGuild():
	global guild

	for g in client.guilds:
		if g.name == guildName:
			guild = g
			break
	guild = client.guilds[0]

#Initializes the category and creates the log channel
async def InitializeSection():
	global category
	global logChannel

	#Gives permissions to the adminRole, and revokes it from everyone else
	permissions = {
    	guild.default_role: discord.PermissionOverwrite(read_messages=False),
    	guild.get_role(adminRoleID): discord.PermissionOverwrite(read_messages=True)
	}

	#Deletes the old category and all its channels if they still exist
	for cat in guild.categories:
		if cat.name == categoryName:
			for chan in cat.channels:
				if chan.name == logChannelName.lower():
					logChannel = chan
					continue
				for mess in await chan.history(limit=25).flatten():
					if(len(mess.mentions) == 1):
						currentChannels.update({chan.id:mess.mentions[0].id})
						break
			category = cat
			await logChannel.send(client.guilds[0].get_role(adminRoleID).mention + " ModMail is back Online")
			return

	category = await guild.create_category(categoryName, overwrites=permissions)
	logChannel = await category.create_text_channel(logChannelName)
	await logChannel.send(client.guilds[0].get_role(adminRoleID).mention + " This is the very beginning of the logs history")

	#Sets an activity for the bot
	await client.change_presence(activity=discord.Activity(name="DM to contact Mods", type=3))

#Loops through all channels within category, returns it if it already exists, otherwise create it
async def create_text_channel(author):
	for channel in category.text_channels:
		if currentChannels.get(channel.id) == author.id:
			return channel
	return await category.create_text_channel(author.name + author.discriminator)

#Loops through the message history and logs it to the log channel
async def log_conversation(conversationOwner, history):
	log = ""

	history.reverse()
	for message in history:
		if message.author == client.user:
			log += message.content + "\n"
		else:
			log += "**" + message.author.name + ":** " + message.content + "\n"
	
	embed=discord.Embed(title="Conversation With " + conversationOwner.name, description=log)
	await logChannel.send(embed=embed)

client.run(BotID)