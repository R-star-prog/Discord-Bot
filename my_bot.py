import discord
from discord.ext import commands
import random
import pandas as pd
import asyncio
import youtube_dl
import os


value = random.randint(1,10)




# bot for the code
#client = discord.Client()

client = commands.Bot(command_prefix = '--')

@client.command(name= 'version')
async def version(context):
    
        
    myEmb = discord.Embed(title = "Current Version",description = "Bot is in Version 1.0", color = 0xff0000)
    myEmb.add_field(name = "Version Code:", value = "v1.0.0", inline = False)
    myEmb.add_field(name = "Date Released", value = "July 18th, 2020", inline = False)
    myEmb.set_footer(text = "This is a sample footer")
    myEmb.set_author(name = "Rayo Belihomji")
    await context.message.channel.send(embed = myEmb)



@client.event
async def on_disconnect():
    general_channel = client.get_channel(796908083393331230)

    await general_channel.send('Bye')


#Kick a person command
@client.command(name= 'kick', pass_context = True) 
@commands.has_permissions(kick_members = True)

async def kick(context, member: discord.Member):
    await member.kick()
    await context.send('User ' + member.display_name + ' has been kicked.')


@client.command(name = 'ban', pass_context = True) 
@commands.has_permissions(kick_members = True)

async def ban(context, member: discord.Member,*, reason = None):
    await member.ban(reason = reason)
    await context.send('User ' + member.display_name + ' has been banned.')







@client.event
#predefined name
async def on_ready():
    # Do stuff...
    print(value)
    if value == 3:
        
        await client.change_presence(status = discord.Status.do_not_disturb, activity = discord.Game('Black Opps 2'))

    else:

        general_channel = client.get_channel(796908083393331230)

        await general_channel.send('hello')

        #df = pd.DataFrame({"A": ['Hello', 'Test']})
        #df.to_csv('/Users/rayobelihomji/Discord Bot/output.csv')





@client.event
async def on_message(message):

    if message.content == 'what is the version':
        general_channel = client.get_channel(796908083393331230)
        
        myEmb = discord.Embed(title = "Current Version",description = "Bot is in Version 1.0", color = 0xff0000)
        myEmb.add_field(name = "Version Code:", value = "v1.0.0", inline = False)
        myEmb.add_field(name = "Date Released", value = "July 18th, 2020", inline = False)
        myEmb.set_footer(text = "This is a sample footer")
        myEmb.set_author(name = "Rayo Belihomji")
        await general_channel.send(embed = myEmb)

    # send DM after work
    if message.content == 'send a DM':
        
        await message.author.send('This is a DM. Have a great day')


        #await general_channel.send(embed = myEmb)
    if message.content == "Append":

        #Add row tht contains message
        df = pd.read_csv('/Users/rayobelihomji/Discord Bot/output.csv', index_col = 0)
        df = df.append({"A": 'This is the message I want to append'},ignore_index = True)
        df.to_csv('/Users/rayobelihomji/Discord Bot/output.csv')

    await client.process_commands(message)



# Plays songs From the API

@client.command()

async def play(ctx, url : str):
    ##convert the url
    song = os.path.isfile("song.mp3")

    try:
        if song:
            os.remove("song.mp3")

    except PermissionError:
        await ctx.send("Wait for song to end or use stop command")
        return

    
    voiceChan = discord.utils.get(ctx.guild.voice_channels, name = 'General')
    await voiceChan.connect()
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)


    '''  
    if not voice.is_connected():
        await voiceChan.connect()
    '''
    #options of the youtube video
    ydl_op =  {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec' : 'mp3',
            'preferredquality' : '192',

        }],
    }
    with youtube_dl.YoutubeDL(ydl_op) as ydl:
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file,"song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"))




@client.command()

async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)

    if voice.is_connected():
        await voice.disconnect()

    
   
    else:
        await ctx.send("Bot is not connected")


@client.command()

async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)

    if voice.is_playing():
        voice.pause()

    else:
        await ctx.send("No audio is playing")


@client.command()

async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)

    if voice.is_paused():
        voice.resume()

    else:
        await ctx.send("audio is not paused")


@client.command()

async def stop(ctx):

    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)

    voice.stop()




# Run on server (Can regenerate token)
client.run('Nzk2OTA2NDY5MjMxNTU4NzA0.X_eu_A.jRXTo3ty9KXCnqdpOD8mTUk17vs')





