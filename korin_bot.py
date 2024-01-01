from dotenv import load_dotenv
from discord.ext import commands, tasks #is a way to communicate with discord, a client with helper functions 
from dataclasses import dataclass
from kami import get_character, get_random_character, get_list # grab information about characters
import discord
import os
import datetime
import random

# Load environment variables from .env
load_dotenv()

# Access environment variables
token = os.getenv("token")
CHANNEL_ID = 1189257854146859058
MAX_SESSION_IN_MINS = 30

#Creating a class for loging Working time
@dataclass
class WorkSession:
    is_active: bool = False
    start_time: int = 0

@dataclass
class StudySession:
    is_active: bool = False
    start_time: int = 0

#creating a bot 
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
worksesh = WorkSession()
studysesh = StudySession()

@bot.event 
async def on_ready():
    try:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send("Hello there fellow Z-Fighters")
        else:
            print("Channel not found")
    except Exception as e:
        print(f"An error occurred: {e}")

@bot.command(name='commands', help='Display the list of available commands')
async def list_commands(ctx):
    command_list = [f"{command.name}: {command.help}" for command in bot.commands]
    command_output = "\n".join(command_list)
    await ctx.send(f"```Available Commands:\n{command_output}```")


@tasks.loop(minutes=MAX_SESSION_IN_MINS, count=2)
async def work_break_reminder(): 
    #ignore the first execution of this command
    if work_break_reminder.current_loop == 0:
        return

    channel =  bot.get_channel(CHANNEL_ID)
    await channel.send(f"**Take a well deserved break!** You've been working for {MAX_SESSION_IN_MINS} minutes.")

@tasks.loop(minutes=MAX_SESSION_IN_MINS, count=2)
async def study_break_reminder(): 
    #ignore the first execution of this command
    if study_break_reminder.current_loop == 0:
        return

    channel =  bot.get_channel(CHANNEL_ID)
    await channel.send(f"**Take a well deserved break!** You've been studying for {MAX_SESSION_IN_MINS} minutes.")

start_work_aliases = ['starting working', 'start work', 'beginning work', 'work begins', 'work started']
@bot.command(name='startwork', aliases=start_work_aliases,
             help="Starts to log a work session.")
async def startwork(ctx):
    if worksesh.is_active:
        await ctx.send(f"A work session is already active!")
        return
    
    worksesh.is_active = True
    worksesh.start_time = ctx.message.created_at.timestamp()
    human_readable_time = ctx.message.created_at.strftime("%H:%M:%S")
    work_break_reminder.start()
    await ctx.send(f"New work session started at {human_readable_time}")

@bot.command(name='endwork', aliases=['stop working', 'stop work', 'finished work', 'end work', 'work ended'],
             help="Ends the work session and returns total time worked")
async def endwork(ctx):
    if not worksesh.is_active:
        await ctx.send(f"No work session is active!")
        return
    
    worksesh.is_active = False
    end_time = ctx.message.created_at.timestamp()
    human_readable_time_end = ctx.message.created_at.strftime("%H:%M:%S")
    duration = int(end_time - worksesh.start_time)
    human_readable_duration = str(datetime.timedelta(seconds=duration))
    work_break_reminder.stop()
    await ctx.send(f"Work session ended at {human_readable_time_end} and lasted for {human_readable_duration}")

@bot.command(name='startstudying', aliases=['start studying', 'study time', 'start studies'], help="Starts a studying session.")
async def startstudying(ctx):
    if studysesh.is_active:
        await ctx.send(f"A study session is already active!")
        return
    
    studysesh.is_active = True
    studysesh.start_time = ctx.message.created_at.timestamp()
    human_readable_time = ctx.message.created_at.strftime("%H:%M:%S")
    study_break_reminder.start()
    await ctx.send(f"New study session started at {human_readable_time}")

@bot.command(name='endstudying', aliases=['end studies', 'end studying', 'stop studying'], help="Ends the study session and" +
             " returns total time studied.")
async def endstudying(ctx):
    if not studysesh.is_active:
        await ctx.send(f"No session is active!")
        return
    
    studysesh.is_active = False
    end_time = ctx.message.created_at.timestamp()
    human_readable_time_end = ctx.message.created_at.strftime("%H:%M:%S")
    duration = int(end_time - worksesh.start_time)
    human_readable_duration = str(datetime.timedelta(seconds=duration))
    study_break_reminder.stop()
    await ctx.send(f"Study session ended at {human_readable_time_end} and lasted for {human_readable_duration}")

#stores list of characters and info from kami.py file
list = get_list()

@bot.command(name='getrandomcharacter', aliases=['rnd character', 'random'],
             help="Displays a random DB,DBZ, and DBS character with its description.")
async def getrandomcharacter(ctx):
    random_char = get_random_character(list)
    await ctx.send(random_char)

@bot.command(name='getcharacter', aliases=['get character', "get char", 'character info'],
             help="Displays a random DB,DBZ, and DBS character with its description.")
async def getcharacter(ctx, *args):
    if(len(args)<=1):
        name = str(args[0]).title()
    elif(len(args)>1 and len(args) <=2):
        name = args[0] +  " " + args[1]
        name = str(name).title() 
    else:
        name = "DNE"
    descriptions = None
    while(descriptions is None):
        try:
            # Call the get_character function to retrieve information about the character
            descriptions  = get_character(list, name)  
            
            # Send the retrieved information as a reply
            await ctx.send(f'Information about {name}: {descriptions} ') 
        except Exception as e:
            print(f'Error retrieving character information: {e}')
            ctx.send('An error occurred while retrieving character information. Try inputting character name again:')
            descriptions = "Couldn't find character."


@bot.command(name='powerlvl', aliases=['my power', 'my power level', 'power', 'level'], help="Gives user their power level.")
async def powerlvl(ctx):
    power = random.randint(-100000,1000000)
    if(power<100):
        return await ctx.send(f'Your power level is: {power}. \nCongrats you are very weak human, How does it feel to be weaker than Yamncha in the Saiyan Saga')
    elif(power>=100 and power<=1000):
        return await ctx.send(f'Your power level is: {power}. \nCongrats you are a low tier warrior, the saibamen might be trouble for you.')
    elif(power>1000 and power<10000):
        return await ctx.send(f'Your power level is: {power}. \nCongrats you are a low-mid tier warrior, the saibamen might be easy work for you.')
    elif(power>=10000 and power<60000):
        return await ctx.send(f'Your power level is: {power}. \nCongrats you are a mid-mid tier warrior, the Ginyu force might recruit you.')
    elif(power>=60000 and power<=150000):
        return await ctx.send(f'Your power level is: {power}. \nCongrats you are a upper-mid tier warrior, you might be able to solo the Ginyu force.')
    elif(power>150000 and power<=500000):
        return await ctx.send(f'Your power level is: {power}. \nCongrats you are a low-upper warrior, King Cold my try to convince you to join forces.')
    elif(power>500000 and power<=1000000):
        return await ctx.send(f'Your power level is: {power}. \nCongrats you are a mid-upper warrior, Your pinky can destroy planets.')
    else:
        return await ctx.send(f'Holy Kami your power level is : {power}, you are strong AF. When you fight planets are prone to explode.')

@bot.command(name='Hello', aliases=['Hi', "Hi korin", "Hello Korin", "hello", "hey", "hi", "Hey"], help="Salutes the user.")
async def hello(ctx):
    await ctx.send("Hello Z-fighter, remember to train to increase your power level. \nThe earth might need your help one day.")
bot.run(token)
