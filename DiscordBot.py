import discord
import time
import asyncio
import os
import configparser

from threading import Timer
from http.server import BaseHTTPRequestHandler, HTTPServer

intents = discord.Intents.default()
intents.members = True
bot = discord.Client(intents = intents)

configSection = 'DiscordBot'
servSection = 'WebServer'
configFile = 'config.ini'
config = configparser.ConfigParser()
config.read(configFile)

token = config.get(configSection, 'token')

buffer_directory = config.get(servSection, 'buffer_directory')
target_directory = config.get(servSection, 'target_directory')
DEBUG = config.getboolean('Default','debug')
is_ready = False

#Used for local testing
if(DEBUG):
    print("DEBUG MODE ACTIVE")
    
def updateConfig():
    print('Checking configuration file')
    config.read(configFile)
    global targetMute_id
    targetMute_id = config.getint(configSection, 'targetMute_id')
    global targetServer_id
    targetServer_id = config.getint(configSection, 'targetServer_id')
    global muteTime
    muteTime = config.getint(configSection, 'timeout')
    global audio_file
    audio_file = config.get(configSection, 'audiofile')
    global enabled
    enabled =  config.getboolean(configSection, 'enabled')
    global cooldown 
    cooldown = config.getint(configSection, 'cooldown')
    print(targetMute_id, targetServer_id, muteTime, audio_file, enabled)
    

updateConfig()

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    global is_ready
    is_ready = True

  
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('$mute'):
        targetMute_id = message.author.id
        chan = message.channel
        is_servmute = message.author.voice.mute
        inverse_servmute = not is_servmute
        
        print('Message auth ID = ', targetMute_id)
        print('Message channel = ',  chan)
        print('Author muted = ',  is_servmute)
        
        #await message.guild.change_voice_state(channel=chan, self_mute=True, self_deaf=False)
        await message.author.edit(mute=inverse_servmute)

@bot.event
async def check_for_cmd():
    while not is_ready:
        await asyncio.sleep(0.5) #Wait for ready
    
    while True:    
        updateConfig()
        while enabled:                              
            lines = []
            last_Edit = os.stat(buffer_directory).st_mtime
            
            while True:
                await asyncio.sleep(0.05)
                if(last_Edit != os.stat(buffer_directory).st_mtime):
                    last_Edit = os.stat(buffer_directory).st_mtime
                    with open(buffer_directory) as f:
                        lines = f.readlines()
                        
                    if(lines[0] == target_directory):
                        break  
                        
            updateConfig() 
            
            if not enabled:
                print('Command recieved, not enabled. Breaking')
                break
             
            try:
                tarVC = bot.get_guild(targetServer_id).get_member(targetMute_id).voice.channel  
                        
                guild = await bot.fetch_guild(targetServer_id)
                print ('Targeting Discord: ', guild)
                
                mute_User = await bot.fetch_user(targetMute_id)
                print ('Targeting User: ', mute_User)
                
                connected = False
                for i in bot.voice_clients:
                    if(i.guild.id == guild.id):
                        connected = True        
                if(connected == False):        
                    vc = await tarVC.connect()
                        
                if DEBUG:
                    vc.play((discord.FFmpegPCMAudio(executable='C:/Users/tnive/Desktop/OBB/ffmpeg/bin/ffmpeg.exe', source=audio_file)), after=None)
                else:     
                    vc.play(discord.FFmpegPCMAudio(source=audio_file))   
                
                #Mutes for determined time period
                await bot.get_guild(targetServer_id).get_member(targetMute_id).edit(mute=True)
                time.sleep(muteTime)
                #Unmutes
                await bot.get_guild(targetServer_id).get_member(targetMute_id).edit(mute=False)
                await vc.disconnect()
                
            except (Exception):
                print('ERROR')        
            
            await asyncio.sleep(cooldown)
            
        await asyncio.sleep(1)

if not DEBUG: 
    time.sleep(5)    
    
bot.loop.create_task(check_for_cmd())
bot.run(token)

print('Ended')
