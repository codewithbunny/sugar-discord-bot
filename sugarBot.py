import discord
from discord.ext import commands, tasks
from itertools import cycle
from discord.utils import get
import youtube_dl
from datetime import *
import json
import spotdl
import os
import shutil
from os import system
import random
import sqlite3
import phonenumbers
from phonenumbers import carrier
from phonenumbers import geocoder
from phonenumbers import timezone

def get_prefix(sugarBot, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

sugarBot = commands.Bot(command_prefix = get_prefix)
@sugarBot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "Sugar "
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

DIR = os.path.dirname(__file__)
db = sqlite3.connect(os.path.join(DIR, "SongTracker.db"))
SQL = db.cursor()
sugarBot.remove_command('help')
status = cycle(['Sugar help', 'Very Sweet'])
now = datetime.now()
current_time = now.strftime("%H")

@tasks.loop(seconds=10)
async def change_status():
    await sugarBot.change_presence(activity=discord.Game(next(status)))
@sugarBot.event
async def on_ready():
    change_status.start()
    print('Bot is ready')

@sugarBot.command(aliases=['help', 'h', 'Help'])
async def _help(ctx):
    embed = discord.Embed(
        colour = discord.Colour.green(),
        title= 'Help Menu',
        description = 'Where there is SUGAR there is SWEETNESS\n'
    )
    embed.set_author(name= 'Sweet Sugar', icon_url='https://img.icons8.com/color/48/000000/technical-support.png')
    embed.set_image(url='https://i.ibb.co/MNNwdvr/sugar.png')
    embed.set_thumbnail(url='https://img.icons8.com/fluent/48/000000/help.png')
    embed.add_field(name='Hello :wave:', value='The bot say Hello and express the good wishes.', inline=False)
    embed.add_field(name='Bye :hand_splayed:', value='The bot say Bye and express the good wishes.', inline=False)
    embed.add_field(name='Clear :recycle:', value='The bot delete the messages how much you want to delete. It take number as a argument.', inline=False)
    embed.add_field(name='Kick :mechanical_leg:', value='The bot kick the member from the discord server. It take argument as a member to whom you want to kick.', inline=False)
    embed.add_field(name='Ban :outbox_tray:', value='The bot ban the member from the discord server. It take argument as a member to whom you want to ban.', inline=False)
    embed.add_field(name='Unban :inbox_tray:', value='The unban kick the member from the discord server. It take argument as a member which you want to unban.', inline=False)
    embed.add_field(name='Join :headphones:', value='The bot join the voice channel.', inline=False)
    embed.add_field(name='Leave :arrow_left:', value='The bot leave the voice channel.', inline=False)
    embed.add_field(name='Play :musical_note:', value='The bot plays the songs. [It can play songs from youtube and spotify].', inline=False)
    embed.add_field(name='Queue :page_with_curl:', value='The bot add the new songs in queue.', inline=False)
    embed.add_field(name='Pause :pause_button:', value='The bot pause the song.', inline=False)
    embed.add_field(name='Resume :play_pause:', value='The bot resume the song.', inline=False)
    embed.add_field(name='Skip :track_next:', value='The bot change the song.', inline=False)
    embed.add_field(name='Stop :octagonal_sign:', value='The bot stop playing music.', inline=False)
    embed.add_field(name='Volume :sound:', value='The bot can increase and decrease the volume of the song. It take number as argument from [0 to 100].', inline=False)
    embed.add_field(name='Games :video_game:', value='For game menu', inline=False)
    embed.add_field(name='Mobile :iphone: ', value='To get the information of a phone number\nCommand : < Sugar mobile [+country_code mobile_number] >', inline=False)
    embed.add_field(name='help :question:', value='The bot show the help menu.', inline=False)
    embed.set_footer(text='Dont try to copy SUGAR. You dont have that COPYRIGHT ©')

    await ctx.send(embed=embed)

@sugarBot.command(aliases=['games', 'g', 'gh'])
async def _games(ctx):
    embed = discord.Embed(
        colour = discord.Colour.green(),
        title= 'Games Menu',
        description = 'Where there is SUGAR there is SWEETNESS\n'
    )
    embed.set_author(name= 'Sweet Sugar', icon_url='https://img.icons8.com/color/48/000000/technical-support.png')
    embed.set_image(url='https://img.icons8.com/officel/100/000000/controller.png')
    embed.set_thumbnail(url='https://img.icons8.com/fluent/48/000000/menu--v2.png')
    embed.add_field(name='Dice :video_game:', value="Dice thrown between 1 to 6 \nCommand : < Sugar dice [args : number] >", inline=False)
    embed.add_field(name='Coin :video_game:', value="Truth and Dare \nCommand : <Sugar flip>", inline=False)
    embed.add_field(name='RPS :video_game:', value="Rock | Paper | Scissor game \nCommand : < Sugar rps [args : rock|paper|scissor] >", inline=False)
    embed.set_footer(text="Life's a game, All you have to do is know how to play it.")

    await ctx.send(embed=embed)

@sugarBot.command(aliases=['hbd'])
async def HBD(ctx, user_date : str) :
    today = date.today()
    await ctx.send(f"Today: " +  today.strftime('%A %d, %b %Y'))

    dob_str = user_date
    dob_data = dob_str.split("/")
    dobDay = int(dob_data[0])
    dobMonth = int(dob_data[1])
    dobYear = int(dob_data[2])
    dob = date(dobYear,dobMonth,dobDay)

    numberOfDays = (today - dob).days 

    age = numberOfDays // 365
    await ctx.send("You are " + str(age) + " years old.")

    day = dob.strftime("%A")
    await ctx.send("You were born on a " + day + ".")

    await ctx.send("You have spent " + str(numberOfDays) + " days on Earth.")

    thisYear = today.year
    nextBirthday = date(thisYear,dobMonth,dobDay)
    if today < nextBirthday:
        gap = (nextBirthday - today).days
        await ctx.send("Your birhday is in " + str(gap) + " days.")
    elif  today == nextBirthday:
        await ctx.send(f"Today is your birthday {ctx.author.mention} Happy Birthday!")
        await ctx.send(f"https://tenor.com/view/gif-4299327")
        await ctx.send(f"https://tenor.com/view/happy-birthday-cake-gif-5954011")
    else:
        nextBirthday = date(thisYear+1,dobMonth,dobDay)
        gap = (nextBirthday - today).days
        await ctx.send("Your birthday is in " + str(gap) + " days.")

@sugarBot.command(aliases=['hello', 'Hey', 'hey', 'Hi', 'hi'])
async def Hello(ctx) :
    if int(current_time) < 12 :
        await ctx.send(f'Hello {ctx.author.mention}! GOOD MORNING')
    elif int(current_time) >= 12 and int(current_time) < 17 :
        await ctx.send(f'Hello {ctx.author.mention}! GOOD AFTERNOON')
    elif int(current_time) >= 17 and int(current_time) < 20 :
        await ctx.send(f'Hello {ctx.author.mention}! GOOD EVENING')
    else :
        await ctx.send(f'Hello {ctx.author.mention}!')
@sugarBot.command(aliases=['bye'])
async def Bye(ctx) :
    if (int(current_time) >= 1 and int(current_time) <= 4) or (int(current_time) >= 20) :
        await ctx.send(f'Bye {ctx.author.mention}! GOOD NIGHT')
    else:
        await ctx.send(f'Bye {ctx.author.mention}!')

@sugarBot.command(aliases=['Mobile', 'phone', 'Phone'])
async def mobile(ctx, user_mobile : str) :
    phone_number = user_mobile
    phone_number = phonenumbers.parse(phone_number)
    validNumber = phonenumbers.is_valid_number(phone_number)
    if validNumber is True :
        phone_number_carrier = carrier.name_for_number(phone_number, 'en')
        phone_number_country = geocoder.description_for_number(phone_number, 'en')
        phone_number_timezone = timezone.time_zones_for_number(phone_number)
        
        await ctx.send(f"Valid no. status : {validNumber}\nPhone no. details : {phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}\nPhone no. carrier : {phone_number_carrier}\nPhone no. country : {phone_number_country}\nPhone no. timezone : {str(phone_number_timezone)}")
    else : 
        await ctx.send(f"Valid no. status : {validNumber}\nNumber is invalid, try to input a valid number")

@sugarBot.command(pass_context=True, aliases=['Flip', 'flip'])
async def coin(ctx):
    items = ['Truth', 'Dare']
    status = random.choice(items)
    coin_result = random.randint(0, 1)
    if coin_result == 1 :
        await ctx.send(f'Heads, you got {status}')
    else : 
        await ctx.send(f'Tails, you got {status}')

@sugarBot.command(pass_context=True, aliases=['Dice', 'dice'])
async def DiceThrow(ctx, user_choice : int):
    dice_result = random.randint(1, 6)
    if user_choice == dice_result:
        await ctx.send(f"{ctx.author.mention} number: {user_choice} \nDice number: {dice_result} \nYou won, you guessed right dice number")
    elif user_choice != dice_result and user_choice <= 6:
        await ctx.send(f"{ctx.author.mention} number: {user_choice} \nDice number: {dice_result} \nYou lose, you guessed wrong dice number")
    else : 
        await ctx.send(f"Invalid number")
@DiceThrow.error
async def DiceThrow_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'Please specify an dice number from between 1 to 6')

@sugarBot.command(pass_context=True, aliases=['rps', 'RPS'])
async def rpsgame(ctx, user_choice : str):
        ROCK = 'rock'
        PAPER = 'paper'
        SCISSOR = 'scissor'
        user_choice = user_choice.lower()
        def get_choices():
            return(ROCK, PAPER, SCISSOR)
        bot_choice = random.choice(get_choices())

        winner_check = {
            (ROCK, PAPER) : False,
            (ROCK, SCISSOR) : True,
            (PAPER, ROCK) : True,
            (PAPER, SCISSOR) : False,
            (SCISSOR, ROCK) : False,
            (SCISSOR, PAPER) : True,
        }
        won = None
        if bot_choice == user_choice:
            won = None
        else:
            won = winner_check[(user_choice, bot_choice)]
        
        if won is None:
            message = f"{ctx.author.mention}: %s\nVS\nBot: %s \nIt's Draw!"%(user_choice, bot_choice)
        elif won is True:
            message = f"{ctx.author.mention}: %s\nVS\nBot: %s \n{ctx.author.mention} win & Bot lose"%(user_choice, bot_choice)
        elif won is False:
            message = f"{ctx.author.mention}: %s\nVS\nBot: %s \n{ctx.author.mention} lose & Bot win"%(user_choice, bot_choice)

        await ctx.send(message)
@rpsgame.error
async def rpsgame_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'Please specify any one value = rock | paper | scissor')

@sugarBot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'Command not found')
@sugarBot.command(aliases=['Clear'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)
    await ctx.channel.send(f'{amount} Messages Deleted')
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'Please specify an amount(eg. 5, 10, 500) to delete the messages')

@sugarBot.command(aliases=['Kick'])
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} Kicked')
@sugarBot.command(aliases=['Ban'])
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} Banned')
@sugarBot.command(aliases=['Unban'])
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_id = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if(user.name, user.discriminator) == (member_name, member_id):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@sugarBot.command(pass_context=True, aliases=['Join'])
async def join(ctx):
    global voice
    SQL.execute('create table if not exists Music('
                '"Num" integer not null primary key autoincrement, '
                '"Server_ID" integer, '
                '"Server_Name" text, '
                '"Voice_ID" integer, '
                '"Voice_Name" text, '
                '"User_Name" text, '
                '"Next_Queue" integer, '
                '"Queue_Name" text, '
                '"Song_Name" text'
                ')')
    server_name = str(ctx.guild)
    server_id = ctx.guild.id
    SQL.execute(f'delete from music where Server_ID ="{server_id}" and Server_Name = "{server_name}"')
    db.commit()
    user_name = str(ctx.message.author)
    queue_name = f"Queue#{server_id}"
    song_name = f"Song#{server_id}"
    channel_id = ctx.message.author.voice.channel.id
    channel_name = str(ctx.message.author.voice.channel)
    queue_num = 1
    SQL.execute('insert into Music(Server_ID, Server_Name, Voice_ID, Voice_Name, User_Name, Next_Queue, Queue_Name, Song_Name) values(?,?,?,?,?,?,?,?)',
                (server_id, server_name, channel_id, channel_name, user_name, queue_num, queue_name, song_name))
    db.commit()

    channel = ctx.message.author.voice.channel
    voice = get(sugarBot.voice_clients, guild=ctx.guild)

    if voice is not None:
        return await voice.move_to(channel)
        
    await channel.connect()
    await ctx.send(f'Joined {channel} :microphone:')
@sugarBot.command(pass_context=True, aliases=['Leave'])
async def leave(ctx):
    server_name = str(ctx.guild)
    server_id = ctx.guild.id
    channel_id = ctx.message.author.voice.channel.id
    channel_name = str(ctx.message.author.voice.channel)
    SQL.execute(f'delete from music where Server_ID ="{server_id}" and Server_Name = "{server_name}" and Voice_ID="{channel_id}" and Voice_Name="{channel_name}"')
    db.commit()

    channel = ctx.message.author.voice.channel
    voice = get(sugarBot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f'Left {channel} :arrow_left:')
    else:
        await ctx.send("I'm not connected in any voice channel :x:")

@sugarBot.command(pass_context=True, aliases=['Pause'])
async def pause(ctx):
    voice = get(sugarBot.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        voice.pause()
        await ctx.send('Paused music :pause_button:')
    else:
        await ctx.send('Music is not playing')
@sugarBot.command(pass_context=True, aliases=['Resume'])
async def resume(ctx):
    voice = get(sugarBot.voice_clients, guild=ctx.guild)
    if voice and voice.is_paused():
        voice.resume()
        await ctx.send('Resumed music :white_check_mark:')
    else:
        await ctx.send('Music is not paused')

@sugarBot.command(pass_context=True, aliases=['Play'])
async def play(ctx, *url: str):
    server_name = str(ctx.guild)
    server_id = ctx.guild.id
    channel_id = ctx.message.author.voice.channel.id
    channel_name = str(ctx.message.author.voice.channel)
    try:
        SQL.execute(f'select Song_Name from Music where Server_ID="{server_id}" and Server_Name="{server_name}" and Voice_ID="{channel_id}" and Voice_Name="{channel_name}"')
        name_song = SQL.fetchone()
        SQL.execute(f'select Server_Name from Music where Server_ID="{server_id}" and Server_Name="{server_name}"')
        name_server = SQL.fetchone()
    except:
        await ctx.send("The bot must join a voice channel to play a song")
        return

    voice = get(sugarBot.voice_clients, guild=ctx.guild)
    def check_queue():
        DIR = os.path.dirname(__file__)
        db = sqlite3.connect(os.path.join(DIR, "SongTracker.db"))
        SQL = db.cursor()
        SQL.execute(f'select Queue_Name from Music where Server_ID="{server_id}" and Server_Name="{server_name}"')
        name_queue = SQL.fetchone()
        SQL.execute(f'select Server_Name from Music where Server_ID="{server_id}" and Server_Name="{server_name}"')
        name_server = SQL.fetchone()

        Queue_infile = os.path.isdir("./Queues")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queues"))
            Queue_Main = os.path.join(DIR, name_queue[0])
            length = len(os.listdir(Queue_Main))
            still_q = length - 1
            try:
                first_file = os.listdir(Queue_Main)[0]
                song_num = first_file.split('-')[0]
            except:
                SQL.execute('update Music set Next_Queue = 1 where Server_ID = ? and Server_Name = ?', (server_id, server_name))
                db.commit()
                return

            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath(Queue_Main) + "\\" + first_file)
            if length != 0:
                song_there = os.path.isfile(f"{name_song[0]}({name_server[0]}).mp3")
                if song_there:
                    os.remove(f"{name_song[0]}({name_server[0]}).mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file == f"{song_num}-{name_song[0]}({name_server[0]}).mp3":
                        os.rename(file, f'{name_song[0]}({name_server[0]}).mp3')

                voice.play(discord.FFmpegPCMAudio(f'{name_song[0]}({name_server[0]}).mp3'), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 1.0
            else:
                SQL.execute('update Music set Next_Queue = 1 where Server_ID = ? and Server_Name = ?', (server_id, server_name))
                db.commit()
                return
        else:
            SQL.execute('update Music set Next_Queue = 1 where Server_ID = ? and Server_Name = ?', (server_id, server_name))
            db.commit()

    song_there = os.path.isfile(f"{name_song[0]}({name_server[0]}).mp3")
    try:
        if song_there:
            os.remove(f"{name_song[0]}({name_server[0]}).mp3")
            SQL.execute('update Music set Next_Queue = 1 where Server_ID = ? and Server_Name = ?', (server_id, server_name))
            db.commit()
    except PermissionError:
        await ctx.send("ERROR: Music playing")
        return
        
    SQL.execute(f'select Queue_Name from Music where Server_ID="{server_id}" and Server_Name="{server_name}"')
    name_queue = SQL.fetchone()
    queue_infile = os.path.isdir("./Queues")
    if queue_infile is True:
        DIR = os.path.abspath(os.path.realpath("Queues"))
        Queue_Main = os.path.join(DIR, name_queue[0])
        Queue_Main_infile = os.path.isdir(Queue_Main)
        if Queue_Main_infile is True:
            print("Removed old queue folder")
            shutil.rmtree(Queue_Main)

        await ctx.send('Getting everything ready now')
        song_path = f"./{name_song[0]}({name_server[0]}).mp3"
        
        ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': False,
        'outtmpl': song_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    song_search = " ".join(url)

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{song_search}", download=False)
            info_dict = info.get('entries', None)[0]
            video_title = info_dict.get('title', None)
            ydl.download([f"ytsearch1:{song_search}"])

    except:
        print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if spotify URL)")
        c_path = os.path.dirname(os.path.realpath(__file__))
        system(f"spotdl -sf {name_song[0]}({name_server[0]}) -f " + '"' + c_path + '"' + " -s " + song_search)

    voice.play(discord.FFmpegPCMAudio(f"{name_song[0]}({name_server[0]}).mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 1.0
    await ctx.send(f"Now playing: {video_title}")

@sugarBot.command(pass_context=True, aliases=['Queue'])
async def queue(ctx, *url: str):
    server_name = str(ctx.guild)
    server_id = ctx.guild.id
    try:
        SQL.execute(f'select Queue_Name from Music where Server_ID="{server_id}" and Server_Name="{server_name}"')
        name_queue = SQL.fetchone()
        print(name_queue)
        SQL.execute(f'select Song_Name from Music where Server_ID="{server_id}" and Server_Name="{server_name}"')
        name_song = SQL.fetchone()
        print(name_song)
        SQL.execute(f'select Next_Queue from Music where Server_ID="{server_id}" and Server_Name="{server_name}"')
        q_num = SQL.fetchone()
        print(q_num)
    except:
        await ctx.send("The bot must join a voice channel to queue a song")
        return

    Queue_infile = os.path.isdir("./Queues")
    if Queue_infile is False:
        os.mkdir("Queues")
    DIR = os.path.abspath(os.path.realpath("Queues"))
    Queue_Main = os.path.join(DIR, name_queue[0])
    Queue_Main_infile = os.path.isdir(Queue_Main)
    if Queue_Main_infile is False:
        os.mkdir(Queue_Main)

    SQL.execute(f'select Server_Name from Music where Server_ID="{server_id}" and Server_Name="{server_name}"')
    name_server = SQL.fetchone()
    queue_path = os.path.abspath(os.path.realpath(Queue_Main) + f"\\{q_num[0]}-{name_song[0]}({name_server[0]}).mp3")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': False,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    song_search = " ".join(url)

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch1:{song_search}"])
            info = ydl.extract_info(f"ytsearch1:{song_search}", download=False)
            info_dict = info.get('entries', None)[0]
            video_title = info_dict.get('title', None)
    except:
        print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if spotify URL)")
        Q_DIR = os.path.abspath(os.path.realpath("Queues"))
        Queue_Path = os.path.join(Q_DIR, name_queue[0])
        print(Queue_Path)
        system(f"spotdl -sf {q_num[0]}-{name_song[0]}({name_server[0]}) -f " + '"' + Queue_Path + '"' + " -s " + song_search)

    await ctx.send(f"Adding {video_title} to the queue")
    SQL.execute('update Music set Next_Queue = Next_Queue + 1 where Server_ID = ? and Server_Name = ?', (server_id, server_name))
    db.commit()

@sugarBot.command(pass_context=True, aliases=['Stop'])
async def stop(ctx):
    server_name = str(ctx.guild)
    server_id = ctx.guild.id
    SQL.execute('update Music set Next_Queue = 1 where Server_ID = ? and Server_Name = ?', (server_id, server_name))
    db.commit()
    SQL.execute(f'select Queue_Name from Music where Server_ID="{server_id}" and Server_Name="{server_name}"')
    name_queue = SQL.fetchone()

    queue_infile = os.path.isdir("./Queues")
    if queue_infile is True:
        DIR = os.path.abspath(os.path.realpath("Queues"))
        Queue_Main = os.path.join(DIR, name_queue[0])
        Queue_Main_infile = os.path.isdir(Queue_Main)
        if Queue_Main_infile is True:
            shutil.rmtree(Queue_Main)

    voice = get(sugarBot.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        voice.stop()
        await ctx.send('Music is stopped :stop_sign:')
    else:
        await ctx.send('No music playing failed to stop')

@sugarBot.command(pass_context=True, aliases=['Volume'])
async def volume(ctx, volume: int):
    
    if ctx.voice_client is None:
        return await ctx.send('Not connected to voice channel')

    ctx.voice_client.source.volume = volume / 100
    await ctx.send(f'Changed volume to {volume}%')

@sugarBot.command(pass_context=True, aliases=['Skip'])
async def skip(ctx):
    voice = get(sugarBot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        voice.stop()
        await ctx.send('Music is skipped :track_next:')
    else:
        await ctx.send('No music playing')

sugarBot.run("NzkwMjI1NjA0NTk0MTA2Mzc5.X99g8Q.F9P0_xe7XXvUA6DMF9E3uu6s_RQ")