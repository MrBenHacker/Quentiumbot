import discord, asyncio, psutil, subprocess, time, calendar, requests, urllib.request, json, random, inspect, re, os
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageFile, ImageFilter
from datetime import datetime, timedelta
from icalendar import Calendar
from bs4 import BeautifulSoup

with open("extra/CONFIG.json", "r", encoding="utf-8", errors="ignore") as file:
    config = json.load(file, strict=False)

with open("extra/data.json", "r", encoding="utf-8", errors="ignore") as file:
    data = json.load(file, strict=False)

with open("extra/triggers.json", "r", encoding="utf-8", errors="ignore") as file:
    triggers = json.load(file, strict=False)

with open("extra/translations.json", "r", encoding="utf-8", errors="ignore") as file:
    translations = json.load(file, strict=False)

with open("extra/letters_dict.json", "r", encoding="utf-8", errors="ignore") as file:
    letters = json.load(file, strict=False)

with open("extra/dt_aliases.json", "r", encoding="utf-8", errors="ignore") as file:
    aliases_dt = json.load(file, strict=False)

with open("extra/dt_mines.json", "r", encoding="utf-8", errors="ignore") as file:
    mines = json.load(file, strict=False)

with open("extra/embed_colors.json", encoding="utf-8", errors="ignore") as file:
    colors_embed = json.load(file, strict=False)

def emo(text):
    return str(discord.utils.get(client.emojis, name=text))

async def get_prefix(bot, message):
    if message.guild.id and message.guild.id == 380373195473027074: # Support Quentiumbot server ID
        await asyncio.sleep(1)
    with open("extra/data.json", "r", encoding="utf-8", errors="ignore") as file:
        data = json.load(file, strict=False)
    if data.get(str(message.guild.id)) == None:
        prefixes_list = "+"
    else:
        prefixes_list = data.get(str(message.guild.id))["prefix_server"]
    if not message.guild:
        return "+"
    return commands.when_mentioned_or(prefixes_list)(bot, message)

token_genius = config["GLOBAL"]["token_genius"]
token_weather = config["GLOBAL"]["token_weather"]
token_timezone = config["GLOBAL"]["token_timezone"]
client = commands.Bot(command_prefix=get_prefix,
                      description="Quentium's Private Bot",
                      owner_id=246943045105221633,
                      pm_help=True,
                      help_command=None,
                      case_insensitive=True)

@client.event
async def on_ready():
    global start_time
    print("\n+--------------------------------------------+"
          "\n|            Quentium67Bot ready !           |"
          "\n|           © 2017 - 2019 QuentiumYT         |"
          "\n+--------------------------------------------+\n")
    print("Logged in as %s#%s" % (client.user.name, client.user.discriminator))
    print("ID: " + str(client.user.id))
    start_time = datetime.now()
    print("\nStarting at: " + start_time.strftime("%d.%m.%Y - %H:%M:%S"))
    await client.change_presence(activity=discord.Activity(name="quentium.fr | +help", type=discord.ActivityType.watching), status=discord.Status.dnd)

#----------------------------- SETUP GLOBAL FUNCTIONS AND GLOBAL EVENTS -----------------------------#

async def async_data(server_id, server_name, message_received):
    global data, translations, lang_server, commands_server, autorole_server, prefix_server
    with open("extra/translations.json", "r", encoding="utf-8", errors="ignore") as file:
        translations = json.load(file, strict=False)
    if server_id == 380373195473027074: # Support Quentiumbot server ID
        await asyncio.sleep(1)
    with open("extra/data.json", "r", encoding="utf-8", errors="ignore") as file:
        data = json.load(file, strict=False)
    if any(x == str(server_id) for x in data.keys()):
        lang_server = data[server_id]["lang_server"]
        commands_server = data[server_id]["commands_server"] + 1
        data[server_id]["commands_server"] = commands_server
        autorole_server = data[server_id]["autorole_server"]
        prefix_server = data[server_id]["prefix_server"]
    else:
        lang_server = "fr"
        commands_server = 1
        autorole_server = None
        prefix_server = "+"
        data[server_id] = {"name_server": server_name}
        data[server_id]["lang_server"] = lang_server
        data[server_id]["commands_server"] = commands_server
        data[server_id]["autorole_server"] = autorole_server
        data[server_id]["prefix_server"] = prefix_server
    with open("extra/data.json", "w", encoding="utf-8", errors="ignore") as file:
        json.dump(data, file, indent=4)
    cmd_received = str(message_received.content).replace(prefix_server, "").split()[0]
    translations = translations[lang_server]["help"] # -- cmd_received
    return data, translations, lang_server, commands_server, autorole_server, prefix_server

async def async_weather(args):
    global embed
    if not args:
        embed = discord.Embed(title="Merci de préciser une ville.", color=0x00FFFF)
        return embed
    args = args.replace(" ", "%20")
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + args
    data_weather = requests.get(url + f"&appid={token_weather}&lang=fr").json()
    if "city not found" in str(data_weather):
        embed = discord.Embed(title="La ville n'a pas été trouvée.", color=0x00FFFF)
        return embed
    if not data_weather["coord"]:
        return
    lat, long = str(data_weather["coord"]["lat"]), str(data_weather["coord"]["lon"])
    url = f"http://api.timezonedb.com/v2/get-time-zone?key={token_timezone}&format=json&by=position&lat={lat}&lng={long}"
    try:current_time = requests.get(url).json()["formatted"]
    except:current_time = data_weather["dt"]
    emoji = discord.utils.get(client.emojis, name=str(data_weather["weather"][0]["icon"]))
    condition = data_weather["weather"][0]["main"]
    if condition == "Thunderstorm": condition = "Orage"
    if condition == "Drizzle": condition = "Bruine"
    if condition == "Rain": condition = "Pluie"
    if condition == "Snow": condition = "Neige"
    if condition == "Mist": condition = "Brouillard"
    if condition == "Clear": condition = "Clair"
    if condition == "Clouds": condition = "Nuages"
    if condition == "Tornado": condition = "Tornade"
    if condition == "Haze": condition = "Brume"
    desc = str(data_weather["weather"][0]["description"])
    content = f"{emoji} Condition météo : {condition} - \"{desc.title()}\"\n"
    try:
        content += ":cloud: Nuageux : " + str(data_weather["clouds"]["all"]) + "%\n"
    except:pass
    try:
        content += ":cloud_rain: Volume de pluie (dernières 3h) : " + str(data_weather["rain"]["3h"]) + "L/m²\n"
    except:pass
    try:
        content += ":cloud_snow: Volume de neige (dernières 3h) : " + str(data_weather["snow"]["3h"]) + "L/m²\n"
    except:pass
    temp_celcius = str(round(data_weather["main"]["temp"] - 273.15, 1))
    content += f":thermometer: Température : {temp_celcius}°C\n"
    content += ":sweat_drops: Humidité : " + str(data_weather["main"]["humidity"]) + "%\n"
    wind_speed = data_weather["wind"]["speed"]
    content += f":wind_blowing_face: Vitesse du vent : {float(wind_speed)}m/s - {round(float(wind_speed) * 3.6, 1)}km/h\n\n"
    sunrise_time = datetime.fromtimestamp(int(data_weather["sys"]["sunrise"])).strftime("%H:%M:%S")
    sunset_time = datetime.fromtimestamp(int(data_weather["sys"]["sunset"])).strftime("%H:%M:%S")
    content += f"<:time:475328338542592000> Lever du soleil : {sunrise_time} • Coucher du soleil : {sunset_time} (DST)"
    embed = discord.Embed(title="Météo actuelle à " + data_weather["name"] + " :flag_" + str(data_weather["sys"]["country"]).lower() + ":\n", description=content, color=0x00FFFF)
    embed.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/{emoji.id}.png")
    embed.set_footer(text=f"Date locale : {current_time}", icon_url="https://cdn.discordapp.com/emojis/475328334557872129.png")
    return embed

async def async_do_task():
    global embed
    if int(datetime.today().weekday()) == 5:
        await async_command("python3 extra/menu4tte.py", None)
    #if not int(datetime.today().weekday()) == 5 and not int(datetime.today().weekday()) == 6:
        #await async_command("python3 extra/data4tte.py 130", None)
    await async_weather("Gundershoffen")
    await discord.utils.get(client.get_all_members(), id=395525422680506379).send(embed=embed)
    #await async_weather("Wintershouse")
    #await discord.utils.get(client.get_all_members(), id=246943045105221633).send(embed=embed)
    del embed

async def async_command(args, msg):
    global emo
    if "data4tte" in args or "menu4tte" in args:
        args = args.split()
        subprocess.Popen(["sudo"] + args)
        return
    msg_channel = discord.utils.get(msg.author.guild.channels, id=msg.channel.id)
    if args == "runpc":
        await msg.delete()
        content = emo("pc1") + " Quentium PC\n" + emo("pc2") + " Office PC\n" + emo("pc3") + " Space PC"
        embed = discord.Embed(title=emo("vote") + " Choisissez un ordinateur à démarrer :", description=content, color=0x000000)
        msg = await msg_channel.send(embed=embed)
        for item in ["pc1", "pc2", "pc3"]:
            emo = discord.utils.get(client.emojis, name=item)
            await msg.add_reaction(emo)
        return
    elif args == "setco":
        await msg.delete()
        content = emo("co1") + " ON 19H\n" + emo("co2") + " ON 22H\n" + emo("co3") + " OFF 19H\n" + emo("co4") + " OFF 22H"
        embed = discord.Embed(title=emo("vote") + " Choisissez une action à réaliser pour la connexion :", description=content, color=0x000000)
        msg = await msg_channel.send(embed=embed)
        for item in ["co1", "co2", "co3", "co4"]:
            emo = discord.utils.get(client.emojis, name=item)
            await msg.add_reaction(emo)
        return
    elif "ping" in args:
        return await msg.delete()
    try:
        result = subprocess.check_output("sudo " + args, shell=True, stderr=subprocess.STDOUT)
    except Exception as e:
        result = type(e).__name__ + ": " + str(e)
    try:
        return await msg_channel.send("```autohotkey\n{}\n```".format(result.decode("cp1252")))
    except:
        try:
            return await msg_channel.send("```autohotkey\n{}\n```".format(result.decode("ISO-8859-1")))
        except:
            return await msg_channel.send("```autohotkey\n{}\n```".format(str(result)))

@client.listen()
async def on_message(message):
    global triggers
    try:server_id = message.guild.id
    except:server_id = None

    if client.user.mention == message.content.replace("!", ""):
        server_prefix = data[str(server_id)]["prefix_server"]
        return await message.channel.send(f"Le préfixe du bot est `{server_prefix}`. Utilisez la commande `{server_prefix}help` pour la liste des commandes.")
    if not message.author.bot == True:
        if any(x == str(server_id) for x in triggers.keys()):
            with open("extra/triggers.json", "r", encoding="utf-8", errors="ignore") as file:
                triggers = json.load(file, strict=False)
            if any(x == message.content.lower() for x in triggers[str(server_id)].keys()):
                response = triggers[str(server_id)].get(message.content.lower())
                return await message.channel.send(response)

@asyncio.coroutine
async def loop_repeat():
    await client.wait_until_ready()
    now = datetime.today().replace(microsecond=0)
    num_days_month = calendar.monthrange(int(now.strftime("%y")), int(now.strftime("%m")))[1]
    clock = now.replace(day=now.day, hour=7, minute=0, second=0, microsecond=0)
    if now.hour > clock.hour:
        if int(now.strftime("%d")) == num_days_month:
            clock = now.replace(month=now.month+1, day=1, hour=7, minute=0, second=0, microsecond=0)
        else:
            clock = now.replace(day=now.day+1, hour=7, minute=0, second=0, microsecond=0)
    elif now.hour == clock.hour:
        clock = now.replace(day=now.day+1, hour=7, minute=0, second=0, microsecond=0)
    while not client.is_closed():
        time_now = datetime.today().replace(microsecond=0)
        timer_finished = time_now
        sec_time = int(time_now.strftime("%S"))
        min_time = int(time_now.strftime("%M"))
        hour_time = int(time_now.strftime("%H"))
        day_time = int(time_now.strftime("%d"))
        if sec_time > 55 and sec_time <= 59:
            if min_time == 59:
                if hour_time == 23:
                    if day_time == num_days_month:
                        timer_finished = time_now.replace(month=time_now.month+1, day=1, hour=0, minute=0, second=0)
                    else:
                        timer_finished = time_now.replace(day=time_now.day+1, hour=0, minute=0, second=0)
                else:
                    timer_finished = time_now.replace(hour=time_now.hour+1, minute=0, second=0)
            else:
                timer_finished = time_now.replace(minute=time_now.minute+1, second=0)
        if timer_finished == clock:
            await async_do_task()
            now = datetime.today().replace(microsecond=0)
            if day_time == num_days_month:
                clock = now.replace(month=now.month+1, day=1, hour=7, minute=0, second=0, microsecond=0)
            else:
                clock = now.replace(day=now.day+1, hour=7, minute=0, second=0, microsecond=0)
        await asyncio.sleep(5)

loop = asyncio.get_event_loop()
try:
    client.loop.create_task(loop_repeat())
except:
    loop.run_forever()

@client.event
async def on_raw_reaction_add(ctx):
    if ctx.user_id == 246943045105221633: # Quentium user ID
        user = client.get_user(ctx.user_id)
        server = client.get_guild(ctx.guild_id)
        channel = server.get_channel(ctx.channel_id)
        message = await channel.fetch_message(ctx.message_id)
        if message.embeds and "<:vote:509442482141003776> Choisissez" in message.embeds[0].title:
            await message.remove_reaction(ctx.emoji, user)
            if "ordinateur" in message.embeds[0].title:
                try:emo = ctx.emoji.name
                except:emo = None
                if emo and emo[:2] == "pc":
                    if emo == "pc1":
                        args = "etherwake -i eth0 40:16:7E:AD:F7:21"
                        tmp = await channel.send(str(ctx.emoji) + " Démarrage de ***PC Quentium***")
                    elif emo == "pc2":
                        args = "etherwake -i eth0 40:61:86:93:B7:C7"
                        tmp = await channel.send(str(ctx.emoji) + " Démarrage de ***PC Bureau***")
                    elif emo == "pc3":
                        args = "etherwake -i eth0 40:16:7E:AD:7B:6C"
                        tmp = await channel.send(str(ctx.emoji) + " Démarrage de ***PC Space***")
                    await async_command(args, message)
                    await asyncio.sleep(10)
                    return await tmp.delete()
            if "connexion" in message.embeds[0].title:
                try:emo = ctx.emoji.name
                except:emo = None
                if emo and emo[:2] == "co":
                    try:
                        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
                        password_mgr.add_password(None, "http://192.168.1.100:8080", "admin", config["GLOBAL"]["co_passwd"])
                        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
                        opener = urllib.request.build_opener(handler)
                        urllib.request.install_opener(opener)
                        if emo == "co1":
                            urllib.request.urlopen("http://192.168.1.100:8080/set.cmd?cmd=setpower+p61=1")
                            tmp = await channel.send(str(ctx.emoji) + " Connexion ajoutée jusqu'à ***19h***")
                        elif emo == "co2":
                            urllib.request.urlopen("http://192.168.1.100:8080/set.cmd?cmd=setpower+p62=1")
                            tmp = await channel.send(str(ctx.emoji) + " Connexion ajoutée jusqu'à ***22h***")
                        elif emo == "co3":
                            urllib.request.urlopen("http://192.168.1.100:8080/set.cmd?cmd=setpower+p61=0")
                            tmp = await channel.send(str(ctx.emoji) + " Connexion enlevée de ***19h***")
                        elif emo == "co4":
                            urllib.request.urlopen("http://192.168.1.100:8080/set.cmd?cmd=setpower+p62=0")
                            tmp = await channel.send(str(ctx.emoji) + " Connexion enlevée de ***22h***")
                        await asyncio.sleep(10)
                        return await tmp.delete()
                    except:
                        return await channel.send("Le site n'a pas pu répondre (No route to host)")

@client.event
async def on_member_join(member):
    global autorole_server
    server_id = member.guild.id

    if server_id == 247350494702338048: # UnityNetwork server ID
        autorole_server = None
        try:
            with open("extra/data.json", "r", encoding="utf-8", errors="ignore") as file:
                data = json.load(file, strict=False)
            autorole_server = data[str(server_id)]["autorole_server"]
            prefix_server = data[str(server_id)]["prefix_server"]
        except:pass

        if autorole_server:
            if member.activity:
                print("ok")
                if "counter" in member.activity.name.lower():
                    role = discord.utils.get(member.guild.roles, id=autorole_server.split("/")[0])
                elif "payday" in member.activity.name.lower():
                    role = discord.utils.get(member.guild.roles, id=autorole_server.split("/")[1])
                elif "minecraft" in member.activity.name.lower():
                    role = discord.utils.get(member.guild.roles, id=autorole_server.split("/")[2])
                elif "rocket" in member.activity.name.lower():
                    role = discord.utils.get(member.guild.roles, id=autorole_server.split("/")[3])
                elif "fortnite" in member.activity.name.lower():
                    role = discord.utils.get(member.guild.roles, id=autorole_server.split("/")[4])
                elif "overwatch" in member.activity.name.lower():
                    role = discord.utils.get(member.guild.roles, id=autorole_server.split("/")[5])
                else:
                    role = None
                print(role)
                if not role:
                    await member.add_roles(role)
                    msg = "`" + member.name + "` à reçu le rôle `" + role.name + "` automatiquement !"
                    channel = [x.id for x in member.guild.channels if str(x.name) == "bots"][0]
                    await discord.utils.get(member.guild.channels, id=channel).send(msg)

        msg = f"Bienvenue {member.mention} sur ***{member.guild.name}*** !\n"
        msg += f"Tu peux demander les rôles qui te concernent à un admin et utiliser le QuentiumBot avec la commande `{prefix_server}help`.\nHave fun :slight_smile: !"
        channel = [x.id for x in member.guild.channels if str(x.name) == "bots"][0]
        return await discord.utils.get(member.guild.channels, id=channel).send(msg)

@client.event
async def on_member_remove(member):
    if member.guild.id == 247350494702338048: # UnityNetwork server ID
        msg = "**" + member.name + "** vient de quitter le serveur :worried:"
        channel = [x.id for x in member.guild.channels if str(x.name) == "bots"][0]
        return await discord.utils.get(member.guild.channels, id=channel).send(msg)

@client.event
async def on_command_error(ctx, error):
    if "is not found" in str(error):
        return
    elif "FORBIDDEN (status code: 403): Missing Permissions" in str(error):
        return await ctx.send(":x: Il manque certaines permissions au bot.")
    elif "FORBIDDEN (error code: 50013): Missing Permissions" in str(error):
        return await ctx.send(":x: Il manque certaines permissions au bot.")
    elif "FORBIDDEN (status code: 403): Missing Access" in str(error):
        return await ctx.send(":x: Il manque certains accès au bot.")
    elif "NotFound: 404 NOT FOUND (error code: 10008): Unknown Message" in str(error):
        return await ctx.send(":x: Discord ne trouve pas l'un des messages.")
    elif "Cannot send an empty message" in str(error):
        return await ctx.message.delete()
    elif "BAD REQUEST (status code: 400): You can only bulk delete messages that are under 14 days old." in str(error):
        return await ctx.send(":x: Vous ne pouvez que supprimer les messages datant de moins de 14 jours :pensive:")
    elif isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send(":x: Un argument requis manque :rolling_eyes:")
    elif isinstance(error, commands.NoPrivateMessage):
        return await ctx.send(":x: Cette commande ne peut pas être utilisée en message privés :confused:")
    elif isinstance(error, commands.DisabledCommand):
        return await ctx.send(":x: Cette commande à été désactivée :confounded:")
    elif isinstance(error, commands.BadArgument):
        return await ctx.send(":x: Un mauvais argument à été donné :slight_frown:")
    elif isinstance(error, commands.TooManyArguments):
        return await ctx.send(":x: Trop d'arguments ont été donnés :scream:")
    elif isinstance(error, commands.CommandOnCooldown):
        time_left = str(error).split("Try again in ", 1)[1].split(".", 1)[0]
        return await ctx.send(":x: Doucement, il y a un cooldown sur cette commande, il vous reste " + time_left + "sec à attendre :raised_hand:")

#----------------------------- INFORMATIONS COMMANDS -----------------------------#

@client.command(pass_context=True, aliases=["cmd", "aide"])
async def help(ctx, *, args=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global translations, server_id, server_name, prefix_server
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        commands_type = ["infos_", "utilities_", "stats_", "feedback_", "admin_configs_", "admin_rights_"]
        commands_type_special = ["flc_", "theswe_", "ism_"]
        commands_type_special_id = ["371687157817016331", "199189022894063627", "391272643229384705"]
        if not args:
            commands_type_emoji = ["informations", "utilities", "statistics", "feedback", "admin_configs", "admin_rights", "serv_flc", "serv_theswe", "serv_ism"]
            commands_title = [translations[x] for x in translations.keys() if "msg_title_" in x]
            embed = discord.Embed(title=translations["msg_list_commands"], url=translations["url_website_discord"], color=0x00ff00)
            for cmds_type in range(len(commands_type)):
                embed_type = [x for x in translations.keys() if commands_type[cmds_type] in x]
                embed_var = ""
                for command in embed_type:
                    command_desc = translations[command]["description"]
                    command_usage = translations[command]["usage"]
                    embed_var += f"- `{prefix_server}{command.replace(commands_type[cmds_type], '')}{command_usage}` > {command_desc}\n"
                embed.add_field(name=emo(commands_type_emoji[cmds_type]) + commands_title[cmds_type], value=embed_var, inline=True)
            for cmds_type in range(len(commands_type_special)):
                embed_type = [x for x in translations.keys() if commands_type_special[cmds_type] in x]
                embed_var = ""
                if str(ctx.message.guild.id) == commands_type_special_id[cmds_type]:
                    for command in embed_type:
                        command_desc = translations[command]["description"]
                        command_usage = translations[command]["usage"]
                        embed_var += f"- `{prefix_server}{command.replace(commands_type_special[cmds_type], '')}{command_usage}` > {command_desc}\n"
                    index = len(commands_type) + int(cmds_type / 2) + 1
                    embed.add_field(name=emo(commands_type_emoji[index]) + commands_title[index], value=embed_var, inline=True)
            if ctx.message.author.id == 246943045105221633: # Quentium user ID
                embed_type = [x for x in translations.keys() if "quentium_" in x]
                embed_var = ""
                for command in embed_type:
                    command_desc = translations[command]["description"]
                    command_usage = translations[command]["usage"]
                    embed_var += f"- `{prefix_server}{command.replace('quentium_', '')}{command_usage}` > {command_desc}\n"
                embed.add_field(name=emo("user_quentium") + commands_title[-1], value=embed_var, inline=True)
            donation = translations["msg_donation"].format("https://www.paypal.me/QLienhardt")
            embed.add_field(name=translations["msg_caption"], value=translations["msg_caption_desc"], inline=True)
            embed.add_field(name=translations["msg_warning"], value=translations["msg_warning_desc"] + donation, inline=True)
            embed.set_footer(text=translations["msg_more_infos"], icon_url=translations["url_logo_bot"])
        else:
            all_commands = []
            commands_type += commands_type_special
            commands_keys = [x for x in translations.keys() if any([y in x for y in commands_type])]
            for types in commands_type:
                all_commands += [x.split(types)[1] for x in translations.keys() if types in x]
            for types_aliases in commands_keys:
                all_commands += [x for x in translations[types_aliases]["aliases"].split(" / ") if not x == ""]

            if any(x.lower() == args.lower() for x in all_commands):
                if any([x for x in commands_keys if args in translations[x]["aliases"]]):
                    command_type = [y for y in commands_keys if any([args in x for x in translations[y]["aliases"].split(" / ")])][0]
                else:
                    command_type = [x for x in commands_keys if args in x][0]
                command_desc = translations[command_type]["description"]
                command_usage = translations[command_type]["usage"]
                command_aliases = [command_type.split("_")[1]] + translations[command_type]["aliases"].split(" / ")
                desc_text = f"```{args}```\n**{command_desc}**\n\n"
                if translations[command_type]["aliases"]:
                    desc_text += f"**{translations['msg_aliases']}** `{'`, `'.join(command_aliases)}`\n\n\n"
                else:
                    desc_text += "\n"
                desc_text += f"{translations['msg_format']} `{prefix_server}{args} {command_usage}`"
                embed = discord.Embed(title=None, description=desc_text, color=0x03A678)
            else:
                return await ctx.send(translations["msg_no_command_found"])
        return await ctx.send(embed=embed)

@client.command(pass_context=True)
async def help_old(ctx):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name, prefix_server
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        commands_user = """
    - `help / cmd` > Affiche la liste des commandes.
    - `letter / lettre ["texte"]` > Ecris un message avec des émojis.
    - `embed [T="titre"] [D="description"] [C="couleur"] [I="imageurl"] [F="footer" / None] [U="url"] [A="auteur"]` > Affiche un embed.
    - `listinvites` > Affiche la liste des liens d'invitation.
    - `msgtotal [all / channel] [@membre]` > Calcule le nombre de messages d'un membre au total ou dans le salon.
    - `lyrics ["musique"]` > Recherche les paroles d'une musique.
    - `weather ["ville"]` > Affiche la météo de la ville spécifiée.
    - `serverstats` > Montre les statistiques du serveur.
    - `userstats [@membre]` > Montre les statistiques d'un membre.
    - `botstats` > Montre les statistiques du bot.
    - `share` > Partage le lien d'invitation du serveur.
    - `shareme` > Invite le bot sur ton serveur.
    - `ping` > Calcule le temps de réactivité du bot.
    - `move ["numéro salon"]` > Déplace les membres dans le salon vocal sélectionné."""
        commands_admin = """
    - `clear ["nombre"]` > Supprime un nombre défini de messages.
    - `kick [@membre]` > Expulse la personne mentionnée.
    - `ban [@membre]` > Bannis la personne mentionnée.
    - `autorole ["nom du role" / show / remove]` > Donne un rôle automatiquement à quelqu'un lorsqu'il rejoins le serveur."""
        commands_quentium = """
    - `showideas` > Affiche la liste des idées.
    - `addlogs ["texte"]` > Permet d'ajouter des logs de mise à jour.
    - `data4tte ["nombre"]` > Envoie des requêtes au projet (timetoeat.xyz).
    - `exec ["texte"]` > Execute des commandes sur la Raspberry (^.^).
    - `eval ["texte"]` > Evalue des données pour Python (^.^).
    - `dtmine ["minerais"]` > Affiche les 10 meilleurs endroits pour miner une ressource (©Fomys :smile:)."""
        commands_feedback = """
    - `idea / bug ["texte"]` > Propose une idée ou reporte un bug pour améliorer le bot.
    - `showlogs` > Affiche la liste des mises à jour du bot.

    Légende : `[argument]` - `["argument donné"]` (Enlevez les guillemets) - `[@mention]` - `[choix / "mon_choix"]`
    :warning: Si vous rencontrez un problème, merci de la soumettre avec la commande `+bug` ou en rejoignant le serveur de test : https://discord.gg/5sehgXx\n"""
        end_text = ":euro: Pour une petite donation : [Cliquez ici]({})".format("https://www.paypal.me/QLienhardt")
        embed = discord.Embed(title="----- Liste des Commandes -----", url="https://quentium.fr/discord/", color=0x00ff00)
        embed.add_field(name=":video_game: Commandes **UTILISATEUR** :", value=commands_user, inline=True)
        embed.add_field(name=":cop: Commandes **ADMIN** :", value=commands_admin, inline=True)
        if ctx.message.author.id == 246943045105221633:
            embed.add_field(name=":eyes: Commandes **QUENTIUM** :", value=commands_quentium, inline=True)
        embed.add_field(name=":incoming_envelope: Commandes **SUPPORT / FEEDBACK** :", value=commands_feedback + end_text, inline=True)
        embed.set_footer(text="Pour plus d'informations, veuillez visiter le site : https://quentium.fr/discord/", icon_url="https://quentium.fr/+img/logoBot.png")
        return await ctx.send(embed=embed)

@client.command(pass_context=True, no_pm=True, aliases=["listeinvites", "invitelist"])
async def listinvites(ctx):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        list_invites = await ctx.guild.invites()
        if list_invites:
            content = "\n- ".join([x.url for x in list_invites])
        else:
            content = "Aucuns"
        embed = discord.Embed(title="Liens d'invitation :", description="- " + content, color=0x00FFFF)
        return await ctx.send(embed=embed)

@client.command(pass_context=True, no_pm=True, aliases=["listebans", "banlist"])
async def listbans(ctx):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        list_banned = await ctx.guild.bans()
        if list_banned:
            content = "\n- ".join([x[1].name for x in list_banned])
        else:
            content = "Aucun"
        embed = discord.Embed(title="Liste des membres bannis :", description="- " + content, color=0xFF0000)
        return await ctx.send(embed=embed)

@client.command(pass_context=True, aliases=["invite"])
async def share(ctx):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        return await ctx.send(":arrow_right: Lien direct : https://discord.gg/PGepHZW\n:arrow_right: Lien à copier : ```https://discord.gg/PGepHZW```")

@client.command(pass_context=True, aliases=["sharebot", "invitebot"])
async def shareme(ctx):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        return await ctx.send("Tu peux partager ce lien pour m'inviter sur d'autres serveurs :\n" + config["PRIVATE"]["invite"])

#----------------------------- UTILITIES COMMANDS -----------------------------#

@client.command(pass_context=True, aliases=["totalmsg"])
async def msgtotal(ctx, *args):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        if not ctx.message.channel.guild.me.guild_permissions.administrator:
            return await ctx.send(":x: Il manque la permissions **Administrateur** au bot.")
        if len(args) == 2:
            member = discord.utils.get(client.get_all_members(), id=str(args[1])[2:-1])
            args = args[0]
        elif len(args) == 1:
            args = args[0]
            if str(args)[2:-1].isdigit():
                member = discord.utils.get(client.get_all_members(), id=str(args)[2:-1])
                args = "all"
            elif not args == "all" and not args == "channel":
                return await ctx.send(f"Merci de préciser un argument valide : `{prefix_server}msgtotal [all / channel] [@membre]`.")
            else:
                member = ctx.message.author
        else:
            member = ctx.message.author
            args = "all"

        if not isinstance(ctx.channel, discord.TextChannel):
            args = "channel"
        counter = 0
        embed = discord.Embed(title="Calcul des messages...", color=0xFFA500)
        tmp = await ctx.send(embed=embed)
        if args == "":args = "all"
        if args == "all":
            msg_total = True
            channel_list = [x for x in ctx.message.guild.channels if isinstance(x, discord.TextChannel)]
            for channel in channel_list:
                async for log in channel.history(limit=1000000):
                    if log.author == member:
                        counter += 1
        elif args == "channel":
            msg_total = False
            async for log in ctx.message.channel.history(limit=1000000):
                if log.author == member:
                    counter += 1
        else:
            await tmp.delete()
            return await ctx.send(f"Merci de préciser un argument valide : `{prefix_server}msgtotal [all / channel] [@membre]`.")

        embed = discord.Embed(title="Nombre de messages :", color=0xFFA500)
        if msg_total == True:
            embed.add_field(name="--------------------------", value="**" + str(member) + "** a envoyé **" + str(counter) + "** messages au total.", inline=True)
        else:
            embed.add_field(name="--------------------------", value="**" + str(member) + "** a envoyé **" + str(counter) + "** messages dans ce channel.", inline=True)
        embed.set_footer(text=f"Demandé par : {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        if not isinstance(ctx.channel, discord.TextChannel):
            return await tmp.edit(embed=embed)
        await tmp.edit(embed=embed)
        await asyncio.sleep(5)
        return await ctx.message.delete()

@client.command(name="embed", pass_context=True, aliases=["embeds", "richembed"])
async def _embed(ctx, *, args=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        def random_color():
            r = lambda: random.randint(0, 255)
            return "0x%02X%02X%02X" % (r(),r(),r())

        if not args:
            return await ctx.send(f"Merci de préciser un argument valide : `{prefix_server}embed T=Titre D=Description C=Couleur I=ImageURL F=Footer U=URL A=Auteur`.")

        content = re.split(".=", args)[1:]
        content = [x.strip() for x in content]
        sep = re.findall(".=", args)
        title = description = color = thumbnail = footer = url = author = None
        for x in range(len(sep)):
            if "T=" == sep[x]:title = content[x]
            if "D=" == sep[x]:description = content[x]
            if "C=" == sep[x]:color = content[x]
            if "I=" == sep[x]:thumbnail = content[x]
            if "F=" == sep[x]:footer = content[x]
            if "U=" == sep[x]:url = content[x]
            if "A=" == sep[x]:author = content[x]
        if all(x is None for x in [title, description, color, thumbnail, footer, url, author]):
            if len(args) <= 255:
                title = args
            else:
                title = None
                description = args
        if not title:
            if description and len(args) <= 255:
                title = description
                description = None
        if color == "random":
            color = int(random_color(), 16)
        elif color is not None:
            if any([x for x in colors_embed.keys() if x == color]):
                color = int(colors_embed[color], 16)
            else:
                if color.isdigit():
                    if int(color) >= 16777215:
                        color = 16777215
                else:
                    try:
                        color = int("0x" + color, 16)
                        if color >= 16777215:
                            color = 16777215
                    except:
                        return await ctx.send("La couleur mentionnée n'existe pas. Paramètres supportés : `nom couleur`, `valeur hexa`, `valeur nombre entier`, `random`.")
        else:
            color = int(random_color(), 16)
        embed = discord.Embed(title=title, description=description, color=color, url=url)
        if thumbnail:
            if "image/" in str(requests.get(thumbnail).headers):
                embed.set_thumbnail(url=thumbnail)
        if author:
            embed.set_author(name=author)
        if footer:
            if not footer == "None":
                embed.set_footer(text=footer)
        else:
            embed.set_footer(text=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        return await ctx.send(embed=embed)

@client.command(pass_context=True, aliases=["lettre", "emojis", "emoji"])
async def letter(ctx, *, args=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        if not args:
            return await ctx.send("Merci de préciser un texte.")
        lst = []
        emojis_used = re.findall(r"<\w*:\w*:\d*>", args)
        emojis_temp = []
        if emojis_used:
            for emoji in emojis_used:
                if int(emoji.split(':', 2)[2].split('>')[0]) in [x.id for x in client.emojis]:
                    args = args.replace(emoji, "☺") # Custom emoji
                else:
                    args = args.replace(emoji, "☻")
                    emojis_temp.append(emoji)
        for emojis in emojis_temp:
            emojis_used.remove(emojis)
        is_mention = re.findall(r"<@\d*>", args)
        for mention in is_mention:
            args = args.replace(mention, str(discord.utils.get(client.get_all_members(), id=int(mention[2:-1])).name))
        letter = list(str(args.lower()))
        for char in range(len(letter)):
            if any(x == letter[char] for x in letters.keys()):
                if "emo(" in letters[letter[char]]:
                    lst += emo(letters[letter[char]].replace("emo(","")[0:-1])
                else:
                    lst += letters[letter[char]]
            elif any(x in letter[char] for x in ["â","ä","à","å"]):lst += ":regional_indicator_a:"
            elif any(x in letter[char] for x in ["ê","ë","è","é"]):lst += ":regional_indicator_e:"
            elif any(x in letter[char] for x in ["î","ï","ì","í"]):lst += ":regional_indicator_i:"
            elif any(x in letter[char] for x in ["ô","ö","ò","ó"]):lst += ":regional_indicator_o:"
            elif any(x in letter[char] for x in ["û","ü","ù","ú"]):lst += ":regional_indicator_u:"
            elif letter[char].isalpha() == True:
                lst += ":regional_indicator_" + letter[char] + ":"
            elif letter[char] == "☺":
                lst.append(str(emojis_used[0]))
                del emojis_used[0]
            else:
                lst.append(letter[char])
        content = "".join(lst)
        comb = lambda s,n: [s[i:i+n] for i in range(0,len(s),n)]
        embeds_temp = comb(content, 2019)
        embeds = []
        cut_end_embed = [""]
        for x in embeds_temp:
            full_embed = re.split(r"(<\w*:\w*:\d*>|:)", x)[:-2]
            embeds.append("".join(cut_end_embed + full_embed))
            cut_end_embed = re.split(r"(<\w*:\w*:\d*>|:)", x)[-2:]
        embeds[-1] = embeds[-1] + "".join(cut_end_embed)
        for content in embeds:
            embed = discord.Embed(title=None, description=content, color=0xFFA952)
            if content == embeds[-1]:
                embed.set_footer(text=f"Demandé par : {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
                return await ctx.send(embed=embed)
            await ctx.send(embed=embed)

@client.command(pass_context=True, aliases=["meteo"])
async def weather(ctx, *, args=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        global embed
        await async_weather(args)
        await ctx.send(embed=embed)
        del embed

@client.command(pass_context=True, aliases=["lyric", "paroles", "parole", "l"])
async def lyrics(ctx, *, args):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        if not args:
            return await ctx.send("Merci de préciser une musique.")
        request_uri = "https://api.genius.com/search/"
        params = {"q": args}
        headers = {"Authorization": "Bearer " + token_genius}
        r = requests.get(request_uri, params=params, headers=headers).json()

        if not r["response"]["hits"]:
            return await ctx.send("La musique n'a pas été trouvée ou n'existe pas.")
        path_lyrics = r["response"]["hits"][0]["result"]["path"]
        URL = "https://genius.com" + path_lyrics
        page = requests.get(URL)
        html = BeautifulSoup(page.text, "html.parser")

        try:lyrics = html.find("div", class_="lyrics").get_text()
        except:return await ctx.send("La musique demandée ne contient pas de paroles.")
        if len(lyrics) > 5900:
            return await ctx.send("Le résultat est trop long (limite discord). Cela peut être aussi causé par l'absence de lyrics de vôtre recherche.")
        title = r["response"]["hits"][0]["result"]["full_title"]
        image = r["response"]["hits"][0]["result"]["header_image_url"]
        if not any(x.lower() in title.lower() for x in args.split()):
            await ctx.send("La recherche ne correspond pas au titre, assurez vous d'avoir bien entré le nom de la musique.")
            await ctx.send(f"Résultat trouvé avec : **{args}**")
        embed = discord.Embed(title=f"Paroles de : __**{title}**__", description=None, color=0x00FFFF)
        embed.set_thumbnail(url=image)
        for block in lyrics.split("\n\n")[1:-1]:
            splitted = block.split("\n", 1)
            if not splitted[0] is "":
                if not len(splitted) == 1:
                    if len(splitted[1]) >= 1024:
                        embed.add_field(name=splitted[0], value=splitted[1][0:1023])
                    else:
                        embed.add_field(name=splitted[0], value=splitted[1])
                else:
                    embed.add_field(name=splitted[0], value=":notes:"*6)
        embed.set_footer(text=f"Demandé par : {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        return await ctx.send(embed=embed)

@client.command(pass_context=True, aliases=["av", "avatars"])
async def avatar(ctx, *, member : discord.Member=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        if not member:
            member = ctx.message.author
        icon = str(member.avatar_url)
        icon1 = icon.split(".", 999)
        icon2 = "".join(icon1[len(icon1) - 1])
        icon3 = icon.replace(icon2, "")
        avatar_url = icon3 + "png?size=1024"
        title = member.name + "#" + member.discriminator
        content = "[Avatar URL]({})".format(avatar_url)
        embed = discord.Embed(title=f"**{title}**", description=content, color=0x15f2c6)
        embed.set_image(url=avatar_url)
        embed.set_footer(text=f"Demandé par : {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        return await ctx.send(embed=embed)

#----------------------------- STATISTICS COMMANDS -----------------------------#

@client.command(pass_context=True, no_pm=True, aliases=["statsuser", "statuser"])
async def userstats(ctx, *, member : discord.Member=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        if not member:
            member = ctx.message.author
        user_name = member.name
        user_nickname = "Aucun" if member.nick == None else str(member.nick)
        user_id = str(member.id)
        user_tag = member.name + "#" + member.discriminator
        user_mention = member.mention
        user_is_bot = "Oui" if member.bot == True else "Non"
        status = str(member.status).lower()
        if status == "online":
            user_status = "En ligne"
        elif status == "offline":
            user_status = "Hors ligne"
        elif status == "idle":
            user_status = "Absent"
        elif status == "dnd":
            user_status = "Ne pas déranger"
        elif status == "invisible":
            user_status = "Invisible"
        user_game = "Aucun" if member.activity == None else str(member.activity.name)
        user_joinserv = datetime.strptime(str(member.joined_at)[:-7], "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y - %H:%M:%S")
        user_joindiscord = datetime.strptime(str(member.created_at)[:-7], "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y - %H:%M:%S")
        user_best_role = str(member.top_role)
        user_roles = str(len([x.name for x in member.roles]))
        user_roles_list = ", ".join([x.name for x in member.roles])

        embed = discord.Embed(color=0x0026FF)
        icon = str(member.avatar_url)
        icon1 = icon.split(".", 999)
        icon2 = "".join(icon1[len(icon1) - 1])
        icon3 = icon.replace(icon2, "")
        avatar_url = icon3 + "png?size=1024"
        embed.set_thumbnail(url=avatar_url)
        content =   "```autohotkey\n" \
                    "Nom:                %s\n" \
                    "Surnom:             %s\n" \
                    "ID:                 %s\n" \
                    "Tag:                %s\n" \
                    "Mention:            %s\n" \
                    "Bot:                %s\n" \
                    "Status:             %s\n" \
                    "Jeu:                %s\n" \
                    "Rejoins serveur le: %s\n" \
                    "Rejoins discord le: %s\n" \
                    "Meilleur Rôle:      %s\n" \
                    "Rôles:              %s\n" \
                    "%s" \
                    "```" % (user_name, user_nickname, user_id, user_tag, user_mention, user_is_bot, user_status,
                            user_game, user_joinserv, user_joindiscord, user_best_role, user_roles, user_roles_list)
        embed.add_field(name="Statistiques de __***" + user_name + "***__", value=content + " ***[Lien Icône]({})***".format(avatar_url), inline=True)
        embed.set_footer(text=f"Demandé par : {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        return await ctx.send(embed=embed)

@client.command(pass_context=True, no_pm=True, aliases=["serveurstats", "statsserveur", "statserveur", "statserver", "statsserver", "servstats"])
async def serverstats(ctx):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        serv = ctx.message.guild
        serv_name = serv.name
        serv_id = str(serv.id)
        serv_owner = serv.owner.name
        serv_owner_dis = "#" + serv.owner.discriminator
        serv_created = datetime.strptime(str(serv.created_at)[:-7], "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y - %H:%M:%S")
        serv_region = serv.region
        serv_members = str(len(serv.members))
        serv_members_on = str(len([x for x in serv.members if not x.status == discord.Status.offline]))
        serv_users = str(len([x for x in serv.members if not x.bot]))
        serv_users_on = str(len([x for x in serv.members if not x.bot and not x.status == discord.Status.offline]))
        serv_bots = str(len([x for x in serv.members if x.bot]))
        serv_bots_on = str(len([x for x in serv.members if x.bot and not x.status == discord.Status.offline]))
        serv_channels = str(len([x for x in serv.channels if not isinstance(x, discord.CategoryChannel)]))
        serv_text_channels = str(len([x for x in serv.channels if isinstance(x, discord.TextChannel)]))
        serv_voice_channels = str(len([x for x in serv.channels if isinstance(x, discord.VoiceChannel)]))
        serv_afk_channel = "Aucun" if serv.afk_channel == None else str(serv.afk_channel)
        serv_afk_time = str(round(int(serv.afk_timeout) / 60))
        verif = str(serv.verification_level)
        if verif == "none":
            serv_verif_lvl = "Aucun"
        elif verif == "low":
            serv_verif_lvl = "Faible"
        elif verif == "medium":
            serv_verif_lvl = "Moyen"
        elif verif == "high":
            serv_verif_lvl = "Elevé"
        elif verif == "extreme":
            serv_verif_lvl = "Extrême"
        serv_roles = str(len([x.name for x in serv.roles]))
        serv_roles_list = ", ".join([x.name for x in serv.roles])

        embed = discord.Embed(url="https://quentium.fr/discord/", color=0x0026FF)
        icon = str(serv.icon_url)
        icon1 = icon.split(".", 999)
        icon2 = "".join(icon1[len(icon1) - 1])
        icon3 = icon.replace(icon2, "")
        icon_url = icon3 + "png?size=1024"
        if len(serv.icon_url):
            embed.set_thumbnail(url=icon_url)
        else:
            embed.set_thumbnail(url="https://quentium.fr/+img/interrogation.png")
        content =   "```autohotkey\n" \
                    "Nom:                %s\n" \
                    "ID:                 %s\n" \
                    "Propriétaire:       %s (%s)\n" \
                    "Crée le:            %s\n" \
                    "Région:             %s\n" \
                    "Membres:            %s (%s En ligne)\n" \
                    "    Personnes:      %s (%s En ligne)\n" \
                    "    Bots:           %s (%s En ligne)\n" \
                    "Salons:             %s\n" \
                    "    Textuels:       %s\n" \
                    "    Vocaux:         %s\n" \
                    "Salon AFK:          %s\n" \
                    "Temps AFK:          %s min\n" \
                    "Niveau vérif:       %s\n" \
                    "Rôles:              %s\n" \
                    "%s" \
                    "```" % (serv_name, serv_id, serv_owner, serv_owner_dis, serv_created, serv_region, serv_members,
                            serv_members_on, serv_users, serv_users_on, serv_bots, serv_bots_on, serv_channels, serv_text_channels,
                            serv_voice_channels, serv_afk_channel, serv_afk_time, serv_verif_lvl, serv_roles, serv_roles_list)
        embed.add_field(name="Statistiques du serveur __***" + serv_name + "***__", value=content + " ***[Lien Icône]({})***".format(icon_url), inline=True)
        embed.set_footer(text=f"Demandé par : {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        return await ctx.send(embed=embed)

@client.command(pass_context=True, aliases=["botstat", "statsbot", "statbot"])
async def botstats(ctx):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name, start_time, commands_server
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        bot_host = "Raspberry Pi 3"
        bot_owner = "QuentiumYT#0207"
        bot_version = "Debian 8.0 (Raspbian)"
        time = round((datetime.now() - start_time).total_seconds())
        m, s = divmod(int(time), 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        bot_uptime = "%s Jours, %s Heures, %s Minutes, %s Secondes." % (d, h, m, s)
        bot_memory = int(psutil.virtual_memory()[0] / int(2 ** 20)) - int(psutil.virtual_memory()[4] / int(2 ** 20))
        if isinstance(ctx.channel, discord.TextChannel):
            bot_commands_get = commands_server
        else:
            bot_commands_get = "Indisponible en MP"
        bot_commands_get_total = 0
        for serv in data.keys():
            bot_commands_get_total += data[serv]["commands_server"]
        users = 0
        for serv in client.guilds:
            users += len(serv.members)
        bot_lang_fr = bot_lang_en = bot_lang_de = 0
        for serv in data.keys():
            if "fr" in data[serv]["lang_server"]:
                bot_lang_fr += 1
            elif "en" in data[serv]["lang_server"]:
                bot_lang_en += 1
            elif "de" in data[serv]["lang_server"]:
                bot_lang_de += 1

        embed = discord.Embed(url="https://quentium.fr/discord/", color=0x0026FF)
        embed.set_thumbnail(url="https://quentium.fr/+img/logoBot.png")
        content =   "```autohotkey\n" \
                    "Hébergée sur:         %s\n" \
                    "Propriétaire:         %s\n" \
                    "Linux version:        %s\n" \
                    "Durée fonctionnement: %s\n" \
                    "Mémoire utilisée:     %s Mo\n" \
                    "Commandes reçues:     %s (serveur)\n" \
                    "Commandes reçues:     %s (total)\n" \
                    "Serveurs FR:          %s\n" \
                    "Serveurs EN:          %s\n" \
                    "Serveurs DE:          %s\n" \
                    "```" % (bot_host, bot_owner, bot_version, bot_uptime, bot_memory, bot_commands_get,
                            bot_commands_get_total, bot_lang_fr, bot_lang_en, bot_lang_de)
        embed.add_field(name="Statistiques du __***QuentiumBot***__", value=content, inline=True)
        embed.set_footer(text=f"Demandé par : {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        return await ctx.send(embed=embed)

@client.command(pass_context=True, aliases=["timeup", "runningtime", "runtime", "timerun"])
async def uptime(ctx):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name, start_time
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        time = round((datetime.now() - start_time).total_seconds())
        m, s = divmod(int(time), 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        bot_uptime = f"{d} Jours, {h} Heures, {m} Minutes, {s} Secondes."
        return await ctx.send("Le bot est en ligne depuis " + bot_uptime)

@client.command(pass_context=True, aliases=["pong"])
async def ping(ctx):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        before = time.perf_counter()
        await ctx.trigger_typing()
        ping = round((time.perf_counter() - before) * 500)
        before = time.monotonic()
        tmp = await ctx.send("***Ping message***")
        ping1 = round((time.monotonic() - before) * 500)
        await tmp.delete()
        return await ctx.send(f":ping_pong: Pong!\n- Latence du Bot : `{ping}ms`\n- Latence d'envoi de message : `{ping1}ms`")

#----------------------------- FEEDBACK COMMANDS -----------------------------#

@client.command(pass_context=True, aliases=["bug", "bugs", "ideas", "idee"])
@commands.cooldown(2, 30, commands.BucketType.channel)
async def idea(ctx, *, args=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        cmd_received = str(ctx.message.content).replace("+", "").split()[0]
        if not args:
            if cmd_received == "idea":
                return await ctx.send("Merci de préciser une idée.")
            elif cmd_received == "bug":
                return await ctx.send("Merci de préciser un bug.")
        ideas = " --- ".join([ctx.message.author.name, cmd_received, args])
        with open("feedback.txt", "a", encoding="utf-8", errors="ignore") as file:
            file.write(ideas + "\n")
        return await ctx.send("Merci de contribuer à l'amélioration du bot !")

@client.command(pass_context=True, aliases=["logs", "showlog", "changelog", "whatsnew", "whatnew"])
async def showlogs(ctx):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        embed = discord.Embed(title="Logs de mise à jour du bot :", url="https://quentium.fr/discord/", color=0xFFFF00)
        counter = 1
        with open("extra/logs.txt", "r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                line_time = line.split(" --- ", 999)[0]
                line_content = line.split(" --- ", 999)[1]
                embed.add_field(name="#" + str(counter) + " / " + line_time, value=line_content.replace("..", ".\n"), inline=True)
                counter += 1
        embed.set_footer(text="Les logs sont publiées dès qu'une nouvelle mise à jour importante du bot a lieu.", icon_url="https://quentium.fr/+img/logoBot.png")
        return await ctx.send(embed=embed)

#----------------------------- ADMIN_CONFIGS COMMANDS -----------------------------#

@client.command(pass_context=True, no_pm=True, aliases=["triggers", "reaction", "customreaction", "customtrigger"])
async def trigger(ctx, *, args=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        global triggers
        if not ctx.message.author.guild_permissions.administrator:
            if not args:
                return await ctx.send(f":x: {ctx.message.author.name}, vous n'avez pas la permission **Administrateur** !")
            else:
                if any(x in args.lower() for x in ["list", "liste"]):
                    if any(x == str(server_id) for x in triggers.keys()) and triggers[str(server_id)]:
                        content = "\n- ".join([x for x in triggers[str(server_id)].keys()])
                        embed = discord.Embed(title=f"Réactions customisées ({len(triggers[str(server_id)].keys())}) :", description="- " + content, color=0xBFFF00)
                    else:
                        embed = discord.Embed(title="Il n'y à aucunes réactions customisées.", color=0xBFFF00)
                    return await ctx.send(embed=embed)
                else:
                    return await ctx.send(f":x: {ctx.message.author.name}, vous n'avez pas la permission **Administrateur** !")

        if not args:
            embed = discord.Embed(title=f"Veuillez préciser un déclencheur et une réponse : `{prefix_server}trigger [\"déclancheur\" / liste / remove] [\"réponse\" / url]`", color=0xBFFF00)
            return await ctx.send(embed=embed)

        with open("extra/triggers.json", "r", encoding="utf-8", errors="ignore") as file:
            triggers = json.load(file, strict=False)

        if any(x in args.lower() for x in ["list", "liste", "remove", "delete"]):
            if args.lower() == "list" or args.lower() == "liste":
                if any(x == str(server_id) for x in triggers.keys()) and triggers[str(server_id)]:
                    content = "\n- ".join([x for x in triggers[str(server_id)].keys()])
                    embed = discord.Embed(title=f"Réactions customisées ({len(triggers[str(server_id)].keys())}) :", description="- " + content, color=0xBFFF00)
                    return await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="Il n'y à aucunes réactions customisées.", color=0xBFFF00)
                    return await ctx.send(embed=embed)
            elif "remove" in args.lower() or "delete" in args.lower():
                if len(args.split()) == 1:
                    embed = discord.Embed(title=f"Veuillez préciser un déclencheur à supprimer : `{prefix_server}trigger [remove / delete] [\"déclancheur\"]`", color=0xBFFF00)
                    return await ctx.send(embed=embed)
                if '"' in args:
                    remove = re.findall(r'["\'](.*?)["\']', args)[-1].lower()
                else:
                    remove = args.split()[-1].lower()
                if any(x.lower() == remove for x in triggers[str(server_id)].keys()):
                    del triggers[str(server_id)][remove]
                    with open("extra/triggers.json", "w", encoding="utf-8", errors="ignore") as file:
                        json.dump(triggers, file, indent=4)
                    embed = discord.Embed(title="Réaction supprimée :", description=f"**{remove}**", color=0xBFFF00)
                else:
                    embed = discord.Embed(title="Aucune réaction ne correspond à celle choisie.", color=0xBFFF00)
                return await ctx.send(embed=embed)
        if not '"' in args and not "'" in args:
            if len(args.split()) == 2:
                trigger = args.split()[0]
                response = args.split()[1]
            elif len(args.split()) < 2:
                embed = discord.Embed(title="Il y à pas assez d'arguments pour créer la réaction, ajoutez-en entre des guillements pour délimiter votre message.", color=0xBFFF00)
                return await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Il y à trop d'arguments pour créer la réaction, mettez des guillements pour délimiter votre message.", color=0xBFFF00)
                return await ctx.send(embed=embed)
        else:
            if len(re.findall(r'["\'](.*?)["\']', args)) == 2:
                trigger = re.findall(r'["\'](.*?)["\']', args)[0]
                if "http://" in args or "https://" in args:
                    response = args.split()[-1].replace('"', "").replace("'", "")
                else:
                    response = re.findall(r'["\'](.*?)["\']', args)[1]
            elif len(re.findall(r'["\'](.*?)["\']', args)) < 2:
                embed = discord.Embed(title="Il y à pas assez d'arguments pour créer la réaction, ajoutez-en entre des guillements pour délimiter votre message.", color=0xBFFF00)
                return await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Il y à trop d'arguments pour créer la réaction, mettez des guillements pour délimiter votre message.", color=0xBFFF00)
                return await ctx.send(embed=embed)
        if not any(x == str(server_id) for x in triggers.keys()):
            triggers[str(server_id)] = {trigger.lower(): response}
        else:
            if trigger.lower() in triggers[str(server_id)].keys():
                embed = discord.Embed(title="Il y a déjà un déclencheur pour ce message. Supprimez le puis refaites la commande.", color=0xBFFF00)
                return await ctx.send(embed=embed)
        triggers[str(server_id)][trigger.lower()] = response
        with open("extra/triggers.json", "w", encoding="utf-8", errors="ignore") as file:
            json.dump(triggers, file, indent=4)
        embed = discord.Embed(title="Nouvelle réaction customisée :", color=0xBFFF00)
        embed.add_field(name="Déclencheur", value=trigger, inline=True)
        embed.add_field(name="Réponse", value=response, inline=True)
        return await ctx.send(embed=embed)

#----------------------------- ADMIN_RIGHTS COMMANDS -----------------------------#

@client.command(pass_context=True, no_pm=True, aliases=["clearmsg", "clean"])
async def clear(ctx, *, args=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        if not server_id == 380373195473027074: # Support QuentiumBot server ID
            if not ctx.message.author.guild_permissions.manage_messages:
                return await ctx.send(f":x: {ctx.message.author.name}, vous n'avez pas la permission **Gérer les messages** !")
            if not ctx.message.guild.me.guild_permissions.manage_messages:
                return await ctx.send(":x: Il manque la permissions **Gérer les messages** au bot.")
            if not args:
                return await ctx.send("Merci de préciser un nombre.")
            else:
                if args.split()[0].isdecimal():
                    number = int(args[0])
                    if number < 99 and number >= 1:
                        limit = number + 1
                        await ctx.message.channel.purge(limit=limit)
                    else:
                        return await ctx.send("Le nombre doit être compris entre 1 et 99 pour limiter les erreurs.")
                else:
                    return await ctx.send("Nombre inconnu, merci de rentrer un nombre correct.")

@client.command(pass_context=True, no_pm=True, aliases=["moves"])
async def move(ctx, *, number=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        if any(x in [x.id for x in ctx.message.author.roles] for x in (285185833596616704, 267713117843095562)):
            channel_list = [x for x in ctx.message.guild.channels if isinstance(x, discord.VoiceChannel)]
            if not number:
                content = "Merci de préciser un salon vocal par son numéro.\n\n"
                numero = 0
                for channel in channel_list:
                    numero += 1
                    content += "{}. {}\n".format(numero, channel)
                embed = discord.Embed(title="Salons vocaux :", description=content, color=0x3498DB)
                return await ctx.send(embed=embed)
            else:
                if "random" in number:
                    if number == "random":
                        nb_times = 5
                    else:
                        nb_times = int(number.split("random ")[1])
                    nb_times = nb_times if nb_times < 20 else 20
                    random_numbers = []
                    list_members = []
                    temp = 0
                    while len(random_numbers) < nb_times:
                        random_numbers.append(random.randint(1, len(channel_list)))
                        if random_numbers[-1] == 2 or temp == random_numbers[-1]:
                            random_numbers = random_numbers[:-1]
                        if len(random_numbers) >= 1:
                            temp = random_numbers[-1]
                    for member in ctx.message.author.voice.channel.members:
                            list_members.append(member)
                    for channel_number in random_numbers:
                        for member in list_members:
                            await member.edit(voice_channel=channel_list[channel_number-1])
                            await asyncio.sleep(0.15)
                    return await ctx.message.delete()
                elif number.isdigit():
                    if not len(channel_list) == 0:
                        if not int(number) > len(channel_list):
                            channel = channel_list[int(number[0])-1]
                            if not channel.id == ctx.guild.afk_channel.id:
                                if not ctx.message.author.voice == None:
                                    if channel.id != ctx.message.author.voice.channel.id:
                                        await ctx.send("Déplacement dans : " + str(channel))
                                        list_members = []
                                        for member in ctx.message.author.voice.channel.members:
                                            list_members.append(member)
                                        for member in list_members:
                                            await member.edit(voice_channel=channel)
                                    else:
                                        return await ctx.send("Vous êtes déjà dans le même salon vocal !")
                                else:
                                    return await ctx.send("Vous n'êtes pas danc un salon vocal !")
                            else:
                                return await ctx.send("Ce channel n'est pas disponible.")
                        else:
                            return await ctx.send("Le numéro de salon ne correspond à aucun salons.")
                    else:
                        return await ctx.send("il n'y à pas de salons vocaux sur cotre serveur.")
                else:
                    content = "Merci de préciser un salon vocal par son numéro.\n\n"
                    numero = 0
                    for channel in channel_list:
                        numero += 1
                        content += "{}. {}\n".format(numero, channel)
                    embed = discord.Embed(title="Salons vocaux :", description=content, color=0x3498DB)
                    return await ctx.send(embed=embed)

@client.command(pass_context=True, no_pm=True)
async def kick(ctx, *, member : discord.Member=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        if not ctx.message.author.guild_permissions.kick_members:
            return await ctx.send(f":x: {ctx.message.author.name}, vous n'avez pas la permission **Expulser des membres** !")
        if not ctx.message.guild.me.guild_permissions.kick_members:
            return await ctx.send(":x: Il manque la permissions **Expulser des membres** au bot.")
        if not member:
            return await ctx.send(f":x: {ctx.message.author.name}, mentionnez la personne à expulser !")
        await member.kick()
        embed = discord.Embed(description = "**%s** à été kick !" % member.name, color=0xFF0000)
        return await ctx.send(embed=embed)

@client.command(pass_context=True, no_pm=True)
async def ban(ctx, *, member : discord.Member=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        if not ctx.message.author.guild_permissions.ban_members:
            return await ctx.send(f":x: {ctx.message.author.name}, vous n'avez pas la permission **Bannir des membres** !")
        if not ctx.message.guild.me.guild_permissions.ban_members:
            return await ctx.send(":x: Il manque la permissions **Bannir des membres** au bot.")
        if not member:
            return await ctx.send(f":x: {ctx.message.author.name}, mentionnez la personne à bannir !")
        await member.ban()
        embed = discord.Embed(description="**%s** à été bannis !" % member.name, color=0xFF0000)
        return await ctx.send(embed=embed)

#----------------------------- QUENTIUM COMMANDS -----------------------------#

@client.command(pass_context=True)
async def showideas(ctx):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        if ctx.message.author.id == 246943045105221633: # Quentium user ID
            if os.path.isfile("feedback.txt") == False:
                tmp = await ctx.send("Le fichier est vide :weary:")
                await asyncio.sleep(5)
                await ctx.message.delete()
                return await tmp.delete()
            content = ""
            if not os.path.isfile("feedback.txt"):
                content += "Aucunes"
            else:
                with open("feedback.txt", "r", encoding="utf-8", errors="ignore") as file:
                    for line in file:
                        content += line
            embed = discord.Embed(title="Idées :", description=content)
            tmp = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await ctx.message.delete()
            return await tmp.delete()
        else:
            return await ctx.send(f":x: {ctx.message.author.name} Vous n'avez pas les droits suffisants (Quentium seulement) !")

@client.command(pass_context=True)
async def addlogs(ctx, *, args=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        if ctx.message.author.id == 246943045105221633: # Quentium user ID
            if not args:
                return await ctx.message.delete()
            else:
                logs = " --- ".join([str(datetime.now().strftime("%d.%m.%Y - %H:%M")), args])
                with open("extra/logs.txt", "a", encoding="utf-8", errors="ignore") as file:
                    file.write(logs + "\n")
                await asyncio.sleep(5)
                return await ctx.message.delete()
        else:
            return await ctx.send(f":x: {ctx.message.author.name} Vous n'avez pas les droits suffisants (Quentium seulement) !")

@client.command(name="exec", pass_context=True, hidden=True, aliases=["execute"])
async def _exec(ctx, *, args=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        if ctx.message.author.id == 246943045105221633: # Quentium user ID
            if args:
                await async_command(args, ctx.message)
            else:
                return ctx.message.delete()

@client.command(name="eval", pass_context=True, hidden=True, aliases=["evaluate"])
async def _eval(ctx, *, args=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        if ctx.message.author.id == 246943045105221633: # Quentium user ID
            if args:
                try:
                    res = eval(args)
                    if inspect.isawaitable(res):
                        await res
                    else:
                        await ctx.send(res)
                except Exception as e:
                    return await ctx.send(f"```python\n{type(e).__name__}: {e}```")
            else:
                return await ctx.message.delete()

@client.command(pass_context=True, hidden=True)
async def data4tte(ctx, *number):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        authorised = [246943045105221633, 224928390694567936, 272412092248752137]
        if any(x == ctx.message.author.id for x in authorised): # Quentium / vectokse / Jaguar AF user ID
            if number:
                if number[0].isdecimal():
                    number = number[0]
            else:
                number = 130

            temp = await ctx.send("Sending requests, it may take long")
            await async_command("python3 extra/data4tte.py " + str(number), ctx.message)
            await asyncio.sleep(5)
            await ctx.message.delete()
            return await temp.delete()
        else:
            return await ctx.message.delete()

#----------------------------- TEMP COMMANDS -----------------------------#

# -- Add dtmine here too (in translations)

@client.command(pass_context=True, aliases=["jour"])
async def edt(ctx):
    edt = open("extra/edt.ics", "rb")
    gcal = Calendar.from_ical(edt.read())
    time_now = datetime.today() + timedelta(days=5)

    img = Image.open("extra/bg.jpg").convert("RGBA")
    img = img.filter(ImageFilter.GaussianBlur(radius=4))
    def cfont(font_size):
        return ImageFont.truetype("extra/sourcesanspro-black.ttf", font_size)
    frame = Image.open("extra/frame.png")
    img_w, img_h = img.size
    img.paste(frame, frame)
    img_draw = ImageDraw.Draw(img)
    text = f"Emploi du temps du {time_now.strftime('%d/%m')}"
    w, _ = img_draw.textsize(text, font=cfont(48))
    img_draw.text(((img_w - w)/2, 30), text, font=cfont(48), fill=(0, 240, 50))

    global_pos = [0, 160, 320, 480, 640, 800]
    global_hour = ["08h30", "10h30", "12h30", "14h00", "16h00", "18h00"]

    for x in range(len(global_pos)):
        position = (img_w * 0.07, img_h * 0.13 + global_pos[x])
        img_draw.text(position, global_hour[x], font=cfont(38), fill=(0, 240, 50))

    global_pos = [0, 180, 480, 660]
    global_color = ["white", "beige", "white", "beige"]
    del global_hour[2]

    for x in range(len(global_pos)):
        position = (img_w * 0.3, img_h * 0.15 + global_pos[x], img_w * 0.95, img_h * 0.3 + global_pos[x])
        img_draw.rectangle(position, outline="black", fill=global_color[x], width=5)
        for component in gcal.walk():
            if component.name == "VEVENT":
                time = component.get("dtstart").dt.strftime("%d/%m/%Y")
                if time == time_now.strftime("%d/%m/%Y"):
                    summary = component.get('summary')
                    location = component.get('location').split(",")[0]
                    dtstart = (component.get("dtstart").dt + timedelta(hours=2)).strftime('%Hh%M')
                    description = component.get('description').split("\n")[:-2]
                    def write_text(text, offset, font):
                        w, _ = img_draw.textsize(text, font=cfont(font))
                        pos = position[0] + ((position[2] - position[0]) - w) / 2
                        written_text = img_draw.text((pos, position[1] + offset), text, font=cfont(font), fill=(0, 240, 50))
                        return written_text

                    for y in range(4):
                        if x == y and dtstart == global_hour[y]:
                            write_text(summary, 0, 30)
                            if len(description) == 5:
                                write_text("(" + description[4] + ")", 28, 26)
                                write_text(location, 56, 26)
                                write_text(description[3], 84, 26)
                                write_text(description[2], 112, 26)
                            else:
                                desc = [description[i:i+2] for i in range(0, len(description), 2)]
                                for x in range(len(desc)):
                                    write_text(" ".join(desc[x]), (x + 1) * 28, 26)

    couverts = Image.open("extra/couverts.png")
    couverts.thumbnail((img_w / 3, img_h / 3), Image.ANTIALIAS)
    img.paste(couverts, (265, 485), couverts)

    edt.close()

    img.save("extra/result.png", quality=90, optimize=True, progressive=True)
    await ctx.send(file=discord.File("extra/result.png", "edt.png"))
    await asyncio.sleep(10)
    try:subprocess.call("sudo rm extra/result.png", shell=True)
    except:pass

@client.command(pass_context=True, aliases=["mc", "omg", "omgserv"])
@commands.cooldown(2, 10, commands.BucketType.channel)
async def minecraft(ctx, * , omg_id=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    # 22915
    if not ctx.message.author.bot == True:
        if ctx.message.author.id == 247775235913285632: # SpaceDragon user ID
            args = "236885"
        if not args:
            return await ctx.send("Veuillez renseigner l'id de vôtre server OMGServ.")
        if not args.isdigit():
            return await ctx.send("L'id OMGServ n'est pas un nombre.")
        data_players = requests.get(f"https://panel.omgserv.com/json/{args}/players").json()
        data_status = requests.get(f"https://panel.omgserv.com/json/{args}/status").json()
        if "Access denied" in str(data_status):
            return await ctx.send("L'id OMGServ n'existe pas !")
        if not "Invalid type" in str(data_players):
            list_players = sorted([x for x in eval(str(data_players["players"]))], key=lambda x: x.casefold())
        else:
            list_players = False

        ImageFile.MAXBLOCK = 2**20
        img = Image.open("extra/background.jpg")
        W, _ = img.size
        font1 = ImageFont.truetype("extra/MikadoUltra.ttf", 120)
        font2 = ImageFont.truetype("extra/MikadoUltra.ttf", 90)
        font3 = ImageFont.truetype("extra/MikadoUltra.ttf", 70)
        draw = ImageDraw.Draw(img)
        w, _ = draw.textsize("Statistiques du Serveur", font=font1)
        draw.text(((W - w)/2, 20), "Statistiques du Serveur", font=font1, fill=(0, 255, 0))

        if list_players:
            for x in range(len(list_players)):
                if len(list_players) <= 4: column = 300
                else: column = 40; column1 = 640
                if x <= 4:
                    draw.text((column, 80 + (x + 1) * 150), "-  " + list_players[x], font=font3, fill=(0, 0, 255))
                elif x <= 9:
                    draw.text((column1, 80 + (x - 4) * 150), "-  " + list_players[x], font=font3, fill=(0, 0, 255))
                else:pass
        else:
            draw.text((200, 300), "Serveur vide !", font=font1, fill=(0, 0, 255))

        try:status = "Online" if str(data_status["status"]["online"]) == "True" else "Offline"
        except:status = "Unknown"
        try:cpu_percent = str(data_status["status"]["cpu"])
        except:cpu_percent = "Ø"
        try:ram_number = str(data_status["status"]["ram"])
        except:ram_number = "Ø"
        try:max_players = str(data_status["status"]["players"]["max"])
        except:max_players = "Ø"
        draw.text((1280, 220), "Status : " + status, font=font2, fill=(255, 0, 0))
        draw.text((1280, 400), "Players : {}/{}".format(len(list_players), max_players), font=font2, fill=(255, 0, 0))
        draw.text((1280, 580), "CPU : {}%".format(cpu_percent), font=font2, fill=(255, 0, 0))
        draw.text((1280, 760), "RAM : {} Mo".format(ram_number[:4]), font=font2, fill=(255, 0, 0))
        img.thumbnail((1280, 720), Image.ANTIALIAS)
        img.save("extra/result.jpg", "JPEG", quality=80, optimize=True, progressive=True)
        await ctx.send(file=discord.File("extra/result.jpg", "mc.jpg"))
        await asyncio.sleep(10)
        try:subprocess.call("sudo rm extra/result.jpg", shell=True)
        except:pass

@client.command(pass_context=True, aliases=["minedt"])
async def dtmine(ctx, *args):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(str(server_id), server_name, ctx.message)

    if not ctx.message.author.bot == True:
        if not args:
            return await ctx.send(f"Merci de préciser au moins un minerais : `{prefix_server}dtmine [\"minerais\"] [\"secteur_max\"]`.")
        minerais = args[0].lower()
        if len(args) == 2 and args[1].isdigit():
            max_deep = args[1]
        else:
            max_deep = "120"

        try:minerais = aliases_dt[minerais]
        except:pass
        ores = mines["0"].keys()
        for area, _ in mines.items():
            for ore in ores:
                if mines[area].get(ore) is None:
                    mines[area].update({ore: 0})

        def best_mines(ore):
            ordered_mines = [(k, v) for k, v in mines.items()]
            ordered_mines.sort(key=lambda x: x[1][ore], reverse=True)
            return ordered_mines
        if minerais not in mines["0"].keys():
            return await ctx.send(f"Le minerais {minerais} n'existe pas :frowning:")
        if max_deep == "120":
            text = f"Voici les 10 meilleurs emplacements pour le minerais {minerais} :```"
        else:
            text = f"Voici les 10 meilleurs emplacements pour le minerais {minerais} jusqu'au secteur {max_deep} :```"
        i = 0
        for mine in best_mines(minerais):
            if i >= 10:
                break
            if mine[0] == "0":
                continue
            if mine[1][minerais] == 0:
                continue
            if int(mine[0]) <= int(max_deep):
                if mine[1][minerais] < 0.01 and minerais != "platinum":
                    break
                text += mine[0].center(3, " ")
                text += " : " + str(round(mine[1][minerais] * 100, 2)) + "%\n"
            else:
                continue
            i += 1
        text += "```"
        return await ctx.send(text)

client.run(config["PRIVATE"]["token"])
