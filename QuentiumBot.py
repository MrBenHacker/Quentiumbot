import discord, asyncio, psutil, subprocess, time, calendar, requests, urllib.request, json, random, inspect, re, os
from PIL import Image, ImageDraw, ImageFont, ImageFile
from discord.ext import commands
from datetime import datetime
from bs4 import BeautifulSoup

open("extra/data.txt", "a+", encoding="utf-8").close()
open("extra/logs.txt", "a+", encoding="utf-8").close()

with open("extra/CONFIG.json", "r", encoding="utf-8") as file:
    config = json.load(file)

with open("extra/triggers.json", "r", encoding="utf-8") as file:
    triggers = json.load(file)

def get_prefix(bot, message):
    with open("extra/prefixes.json", "r", encoding="utf-8") as file:
        prefixes = json.load(file)
    if not message.guild:
        return "+"
    if prefixes.get(str(message.guild.id)):
        prefixes_list = prefixes.get(str(message.guild.id))
    else:
        prefixes_list = "+"
    return commands.when_mentioned_or(prefixes_list)(bot, message)

sep = config["GLOBAL"]["sep"]
token_genius = config["GLOBAL"]["token_genius"]
token_weather = config["GLOBAL"]["token_weather"]
token_timezone = config["GLOBAL"]["token_timezone"]
client = commands.Bot(command_prefix=get_prefix, description="Quentium's Public Bot", pm_help=True)
client.remove_command("help")

@client.event
async def on_ready():
    global start_time
    url = "https://discordbots.org/api/bots/" + str(client.user.id) + "/stats"
    headers = {"Authorization" : config["GLOBAL"]["token_dbl"]}
    print("\n+--------------------------------------------+"
          "\n|             QuentiumBot ready !            |"
          "\n|           © 2017 - 2019 QuentiumYT         |"
          "\n+--------------------------------------------+\n")
    print("Logged in as %s#%s" % (client.user.name, client.user.discriminator))
    print("ID: " + str(client.user.id))
    start_time = datetime.now()
    print("\nStarting at: " + start_time.strftime("%d.%m.%Y - %H:%M:%S"))
    try:
        payload = {"server_count"  : len(client.guilds)}
        requests.post(url, data=payload, headers=headers)
    except:pass
    await client.change_presence(activity=discord.Activity(name="+help | quentium.fr", type=discord.ActivityType.playing), status=discord.Status.online)

#----------------------------- SETUP GLOBAL FUNCTIONS AND GLOBAL EVENTS -----------------------------#

async def async_data(server_id1, server_name1):
    global lang_server, commands_server, autorole_server
    with open("extra/data.txt", encoding="utf-8") as file:
        def unknown_server():
            global lang_server, commands_server, autorole_server
            lang_server = "fr"
            commands_server = 1
            autorole_server = "@everyone"
            with open("extra/data.txt", "a", encoding="utf-8") as file:
                infos = [server_id1, server_name1, lang_server, commands_server, autorole_server]
                file.write(sep.join(map(str, infos)) + "\n")
        if os.stat("extra/data.txt").st_size == 0:
            unknown_server()
        else:
            not_id = True
            for line in file:
                if str(server_id1) in line:
                    clean_line = line.rstrip().split(sep, 999)
                    lang_server = clean_line[2]
                    clean_line[3] = str(int(clean_line[3]) + 1)
                    commands_server = clean_line[3]
                    autorole_server = clean_line[4]
                    with open("extra/data.txt", "r", encoding="utf-8") as file:
                        filedata = file.read()
                    filedata = filedata.replace(str(line), str(sep.join(clean_line) + "\n"))
                    with open("extra/data.txt", "w", encoding="utf-8") as file2:
                        file2.write(filedata)
                    not_id = False
                    break
                else:
                    not_id = True
            if not_id:
                unknown_server()
    return lang_server, commands_server, autorole_server

async def async_command(args, msg):
    def emo(text):
        return str(discord.utils.get(client.emojis, name=text))
    if "data4tte" in args or "menu4tte" in args:
        args = args.split(" ")
        subprocess.Popen(["sudo"] + args)
        return None
    msg_channel = discord.utils.get(msg.author.guild.channels, id=msg.channel.id)
    if args == "runpc":
        await msg.delete()
        content = emo("pc1") + " Quentium PC\n" + emo("pc2") + " Office PC\n" + emo("pc3") + " Space PC"
        embed = discord.Embed(title=emo("vote") + " Choisissez un ordinateur à démarrer :", description=content, color=0x000000)
        msg = await msg_channel.send(embed=embed)
        for item in ["pc1", "pc2", "pc3"]:
            emo = discord.utils.get(client.emojis, name=item)
            await msg.add_reaction(emo)
        return None
    elif args == "setco":
        await msg.delete()
        content = emo("co1") + " ON 19H\n" + emo("co2") + " ON 22H\n" + emo("co3") + " OFF 19H\n" + emo("co4") + " OFF 22H"
        embed = discord.Embed(title=emo("vote") + " Choisissez une action à réaliser pour la connexion :", description=content, color=0x000000)
        msg = await msg_channel.send(embed=embed)
        for item in ["co1", "co2", "co3", "co4"]:
            emo = discord.utils.get(client.emojis, name=item)
            await msg.add_reaction(emo)
        return None
    elif "ping" in args:
        return await msg_class.delete()
    try:
        result = subprocess.check_output("sudo " + args, shell=True, stderr=subprocess.STDOUT)
    except Exception as e:
        result = type(e).__name__ + ": " + str(e)
    try:
        return await msg_channel.send("```autohotkey\n{}\n```".format(result.decode("cp1252")))
    except:
        try:
            return await msg_channel.send("```autohotkey\n{}\n```".format(result.decode("UTF-8")))
        except:
            return await msg_channel.send("```autohotkey\n{}\n```".format(str(result)))

@client.listen()
async def on_message(message):
    global triggers
    try:server_id = message.guild.id
    except:server_id = None

    try:
        global lang_server
        lang_server = "fr"
        with open("extra/data.txt", encoding="utf-8") as file:
            for line in file:
                if str(server_id) in line:
                    lang_server = line.rstrip().split(sep, 999)[2]
                    break
    except:
        lang_server = "fr"

    if client.user.mention == message.content.replace("!", ""):
        if str(message.guild.id) in prefixes.keys():
            pre = prefixes[str(message.guild.id)]
            if lang_server == "fr":
                return await message.channel.send(f"Le préfixe du bot est `{pre}`. Utilisez la commande `{pre}help` pour la liste des commandes.")
            elif lang_server == "en":
                return await message.channel.send(f"The prefix of the bot is `{pre}`. Use the `{pre}help` command for the list of commands.")
            elif lang_server == "de":
                return await message.channel.send(f"Das Präfix des Bots ist `{pre}`. Verwenden Sie den Befehl `{pre}help` für die Liste der Befehle.")
        else:
            if lang_server == "fr":
                return await message.channel.send("Le préfixe du bot est `+`. Utilisez la commande `+help` pour la liste des commandes.")
            elif lang_server == "en":
                return await message.channel.send("The prefix of the bot is `+`. Use the `+help` command for the list of commands.")
            elif lang_server == "de":
                return await message.channel.send("Das Präfix des Bots ist `+`. Verwenden Sie den Befehl `+help` für die Liste der Befehle.")

    if server_id == 199189022894063627: # TheSweMaster server ID
        if len([x.name for x in message.author.roles]) == 1:
            if any(x in message.content.lower() for x in ["oauth2", "discord.gg"]):
                return await message.delete()

    if not message.author.bot == True:
        if any(x == str(server_id) for x in triggers.keys()):
            with open("extra/triggers.json", "r", encoding="utf-8") as file:
                triggers = json.load(file)
            if any(x == message.content.lower() for x in triggers[str(server_id)].keys()):
                response = triggers[str(server_id)].get(message.content.lower())
                return await message.channel.send(response)

async def on_server_join(server):
    try:
        payload = {"server_count"  : len(client.guilds)}
        requests.post(url, data=payload, headers=headers)
    except:pass

async def on_server_remove(server):
    try:
        payload = {"server_count"  : len(client.guilds)}
        requests.post(url, data=payload, headers=headers)
    except:pass

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
            serv = client.get_guild(391272643229384705) # Insoumis server ID
            kick_list = [x for x in [x for x in serv.members if not x.bot] if len(x.roles) <=1]
            for member in kick_list:
                await member.kick()
            kick_list_name = [x.name for x in [x for x in serv.members if not x.bot] if len(x.roles) <=1]
            if kick_list_name:
                content = "- " + "\n- ".join(kick_list_name)
            else:
                content = "Personne"
            embed = discord.Embed(title=f"Membres expulsés : {len(kick_list_name)}", description=content, color=0xFF0000)
            embed.set_footer(text=str(datetime.now().strftime("%d.%m.%Y - %H:%M:%S")))
            await serv.get_channel(485168827580284948).send(embed=embed) # Insoumis channel ID
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
async def on_member_join(member):
    with open("extra/data.txt", encoding="utf-8") as file:
        for line in file:
            if str(member.guild.id) in line:
                clean_line = line.rstrip().split(sep, 999)
                autorole_server = clean_line[4]
                break
            else:
                autorole_server = "@everyone"
    if not autorole_server == "@everyone":
        role = discord.utils.get(member.guild.roles, id=int(autorole_server))
        if not role == None:
            try:await member.add_roles(role)
            except:pass

    if member.guild.id == 199189022894063627: # TheSweMaster server ID
        if any(x in member.name for x in ["discord.gg", "twitter.com"]):
            await member.ban()
            msg = "A bot has been banned because we don't like them :ok_hand:"
            return await discord.utils.get(member.guild.channels, id=290905147826110464).send(msg)
        else:
            msg = f"Hey {member.mention} ! Welcome on ***{member.guild.name}***! Feel free to ask for a cookie :cookie:"
            return await discord.utils.get(member.guild.channels, id=199189022894063627).send(msg)

@client.event
async def on_reaction_add(reaction, user):
    if user.id == 246943045105221633: # Quentium user ID
        try:
            if "<:vote:509442482141003776> Choisissez" in reaction.message.embeds[0].title:
                await reaction.message.remove_reaction(reaction.emoji, user)
                if "ordinateur" in reaction.message.embeds[0].title:
                    msg_channel = discord.utils.get(user.guild.channels, id=reaction.message.channel.id)
                    try:emo = reaction.emoji.name
                    except:emo = None
                    if emo and emo[:2] == "pc":
                        if emo == "pc1":
                            args = "etherwake -i eth0 40:16:7E:AD:F7:21"
                            tmp = await msg_channel.send(str(reaction.emoji) + " Démarrage de ***PC Quentium***")
                        elif emo == "pc2":
                            args = "etherwake -i eth0 40:61:86:93:B7:C7"
                            tmp = await msg_channel.send(str(reaction.emoji) + " Démarrage de ***PC Bureau***")
                        elif emo == "pc3":
                            args = "etherwake -i eth0 40:16:7E:AD:7B:6C"
                            tmp = await msg_channel.send(str(reaction.emoji) + " Démarrage de ***PC Space***")
                        await async_command(args, reaction.message)
                        await asyncio.sleep(10)
                        return await tmp.delete()
                if "connexion" in reaction.message.embeds[0].title:
                    msg_channel = discord.utils.get(user.guild.channels, id=reaction.message.channel.id)
                    try:emo = reaction.emoji.name
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
                                tmp = await msg_channel.send(str(reaction.emoji) + " Connexion ajoutée jusqu'à ***19h***")
                            elif emo == "co2":
                                urllib.request.urlopen("http://192.168.1.100:8080/set.cmd?cmd=setpower+p62=1")
                                tmp = await msg_channel.send(str(reaction.emoji) + " Connexion ajoutée jusqu'à ***22h***""")
                            elif emo == "co3":
                                urllib.request.urlopen("http://192.168.1.100:8080/set.cmd?cmd=setpower+p61=0")
                                tmp = await msg_channel.send(str(reaction.emoji) + " Connexion enlevée de ***19h***")
                            elif emo == "co4":
                                urllib.request.urlopen("http://192.168.1.100:8080/set.cmd?cmd=setpower+p62=0")
                                tmp = await msg_channel.send(str(reaction.emoji) + " Connexion enlevée de ***22h***")
                            await asyncio.sleep(10)
                            return await tmp.delete()
                        except:
                            return await msg_channel.send("Le site n'a pas pu répondre (No route to host)")
        except:
            pass

@client.event
async def on_command_error(ctx, error):
    try:
        global lang_server
        lang_server = "fr"
        with open("extra/data.txt", encoding="utf-8") as file:
            for line in file:
                if str(ctx.message.guild.id) in line:
                    lang_server = line.rstrip().split(sep, 999)[2]
                    break
    except:
        lang_server = "fr"

    if lang_server == "fr":
        if "is not found" in str(error):
            return False
        elif "FORBIDDEN (status code: 403): Missing Permissions" in str(error):
            return await ctx.send(":x: Il manque certaines permissions au bot.")
        elif "FORBIDDEN (error code: 50013): Missing Permissions" in str(error):
            return await ctx.send(":x: Il manque certaines permissions au bot.")
        elif "FORBIDDEN (status code: 403): Missing Access" in str(error):
            return await ctx.send(":x: Il manque certains accès au bot.")
        elif "Cannot send an empty message" in str(error):
            return await ctx.message.delete()
        elif "BAD REQUEST (status code: 400): You can only bulk delete messages that are under 14 days old." in str(error):
            return await ctx.send(":x: Vous ne pouvez que supprimer les messages datant de moins de 14 jours :pensive:")
        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(":x: Un argument requis manque :rolling_eyes:")
        elif isinstance(error, commands.NoPrivateMessage):
            return await ctx.send(":x: Cette commande ne peut pas être utilisée en message privés :confused:")
        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(":x: Cette commande à été désactivée :confounded:")
        elif isinstance(error, commands.BadArgument):
            return await ctx.send(":x: Un mauvais argument à été donné :slight_frown:")
        elif isinstance(error, commands.TooManyArguments):
            return await ctx.send(":x: Trop d'arguments ont étés donnés :scream:")
        elif isinstance(error, commands.CommandOnCooldown):
            time_left = str(error).split("Try again in ", 1)[1].split(".", 1)[0]
            return await ctx.send(f":x: Doucement, il y a un cooldown sur cette commande, il vous reste {time_left} secondes à attendre :raised_hand:")
    elif lang_server == "en":
        if "is not found" in str(error):
            return False
        elif "FORBIDDEN (status code: 403): Missing Permissions" in str(error):
            return await ctx.send(":x: The bot is missing some permissions.")
        elif "FORBIDDEN (error code: 50013): Missing Permissions" in str(error):
            return await ctx.send(":x: The bot is missing some permissions.")
        elif "FORBIDDEN (status code: 403): Missing Access" in str(error):
            return await ctx.send(":x: The bot is missing some access.")
        elif "Cannot send an empty message" in str(error):
            return await ctx.message.delete()
        elif "BAD REQUEST (status code: 400): You can only bulk delete messages that are under 14 days old." in str(error):
            return await ctx.send(":x: You can only delete messages that are under 14 days old :pensive:")
        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(":x: A required argument is missing :rolling_eyes:")
        elif isinstance(error, commands.NoPrivateMessage):
            return await ctx.send(":x: This command can't be used in private messages :confused:")
        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(":x: This command has been disabled :confounded:")
        elif isinstance(error, commands.BadArgument):
            return await ctx.send(":x: A wrong argument has been given :slight_frown:")
        elif isinstance(error, commands.TooManyArguments):
            return await ctx.send(":x: Too many arguments has been given :scream:")
        elif isinstance(error, commands.CommandOnCooldown):
            time_left = str(error).split("Try again in ", 1)[1].split(".", 1)[0]
            return await ctx.send(f":x: Slow down, there is a cooldown on that command, you have to wait {time_left} more seconds :raised_hand:")
    elif lang_server == "de":
        if "is not found" in str(error):
            return False
        elif "FORBIDDEN (status code: 403): Missing Permissions" in str(error):
            return await ctx.send(":x: Dem Bot fehlen einige Berechtigungen.")
        elif "FORBIDDEN (error code: 50013): Missing Permissions" in str(error):
            return await ctx.send(":x: Dem Bot fehlen einige Berechtigungen.")
        elif "FORBIDDEN (status code: 403): Missing Access" in str(error):
            return await ctx.send(":x: Dem Bot fehlen einige Zugang.")
        elif "Cannot send an empty message" in str(error):
            return await ctx.message.delete()
        elif "BAD REQUEST (status code: 400): You can only bulk delete messages that are under 14 days old." in str(error):
            return await ctx.send(":x: Sie können nur Nachrichten löschen, die weniger als 14 Tage alt sind :pensive:")
        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(":x: Ein Erfordertes argument fehlt :rolling_eyes:")
        elif isinstance(error, commands.NoPrivateMessage):
            return await ctx.send(":x: Dieser Befehl kann nicht in direkt nachrichten verwendet werden :confused:")
        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(":x: Dieser Befehl wurde deaktivier :confounded:")
        elif isinstance(error, commands.BadArgument):
            return await ctx.send(":x: Es wurd ein falsches argument gegeben :slight_frown:")
        elif isinstance(error, commands.TooManyArguments):
            return await ctx.send(":x: Es wurden zu viele argumente gegeben :scream:")
        elif isinstance(error, commands.CommandOnCooldown):
            time_left = str(error).split("Try again in ", 1)[1].split(".", 1)[0]
            return await ctx.send(f":x: Langsam, dieser befehl hat einen cool down, Sie haben noch {time_left} sekunden zu warten :raised_hand:")
    file = open("errors.txt", "a", encoding="utf-8")
    infos = [ctx.message.guild.name, ctx.message.author.name, datetime.now().strftime("%d.%m.%Y - %H:%M:%S"), ctx.message.content, str(error)]
    file.write(sep.join(map(str, infos)) + "\n")
    file.close()
    return False

#----------------------------- USER COMMANDS -----------------------------#

@client.command(pass_context=True, aliases=["cmd"])
async def help(ctx):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        if lang_server == "fr":
            commands_user = """
- `help / cmd` > Affiche la liste des commandes.
- `letter ["texte"]` > Ecris un message avec des émojis.
- `embed [T="titre"] [D="description"] [C="couleur"] [I="image URL"] [F="bas de page"] [U="URL"] [A="auteur"]` > Affiche un embed personnalisé.
- `listbans` > Affiche la liste des personnes bannies.
- `listinvites` > Affiche la liste des liens d'invitation.
- `listservers` > Affiche la liste des serveurs comportant le bot.
- `msgtotal [all / channel] [@membre]` > Calcule le nombre de messages d'un membre au total ou dans le salon.
- `lyrics ["musique"]` > Recherche les paroles d'une musique.
- `weather ["ville"]` > Affiche la météo de la ville spécifiée.
- `serverstats` > Montre les statistiques du serveur.
- `userstats [@membre]` > Montre les statistiques d'un membre.
- `botstats` > Montre les statistiques du bot.
- `shareme` > Invite le bot sur votre serveur.
- `ping` > Calcule le temps de réactivité du bot."""
            commands_dt = """
:warning: Le préfixe pour France Les Cités est `-` :warning: 
- `absent ["durée + (raison)"]` > Attribuez vous le rôle Absent si vous devez vous absenter un moment.
- `dtmine ["minerais"]` > Affiche les 10 meilleurs endroits pour miner une ressource (©Fomys :smile:)."""
            commands_admin = """
- `clear ["nombre"]` > Supprime un nombre défini de messages.
- `kick [@membre]` > Expulse la personne mentionnée.
- `ban [@membre]` > Bannis la personne mentionnée.
- `autorole ["nom du role" / show / remove]` > Donne un rôle automatiquement à quelqu'un lorsqu'il rejoins le serveur.
- `lang [fr / en / de]` > Change la langue du bot. (Langue par défaut : fr)"""
            commands_feedback = """
- `idea / bug ["texte"]` > Propose une idée ou reporte un bug pour améliorer le bot.
- `showlogs` > Affiche la liste des mises à jour du bot.

Légende : `[argument]` - `["argument donné"]` (Enlevez les guillemets) - `[@mention]` - `[choix / "mon_choix"]`
:warning: Si vous rencontrez un problème, merci de la soumettre avec la commande `+bug` ou en rejoignant le serveur de test/support : https://discord.gg/5sehgXx\n"""
            end_text = ":euro: Pour une petite donation : [Cliquez ici]({})".format("https://www.paypal.me/QLienhardt")
            embed = discord.Embed(title="----- Liste des Commandes -----", url="https://quentium.fr/discord/", color=0x00ff00)
            embed.add_field(name=":video_game: Commandes **UTILISATEUR** :", value=commands_user, inline=True)
            if server_id == 371687157817016331: # France Les Cités ID
                embed.add_field(name=":flag_fr: Commandes **Deep Town** :", value=commands_dt, inline=True)
            embed.add_field(name=":cop: Commandes **ADMIN** :", value=commands_admin, inline=True)
            embed.add_field(name=":incoming_envelope: Commandes **SUPPORT / FEEDBACK** :", value=commands_feedback + end_text, inline=True)
            embed.set_footer(text="Pour plus d'informations, veuillez visiter le site : https://quentium.fr/discord/", icon_url="https://quentium.fr/+img/logoBot.png")
            return await ctx.send(embed=embed)

        elif lang_server == "en":
            commands_user = """
- `help / cmd` > Show list of commands available.
- `letter ["text"]` > Write a message with emojis.
- `embed [T="title"] [D="description"] [C="color"] [I="image URL"] [F="footer" / None] [U="URL"] [A="author"]` > Shows a personalized embed.
- `listbans` > Show list of banned members.
- `listinvites` > Show list of invite links.
- `listservers` > Show list of servers with the bot.
- `msgtotal [all / channel] [@member]` > Calculates the number of messages of a member in total or in the current channel.
- `lyrics ["music"]` > Search for lyrics of a song.
- `weather ["city"]` > Shows the weather of the specified city.
- `serverstats` > Show stats of the server.
- `userstats [@member]` > Show stats of a member.
- `botstats` > Show stats of the bot.
- `shareme` > Invite the bot to your server.
- `ping` > Calculate bot's latency."""
            commands_admin = """
- `clear ["number"]` > Clear a specific number of messages.
- `kick [@member]` > Kick the tagged member.
- `ban [@member]` > Ban the tagged member.
- `autorole ["rolename" / show / remove]` > Give a role automatically to someone when he join the server.
- `lang [fr / en / de]` > Change the language of the bot. (Default language : fr)"""
            commands_feedback = """
- `idea / bug ["text"]` > Submit an idea or report a bug to improve the bot.
- `showlogs` > Shows update logs of the bot.

Caption: `[argument]` - `["given argument"]` (Remove quotes) - `[@mention]` - `[choice  / "my_choice"]`
:warning: If you have any problem, please submit it with `+bug` command or join our test/support server: https://discord.gg/5sehgXx\n"""
            end_text = ":dollar: For a small donation: [Click here]({})".format("https://www.paypal.me/QLienhardt")
            embed = discord.Embed(title="----- List of Commands -----", url="https://quentium.fr/en/discord/", color=0x00ff00)
            embed.add_field(name=":video_game: Commands **USER**:", value=commands_user, inline=True)
            embed.add_field(name=":cop: Commands **ADMIN**:", value=commands_admin, inline=True)
            embed.add_field(name=":incoming_envelope: Commands **SUPPORT / FEEDBACK**:", value=commands_feedback + end_text, inline=True)
            embed.set_footer(text="For more informations, please check my website: https://quentium.fr/en/discord/", icon_url="https://quentium.fr/+img/logoBot.png")
            return await ctx.send(embed=embed)

        elif lang_server == "de":
            commands_user = """
- `help / cmd` > Zeigt die Befehlsliste an.
- `letter ["Text"]` > Schreibe eine Nachricht mit emojis.
- `embed [T="Titel"] [D="Beschreibung"] [C="Farbe"] [I="Bild URL"] [F="Fußzeile" / None] [U="URL"] [A="Autor"]` > Zeigt eine personifizierte embed an.
- `listbans` > Zeigt die Liste der verbanten Benutzer.
- `listinvites` > Zeigt die Liste der Einladungslinks.
- `listservers` > Zeigt die Liste des Servers mit dem Bot.
- `msgtotal [all / channel] [@Mitglied]` > Berechnet die Anzahl der Nachrichten eines Mitglieds insgesamt oder im Chatroom.
- `lyrics ["Musik"]`> Durchsucht den Text einer Musik.
- `weather ["Stadt"]` > Zeigt das Wetter der angegebenen Stadt an.
- `serverstats` > Zeigt die Serverstatistiken an.
- `userstats [@Mitglied]` > Zeigt die Statistiken des jeweiligen Mitglieds an.
- `botstats` > Zeigt die Botstatistiken an.
- `shareme` > Lädet den Bot auf Deinen Server ein.
- `ping` > Berechnen Sie die Latenz des Bots."""
            commands_admin = """
- `clear ["Zahl"]` > Löscht eine bestimmte Anzahl von Nachrichten.
- `kick [@Mitglied]` > Kickt das genannte Mitglied.
- `ban [@Mitglied]` > Verbannt das genannte Mitglied.
- `autorole ["Rolename" / show / remove]` > Gibt jemandem automatisch eine Rolle, wenn er dem Server beitritt.
- `lang [fr / en / de]` > Verändert die Sprache des Bots. (Standardsprache : fr)"""
            commands_feedback = """
- `idea / bug ["Text"]` > Schlag eine Idee vor oder melde einen Fehler um den Bot zu verbessern.
- `showlogs` > Zeigt die liste der Neuigkeiten des Bots an.

Beschriftung: `[Argument]` - `["Gegeben Argument"]` (Entfernen Sie Anführungszeichen) - `[@Erwähnung]` - `[wähl / "Meine_Wähle"]`
:warning: Wenn ihr einen Fehler findet, bitte meldet ihn mit `+bug` befehle oder indem Sie dem test/support-Server beitreten: https://discord.gg/5sehgXx\n"""
            end_text = ":euro: Für eine kleine spende: [Hier klicken]({})".format("https://www.paypal.me/QLienhardt")
            embed = discord.Embed(title="----- Liste der Befehle -----", url="https://quentium.fr/de/discord/", color=0x00ff00)
            embed.add_field(name=":video_game: Befehle **BENUTZER**:", value=commands_user, inline=True)
            embed.add_field(name=":cop: Befehle **VERWALTER**:", value=commands_admin, inline=True)
            embed.add_field(name=":incoming_envelope: Befehle **SUPPORT / FEEDBACK**:", value=commands_feedback + end_text, inline=True)
            embed.set_footer(text="Für weitere Informationen, Bitte besuchen Sie meine Website: https://quentium.fr/de/discord/", icon_url="https://quentium.fr/+img/logoBot.png")
            return await ctx.send(embed=embed)

@client.command(pass_context=True)
async def prefix(ctx, *, args=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    def update_prefix():
        with open("extra/prefixes.json", "w", encoding="utf-8") as file:
            json.dump(prefixes, file, indent=4)
            client.command_prefix = get_prefix(client, ctx.message)

    if not ctx.message.author.guild_permissions.administrator:
        if lang_server == "fr":
            return await ctx.send(f":x: {ctx.message.author.name}, vous n'avez pas la permission **Administrateur** !")
        elif lang_server == "en":
            return await ctx.send(f":x: {ctx.message.author.name}, you don't have the permission **Administrator**!")
        elif lang_server == "de":
            return await ctx.send(f":x: {ctx.message.author.name}, Sie haben nicht die Berechtigung **Verwalter**!")
    if not args:
        if lang_server == "fr":
            return await ctx.send("Merci de préciser un argument valide : `+prefix [\"préfixe\" / reset]`.")
        elif lang_server == "en":
            return await ctx.send("Please specify a valid argument: `+prefix [\"prefix\" / reset]`.")
        elif lang_server == "de":
            return await ctx.send("Bitte geben Sie ein richtiges Argument an: `+prefix [\"Präfix\" / reset]`.")
    if args == "reset" or args == "remove":
        if str(server_id) in prefixes:
            del prefixes[str(server_id)]
            update_prefix()
            if lang_server == "fr":
                return await ctx.send("Le préfixe à été supprimé.")
            elif lang_server == "en":
                return await ctx.send("The prefix has been removed.")
            elif lang_server == "de":
                return await ctx.send("Das Präfix wurde entfernt.")
        else:
            if lang_server == "fr":
                return await ctx.send("Le préfixe n'a pas pu être supprimé car il n'a pas été défini.")
            elif lang_server == "en":
                return await ctx.send("The prefix could not be deleted because it was not defined.")
            elif lang_server == "de":
                return await ctx.send("Das Präfix konnte nicht gelöscht werden, da es nicht definiert wurde.")
    prefixes[str(server_id)] = args
    update_prefix()
    if lang_server == "fr":
        return await ctx.send(f"Le préfixe à été changé en `{args}`.")
    elif lang_server == "en":
        return await ctx.send(f"The prefix has been changed to `{args}`.")
    elif lang_server == "de":
        return await ctx.send(f"Das Präfix wurde in `{args}` geändert.")

@client.command(pass_context=True, aliases=["lettre"])
async def letter(ctx, *, args=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    def emo(text):
        return str(discord.utils.get(client.emojis, name=text))

    if not ctx.message.author.bot == True:
        if not args:
            if lang_server == "fr":
                return await ctx.send("Merci de préciser un texte.")
            elif lang_server == "en":
                return await ctx.send("Please specify a text.")
            elif lang_server == "de":
                return await ctx.send("Bitte geben Sie einen text an.")
        lst = []
        sentence = args
        emojis_used = re.findall(r"<\w*:\w*:\d*>", sentence)
        emojis_temp = []
        if emojis_used:
            for emoji in emojis_used:
                if int(emoji.split(":", 2)[2].split(">")[0]) in [x.id for x in client.emojis]:
                    sentence = sentence.replace(emoji, "☺")
                else:
                    sentence = sentence.replace(emoji, "☻")
                    emojis_temp.append(emoji)
        for emojis in emojis_temp:
            emojis_used.remove(emojis)
        is_mention = re.findall(r"<@\d*>", sentence)
        for mention in is_mention:
            sentence = sentence.replace(mention, str(discord.utils.get(client.get_all_members(), id=mention[2:-1]).name))
        letter = list(str(sentence.lower()))
        for char in range(len(letter)):
            if letter[char] == " ":lst += "<:blank:569189027316629505>"
            elif any(x in letter[char] for x in ["â","ä","à","å"]):lst += ":regional_indicator_a:"
            elif any(x in letter[char] for x in ["ê","ë","è","é"]):lst += ":regional_indicator_e:"
            elif any(x in letter[char] for x in ["î","ï","ì","í"]):lst += ":regional_indicator_i:"
            elif any(x in letter[char] for x in ["ô","ö","ò","ó"]):lst += ":regional_indicator_o:"
            elif any(x in letter[char] for x in ["û","ü","ù","ú"]):lst += ":regional_indicator_u:"
            elif letter[char] == "ç":lst += ":regional_indicator_c:"
            elif letter[char] == "←":lst += ":arrow_left:"
            elif letter[char] == "↑":lst += ":arrow_up:"
            elif letter[char] == "↓":lst += ":arrow_down:"
            elif letter[char] == "→":lst += ":arrow_right:"
            elif letter[char] == "$":lst += ":dollar:"
            elif letter[char] == "€":lst += ":euro:"
            elif letter[char] == "£":lst += ":pound:"
            elif letter[char] == "#":lst += ":hash:"
            elif letter[char] == "æ":lst += emo("a_variation")
            elif letter[char] == "œ":lst += emo("o_variation")
            elif letter[char] == "^":lst += emo("accent_circumflex")
            elif letter[char] == "¨":lst += emo("accent_doublepoint")
            elif letter[char] == "`":lst += emo("accent_grave")
            elif letter[char] == "&":lst += emo("and")
            elif letter[char] == "~":lst += emo("approximately")
            elif letter[char] == "@":lst += emo("at")
            elif letter[char] == "\\":lst += emo("backslash")
            elif letter[char] == ":":lst += emo("colons")
            elif letter[char] == ",":lst += emo("comma")
            elif letter[char] == "©":lst += emo("copyright")
            elif letter[char] == "-":lst += emo("dash")
            elif letter[char] == "°":lst += emo("degree")
            elif letter[char] == "δ":lst += emo("delta")
            elif letter[char] == "÷":lst += emo("divide")
            elif letter[char] == ".":lst += emo("dot")
            elif letter[char] == '"':lst += emo("double_quotes")
            elif letter[char] == "=":lst += emo("equal")
            elif letter[char] == "!":lst += emo("exclamation")
            elif letter[char] == "<":lst += emo("inferior")
            elif letter[char] == "∞":lst += emo("infinite")
            elif letter[char] == "{":lst += emo("left_brace")
            elif letter[char] == "[":lst += emo("left_bracket")
            elif letter[char] == "(":lst += emo("left_parenthese")
            elif letter[char] == "µ":lst += emo("micro")
            elif letter[char] == "*":lst += emo("multiply")
            elif letter[char] == "§":lst += emo("paragraph")
            elif letter[char] == "%":lst += emo("percent")
            elif letter[char] == "π":lst += emo("pi")
            elif letter[char] == "?":lst += emo("question")
            elif letter[char] == "'":lst += emo("quote")
            elif letter[char] == "®":lst += emo("registered")
            elif letter[char] == "}":lst += emo("right_brace")
            elif letter[char] == "]":lst += emo("right_bracket")
            elif letter[char] == ")":lst += emo("right_parenthese")
            elif letter[char] == ";":lst += emo("semicolons")
            elif letter[char] == "/":lst += emo("slash")
            elif letter[char] == ">":lst += emo("superior")
            elif letter[char] == "_":lst += emo("underscore")
            elif letter[char] == "¤":lst += emo("unknow_currency")
            elif letter[char] == "²":lst += emo("upper_2")
            elif letter[char] == "|":lst += emo("vertical_bar")
            elif letter[char] == "0":lst += ":zero:"
            elif letter[char] == "1":lst += ":one:"
            elif letter[char] == "2":lst += ":two:"
            elif letter[char] == "3":lst += ":three:"
            elif letter[char] == "4":lst += ":four:"
            elif letter[char] == "5":lst += ":five:"
            elif letter[char] == "6":lst += ":six:"
            elif letter[char] == "7":lst += ":seven:"
            elif letter[char] == "8":lst += ":eight:"
            elif letter[char] == "9":lst += ":nine:"
            elif letter[char].isalpha() == True:
                lst += ":regional_indicator_" + letter[char] + ":"
            elif letter[char] == "☺":
                lst.append(str(emojis_used[0]))
                del emojis_used[0]
            else:
                lst.append("<:unknown:569176260241260564>")
        content = "".join(lst)
        comb = lambda s,n: [s[i:i+n] for i in range(0,len(s),n)]
        embeds_temp = comb(content, 2012)
        embeds = []
        temp = [""]
        for x in embeds_temp:
            b = re.split("(<\w*:\w*:\d*>)", x)[0:-1]
            embeds.append("".join(temp + b))
            if not b:
                embeds[len(embeds_temp)-1] = embeds[len(embeds_temp)-1] + embeds_temp[-1][-1]
            temp = re.split("(<\w*:\w*:\d*>)", x)[-1:len(x)]
        for content in embeds:
            embed = discord.Embed(title=None, description=content, color=0xFFA952)
            if content == embeds[-1]:
                if lang_server == "fr":
                    embed.set_footer(text=f"Demandé par : {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
                elif lang_server == "en":
                    embed.set_footer(text=f"Requested by: { ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
                elif lang_server == "de":
                    embed.set_footer(text=f"Angefordert von: { ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
                return await ctx.send(embed=embed)
            await ctx.send(embed=embed)

@client.command(pass_context=True, aliases=["embeds", "richembed"])
async def embed(ctx, *, args=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        def random_color():
            r = lambda: random.randint(0, 255)
            return "0x%02X%02X%02X" % (r(),r(),r())

        if not args:
            if lang_server == "fr":
                return await ctx.send("Merci de préciser un argument valide : `+embed T=Titre D=Description C=Couleur I=ImageURL F=Footer U=URL A=Auteur`.")
            elif lang_server == "en":
                return await ctx.send("Please specify a valid argument: `+embed T=Title D=Description C=Color I=ImageURL F=Footer U=URL A=Author`.")
            elif lang_server == "de":
                return await ctx.send("Bitte geben Sie eine ein richtiges Argument: `+embed T=Title D=Description C=Color I=ImageURL F=Footer U=URL A=Author`.")

        with open("extra/colors_embed.json", encoding="utf-8") as file:
            colors_embed = json.load(file)

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
            title = args
        if not title:
            if description:
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
                        if lang_server == "fr":
                            return await ctx.send("La couleur mentionnée n'existe pas. Paramètres supportés : `nom couleur`, `valeur hexa`, `valeur nombre entier`, `random`.")
                        elif lang_server == "en":
                            return await ctx.send("The mentionned color does not exists. Supported parameters: `color name`, `hex value`, `int value`, `random`.")
                        elif lang_server == "en":
                            return await ctx.send("Die angegebene Farbe existiert nicht. Unterstützte Parameter: `Farbname`, ` Hex-Wert`, `Nummer-Wert`, `random`.")
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
            if lang_server == "fr":
                embed.set_footer(text=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            elif lang_server == "en":
                embed.set_footer(text=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            elif lang_server == "de":
                embed.set_footer(text=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        return await ctx.send(embed=embed)

@client.command(pass_context=True, aliases=["listebans", "banlist"])
async def listbans(ctx):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        if lang_server == "fr":
            msg_any = "Aucun"
        elif lang_server == "en":
            msg_any = "None"
        elif lang_server == "de":
            msg_any = "Keine"

        list_banned = await ctx.guild.bans()
        if list_banned:
            content = "\n- ".join([x[1].name for x in list_banned])
        else:
            content = msg_any
        if lang_server == "fr":
            embed = discord.Embed(title="Liste des membres bannis :", description="- " + content, color=0xFF0000)
        elif lang_server == "en":
            embed = discord.Embed(title="List of banned members:", description="- " + content, color=0xFF0000)
        elif lang_server == "de":
            embed = discord.Embed(title="Liste der verbotenen Mitglied:", description="- " + content, color=0xFF0000)
        return await ctx.send(embed=embed)

@client.command(pass_context=True, no_pm=True, aliases=["listeinvites", "invitelist"])
async def listinvites(ctx):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        if lang_server == "fr":
            msg_any = "Aucuns"
        elif lang_server == "en":
            msg_any = "None"
        elif lang_server == "de":
            msg_any = "Keine"

        list_invites = await ctx.guild.invites()
        if list_invites:
            content = "\n- ".join([x.url for x in list_invites])
        else:
            content = msg_any
        if lang_server == "fr":
            embed = discord.Embed(title="Liens d'invitation :", description="- " + content, color=0x00FFFF)
        elif lang_server == "en":
            embed = discord.Embed(title="Invite links:", description="- " + content, color=0x00FFFF)
        elif lang_server == "de":
            embed = discord.Embed(title="Einladungslinks:", description="- " + content, color=0x00FFFF)
        return await ctx.send(embed=embed)

@client.command(pass_context=True, aliases=["listserveurs", "listserver", "listeserveurs", "serverlist", "serverliste", "servlist", "servelist", "listservs"])
async def listservers(ctx):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        if not server_id == 264445053596991498: # DBL ID
            serv_id = [str(server.id) for server in client.guilds]
            serv_id_exist = []
            serv_pos = []

            count = 0
            with open("extra/data.txt", "r", encoding="utf-8") as file:
                for line in file:
                    count += 1
                    for server in serv_id:
                        if server in line:
                            serv_pos.append(count)
                            serv_id_exist.append(server)

            if lang_server == "fr":
                content = "**__Nom du serveur | Position enregistrée__**"
            elif lang_server == "en":
                content = "**__Server name | Registered position__**"
            elif lang_server == "de":
                content = "**__Servername | Registrierte Position__**"
            content2 = ""
            for pos in range(len(serv_id_exist)):
                if len(content) < 2000:
                    content += "\n- " + str(client.get_guild(int(serv_id_exist[pos]))) + " | " + str(serv_pos[pos])
                else:
                    content2 += "\n- " + str(client.get_guild(int(serv_id_exist[pos]))) + " | " + str(serv_pos[pos])
            if lang_server == "fr":
                embed = discord.Embed(title=f"Serveurs : {len(client.guilds)}", description=content, color=0xFF9000)
            elif lang_server == "en":
                embed = discord.Embed(title=f"Servers: {len(client.guilds)}", description=content, color=0xFF9000)
            elif lang_server == "de":
                embed = discord.Embed(title=f"Server: {len(client.guilds)}", description=content, color=0xFF9000)
            if not content2 == "":
                embed2 = discord.Embed(title=None, description=content2, color=0xFF9000)
                await ctx.send(embed=embed)
                return await ctx.send(embed=embed2)
            else:
                return await ctx.send(embed=embed)

@client.command(pass_context=True, aliases=["totalmsg"])
async def msgtotal(ctx, *args):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        if not ctx.message.channel.guild.me.guild_permissions.administrator:
            if lang_server == "fr":
                return await ctx.send(":x: Il manque la permissions **Administrateur** au bot.")
            elif lang_server == "en":
                return await ctx.send(":x: The bot is missing **Administrator** permissions.")
            elif lang_server == "de":
                return await ctx.send(":x: Dem Bot fehlen **Administrator** Berechtigungen.")
        if len(args) == 2:
            member = discord.utils.get(client.get_all_members(), id=str(args[1])[2:-1])
            args = args[0]
        elif len(args) == 1:
            args = args[0]
            if str(args)[2:-1].isdigit():
                member = discord.utils.get(client.get_all_members(), id=str(args)[2:-1])
                args = "all"
            elif not args == "all" and not args == "channel":
                if lang_server == "fr":
                    return await ctx.send("Merci de préciser un argument valide : `+msgtotal [all / channel] [@membre]`.")
                elif lang_server == "en":
                    return await ctx.send("Please specify a valid argument: `+msgtotal channel [@membre]` ou `+msgtotal all [@membre]`.")
                elif lang_server == "de":
                    return await ctx.send("Bitte geben Sie eine richtiges Argument: `+msgtotal channel [@membre]` ou `+msgtotal all [@membre]`.")
            else:
                member = ctx.message.author
        else:
            member = ctx.message.author
            args = "all"

        if not isinstance(ctx.channel, discord.TextChannel):
            args = "channel"
        counter = 0
        if lang_server == "fr":
            embed = discord.Embed(title="Calcul des messages...", color=0xFFA500)
        elif lang_server == "en":
            embed = discord.Embed(title="Calculating messages...", color=0xFFA500)
        elif lang_server == "de":
            embed = discord.Embed(title="Nachrichten werden berechnet...", color=0xFFA500)
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
            if lang_server == "fr":
                return await ctx.send("Merci de préciser un argument valide : `+msgtotal [all / channel] [@membre]`.")
            elif lang_server == "en":
                return await ctx.send("Please specify a valid argument: `+msgtotal channel [@membre]` ou `+msgtotal all [@membre]`.")
            elif lang_server == "de":
                return await ctx.send("Bitte geben Sie eine ein richtiges Argument: `+msgtotal channel [@membre]` ou `+msgtotal all [@membre]`.")

        if lang_server == "fr":
            if msg_total == True:
                content = f"**{member}** a envoyé **{counter}** messages au total."
            else:
                content = f"**{member}** a envoyé **{counter}** messages dans ce channel."
            embed = discord.Embed(title="**Nombre de messages :**", description=content, color=0xFFA500)
            embed.set_footer(text=f"Demandé par : {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        elif lang_server == "en":
            if msg_total == True:
                content = f"**{member}** has sent **{counter}** messages in total."
            else:
                content = f"**{member}** has sent **{counter}** messages in this channel."
            embed = discord.Embed(title="**Number of messages:**", description=content, color=0xFFA500)
            embed.set_footer(text=f"Requested by: { ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        elif lang_server == "de":
            if msg_total == True:
                content = f"**{member}** hast **{counter}** Nachrichten insgesamt gesendet."
            else:
                content = f"**{member}** hast **{counter}** Nachrichten in diesem Chatroom gesendet."
            embed = discord.Embed(title="**Anzahl der Nachrichten:**", description=content, color=0xFFA500)
            embed.set_footer(text="Angefordert von: {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)

        if not isinstance(ctx.channel, discord.TextChannel):
            return await tmp.edit(embed=embed)
        await tmp.edit(embed=embed)
        await asyncio.sleep(5)
        return await ctx.message.delete()

@client.command(pass_context=True, aliases=["lyric", "paroles", "parole"])
async def lyrics(ctx, *, args):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        if not args:
            if lang_server == "fr":
                return await ctx.send("Merci de préciser une musique.")
            elif lang_server == "en":
                return await ctx.send("Please specify a music.")
            elif lang_server == "de":
                return await ctx.send("Bitte geben Sie eine Musik.")
        request_uri = "https://api.genius.com/search/"
        params = {"q": args}
        headers = {"Authorization": "Bearer " + token_genius}
        r = requests.get(request_uri, params=params, headers=headers).json()

        if not r["response"]["hits"]:
            if lang_server == "fr":
                return await ctx.send("La musique n'a pas été trouvée ou n'existe pas.")
            elif lang_server == "en":
                return await ctx.send("The music has not been found or does not exist.")
            elif lang_server == "de":
                return await ctx.send("Die Musik wurde nicht gefunden oder existiert nicht.")
        path_lyrics = r["response"]["hits"][0]["result"]["path"]
        URL = "https://genius.com" + path_lyrics
        page = requests.get(URL)
        html = BeautifulSoup(page.text, "html.parser")

        try:lyrics = html.find("div", class_="lyrics").get_text()
        except:
            if lang_server == "fr":
                return await ctx.send("La musique demandée ne contient pas de paroles.")
            elif lang_server == "en":
                return await ctx.send("The requested music does not contain lyrics.")
            elif lang_server == "de":
                return await ctx.send("Die angeforderte Musik enthält keinen Text.")
        if len(lyrics) > 5900:
            if lang_server == "fr":
                return await ctx.send("Le résultat est trop long (limite discord). Cela peut être aussi causé par l'absence de lyrics de vôtre recherche.")
            elif lang_server == "en":
                return await ctx.send("The result is too long (discord limit). This can also be caused by the absence of lyrics from your research.")
            elif lang_server == "de":
                return await ctx.send("Das Ergebnis ist zu lang (Discord Limit). Dies kann auch durch das Fehlen von Texten aus Ihrer Forschung verursacht werden.")
        title = r["response"]["hits"][0]["result"]["full_title"]
        image = r["response"]["hits"][0]["result"]["header_image_url"]
        if not any(x.lower() in title.lower() for x in args.split(" ")):
            if lang_server == "fr":
                await ctx.send("La recherche ne correspond pas au titre, assurez vous d'avoir bien entré le nom de la musique.")
                await ctx.send(f"Résultat trouvé avec : **{args}**")
            elif lang_server == "en":
                await ctx.send("The search does not match the title, make sure you have entered the name of the music.")
                await ctx.send(f"Result found with: **{args}**")
            elif lang_server == "de":
                await ctx.send("Die Suche stimmt nicht mit dem Titel überein. Vergewissern Sie sich, dass Sie den Namen der Musik eingegeben haben.")
                await ctx.send(f"Ergebnis gefunden mit: **{args}**")
        if lang_server == "fr":
            embed = discord.Embed(title=f"Paroles de : __**{title}**__", description=None, color=0x00FFFF)
        elif lang_server == "en":
            embed = discord.Embed(title=f"Lyrics of: __**{title}**__", description=None, color=0x00FFFF)
        elif lang_server == "de":
            embed = discord.Embed(title=f"Songtexte von: __**{title}**__", description=None, color=0x00FFFF)
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
        if lang_server == "fr":
            embed.set_footer(text=f"Demandé par : {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        elif lang_server == "en":
            embed.set_footer(text=f"Requested by: { ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        elif lang_server == "de":
            embed.set_footer(text=f"Angefordert von: { ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        return await ctx.send(embed=embed)

@client.command(pass_context=True, aliases=["meteo"])
async def weather(ctx, *, args=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        if lang_server == "fr":
            msg_condition = "Condition météo :"
            msg_cloud = ":cloud: Nuageux : "
            msg_rain = ":cloud_rain: Volume de pluie (dernières 3h) : "
            msg_snow = ":cloud_snow: Volume de neige (dernières 3h) : "
            msg_temp = ":thermometer: Température :"
            msg_humidity = ":sweat_drops: Humidité : "
            msg_wind = ":wind_blowing_face: Vitesse du vent :"
            msg_city = "Météo actuelle à "
            msg_local_time = "Date locale :"
            msg_sunrise = "Lever du soleil :"
            msg_sunset = " • Coucher du soleil :"
        elif lang_server == "en":
            msg_condition = "Weather condition:"
            msg_cloud = ":cloud: Cloudiness: "
            msg_rain = ":cloud_rain: Rain volume (last 3h): "
            msg_snow = ":cloud_snow: Snow volume (last 3h): "
            msg_temp = ":thermometer: Temperature:"
            msg_humidity = ":sweat_drops: Humidity: "
            msg_wind = ":wind_blowing_face: Wind speed:"
            msg_city = "Current weather at "
            msg_local_time = "Local date:"
            msg_sunrise = "Sunrise:"
            msg_sunset = " • Sunset:"
        elif lang_server == "de":
            msg_condition = "Wetterlage:"
            msg_cloud = ":cloud: Trübung: "
            msg_rain = ":cloud_rain: Regenvolum (letzte 3h): "
            msg_snow = ":cloud_snow: Schneevolum (letzte 3h): "
            msg_temp = ":thermometer: Temperatur:"
            msg_humidity = ":sweat_drops: Feuchtigkeit: "
            msg_wind = ":wind_blowing_face: Windgeschwindigkeit:"
            msg_city = "Aktuelles Wetter bei "
            msg_local_time = "Lokales Datum:"
            msg_sunrise = "Sonnenaufgang:"
            msg_sunset = " • Sonnenuntergang:"

        if not args:
            if lang_server == "fr":
                embed = discord.Embed(title="Merci de préciser une ville.", color=0x00FFFF)
            elif lang_server == "en":
                embed = discord.Embed(title="Please specify a city.", color=0x00FFFF)
            elif lang_server == "de":
                embed = discord.Embed(title="Bitte geben Sie eine Stadt an.", color=0x00FFFF)
            return await ctx.send(embed=embed)
        args = args.replace(" ", "%20")
        url = "http://api.openweathermap.org/data/2.5/weather?q=" + args
        data = requests.get(url + f"&appid={token_weather}&lang={lang_server}").json()
        if "city not found" in str(data):
            if lang_server == "fr":
                embed = discord.Embed(title="La ville n'a pas été trouvée.", color=0x00FFFF)
            elif lang_server == "en":
                embed = discord.Embed(title="The city was not found.", color=0x00FFFF)
            elif lang_server == "de":
                embed = discord.Embed(title="Die Stadt wurde nicht gefunden.", color=0x00FFFF)
            return await ctx.send(embed=embed)
        if not data["coord"]:
            return False
        lat, long = str(data["coord"]["lat"]), str(data["coord"]["lon"])
        url = f"http://api.timezonedb.com/v2/get-time-zone?key={token_timezone}&format=json&by=position&lat={lat}&lng={long}"
        try:current_time = requests.get(url).json()["formatted"]
        except:current_time = data["dt"]
        emoji = discord.utils.get(client.emojis, name=str(data["weather"][0]["icon"]))
        condition = data["weather"][0]["main"]
        if lang_server == "fr":
            if condition == "Thunderstorm": condition = "Orage"
            if condition == "Drizzle": condition = "Bruine"
            if condition == "Rain": condition = "Pluie"
            if condition == "Snow": condition = "Neige"
            if condition == "Mist": condition = "Brouillard"
            if condition == "Clear": condition = "Clair"
            if condition == "Clouds": condition = "Nuages"
            if condition == "Tornado": condition = "Tornade"
            if condition == "Haze": condition = "Brume"
        elif lang_server == "de":
            if condition == "Thunderstorm": condition = "Gewitter"
            if condition == "Drizzle": condition = "Nieselregen"
            if condition == "Rain": condition = "Regen"
            if condition == "Snow": condition = "Schnee"
            if condition == "Mist": condition = "Nebel"
            if condition == "Clear": condition = "Klar"
            if condition == "Clouds": condition = "Wolken"
            if condition == "Haze": condition = "Nebel"
        desc = str(data["weather"][0]["description"])
        content = f"{emoji} {msg_condition} {condition} - \"{desc.title()}\"\n"
        try:
            content += msg_cloud + str(data["clouds"]["all"]) + "%\n"
        except:pass
        try:
            content += msg_rain + str(data["rain"]["3h"]) + "L/m²\n"
        except:pass
        try:
            content += msg_snow + str(data["snow"]["3h"]) + "L/m²\n"
        except:pass
        temp_celcius = str(round(data["main"]["temp"] - 273.15, 1))
        temp_farenheit = str(round(data["main"]["temp"] * 9/5 - 459.67, 1))
        if lang_server == "fr" or lang_server == "de":
            content += f"{msg_temp} {temp_celcius}°C\n"
        elif lang_server == "en":
            content += f"{msg_temp} {temp_celcius}°C - {temp_farenheit}°F\n"
        content += msg_humidity + str(data["main"]["humidity"]) + "%\n"
        wind_speed = data["wind"]["speed"]
        content += f"{msg_wind} {float(wind_speed)}m/s - {round(float(wind_speed) * 3.6, 1)}km/h\n\n"
        sunrise_time = datetime.fromtimestamp(int(data["sys"]["sunrise"])).strftime("%H:%M:%S")
        sunset_time = datetime.fromtimestamp(int(data["sys"]["sunset"])).strftime("%H:%M:%S")
        content += f"<:time:475328338542592000> {msg_sunrise} {sunrise_time} {msg_sunset} {sunset_time} (DST)"
        embed = discord.Embed(title=msg_city + data["name"] + " :flag_" + str(data["sys"]["country"]).lower() + ":\n", description=content, color=0x00FFFF)
        embed.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/{emoji.id}.png")
        embed.set_footer(text=f"{msg_local_time} {current_time}", icon_url="https://cdn.discordapp.com/emojis/475328334557872129.png")
        return await ctx.send(embed=embed)

@client.command(pass_context=True, no_pm=True, aliases=["serveurstats", "statsserveur", "statserveur", "statserver"])
async def serverstats(ctx):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        if lang_server == "fr":
            msg_any = "Aucun"
            msg_low = "Faible"
            msg_medium = "Moyen"
            msg_high = "Elevé"
            msg_extreme = "Extrême"
            msg_limit = "La longueur de la liste des rôles est supérieure à ce que discord peut envoyer."
        elif lang_server == "en":
            msg_any = "None"
            msg_low = "Low"
            msg_medium = "Medium"
            msg_high = "High"
            msg_extreme = "Extreme"
            msg_limit = "The length of the roles list is greater than what discord can send."
        elif lang_server == "de":
            msg_any = "Keine"
            msg_low = "Niedrig"
            msg_medium = "Mittel"
            msg_high = "Hoch"
            msg_extreme = "Extrem"
            msg_limit = "Die länge der Rollenliste ist Größer als die die Discord senden kann."

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
        serv_afk_channel = msg_any if serv.afk_channel == None else str(serv.afk_channel)
        serv_afk_time = str(round(int(serv.afk_timeout) / 60))
        verif = str(serv.verification_level)
        if verif == "none":
            serv_verif_lvl = msg_any
        elif verif == "low":
            serv_verif_lvl = msg_low
        elif verif == "medium":
            serv_verif_lvl = msg_medium
        elif verif == "high":
            serv_verif_lvl = msg_high
        elif verif == "extreme":
            serv_verif_lvl = msg_extreme
        serv_roles = str(len([x.name for x in serv.roles]))
        serv_roles_list = ", ".join([x.name for x in serv.roles])
        if len(serv_roles_list) > 500:
            serv_roles_list = msg_limit

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

        if lang_server == "fr":
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
            embed.add_field(name=f"Statistiques du serveur __***{serv_name}***__", value=content + " ***[Lien Icône]({})***".format(icon_url), inline=True)
            embed.set_footer(text=f"Demandé par : {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        elif lang_server == "en":
            content =   "```autohotkey\n" \
                        "Name:               %s\n" \
                        "ID:                 %s\n" \
                        "Owner:              %s (%s)\n" \
                        "Created at:         %s\n" \
                        "Region:             %s\n" \
                        "Members:            %s (%s Online)\n" \
                        "    Users:          %s (%s Online)\n" \
                        "    Bots:           %s (%s Online)\n" \
                        "Channels:           %s\n" \
                        "    Text:           %s\n" \
                        "    Voice:          %s\n" \
                        "AFK Channel:        %s\n" \
                        "AFK Time:           %s min\n" \
                        "Verify level:       %s\n" \
                        "Roles:              %s\n" \
                        "%s" \
                        "```" % (serv_name, serv_id, serv_owner, serv_owner_dis, serv_created, serv_region, serv_members,
                                 serv_members_on, serv_users, serv_users_on, serv_bots, serv_bots_on, serv_channels, serv_text_channels,
                                 serv_voice_channels, serv_afk_channel, serv_afk_time, serv_verif_lvl, serv_roles, serv_roles_list)
            embed.add_field(name=f"Statistics of __***{serv_name}***__ Server", value=content + " ***[Icon Link]({})***".format(icon_url), inline=True)
            embed.set_footer(text=f"Requested by: { ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        elif lang_server == "de":
            content =   "```autohotkey\n" \
                        "Name:               %s\n" \
                        "ID:                 %s\n" \
                        "Inhaber:            %s (%s)\n" \
                        "Hergestellt in:     %s\n" \
                        "Region:             %s\n" \
                        "Mitglied:           %s (%s Online)\n" \
                        "    Leute:          %s (%s Online)\n" \
                        "    Bots:           %s (%s Online)\n" \
                        "Kanäle:             %s\n" \
                        "    Text:           %s\n" \
                        "    Sprach:         %s\n" \
                        "AFK Kanäle:         %s\n" \
                        "AFK Zeit:           %s min\n" \
                        "Verify Stufe:       %s\n" \
                        "Rollen:             %s\n" \
                        "%s" \
                        "```" % (serv_name, serv_id, serv_owner, serv_owner_dis, serv_created, serv_region, serv_members,
                                 serv_members_on, serv_users, serv_users_on, serv_bots, serv_bots_on, serv_channels, serv_text_channels,
                                 serv_voice_channels, serv_afk_channel, serv_afk_time, serv_verif_lvl, serv_roles, serv_roles_list)
            embed.add_field(name=f"__***{serv_name}***__'s Serverstatistiken", value=content + " ***[Symbolverbindung]({})***".format(icon_url), inline=True)
            embed.set_footer(text=f"Angefordert von: { ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        return await ctx.send(embed=embed)

@client.command(pass_context=True, no_pm=True, aliases=["statsuser"])
async def userstats(ctx, *, member : discord.Member=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        if lang_server == "fr":
            msg_any = "Aucun"
            msg_yes = "Oui"
            msg_no = "Non"
            msg_online = "En ligne"
            msg_offline = "Hors ligne"
            msg_idle = "Absent"
            msg_dnd = "Ne pas déranger"
            msg_invisible = "Invisible"
        elif lang_server == "en":
            msg_any = "None"
            msg_yes = "Yes"
            msg_no = "No"
            msg_online = "Online"
            msg_offline = "Offline"
            msg_idle = "Absent"
            msg_dnd = "Do not disturb"
            msg_invisible = "Invisible"
        elif lang_server == "de":
            msg_any = "Keine"
            msg_yes = "Ja"
            msg_no = "Nein"
            msg_online = "Online"
            msg_offline = "Offline"
            msg_idle = "Abwesend"
            msg_dnd = "Beschäftigt"
            msg_invisible = "Unsichtbar"

        if not member:
            member = ctx.message.author
        user_name = member.name
        user_nickname = msg_any if member.nick == None else str(member.nick)
        user_id = str(member.id)
        user_tag = member.name + "#" + member.discriminator
        user_mention = member.mention
        user_is_bot = msg_yes if member.bot == True else msg_no
        status = str(member.status).lower()
        if status == "online":
            user_status = msg_online
        elif status == "offline":
            user_status = msg_offline
        elif status == "idle":
            user_status = msg_idle
        elif status == "dnd":
            user_status = msg_dnd
        elif status == "invisible":
            user_status = msg_invisible
        user_game = msg_any if member.activity == None else str(member.activity.name)
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
        if member.avatar_url is not None:
            embed.set_thumbnail(url=avatar_url)
        else:
            embed.set_thumbnail(url=member.default_avatar_url)

        if lang_server == "fr":
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
            embed.add_field(name=f"Statistiques de __***{user_name}***__", value=content + " ***[Lien Icône]({})***".format(avatar_url), inline=True)
            embed.set_footer(text=f"Demandé par : {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        elif lang_server == "en":
            content =   "```autohotkey\n" \
                        "Name:               %s\n" \
                        "Nickname:           %s\n" \
                        "ID:                 %s\n" \
                        "Tag:                %s\n" \
                        "Mention:            %s\n" \
                        "Bot:                %s\n" \
                        "Status:             %s\n" \
                        "Game:               %s\n" \
                        "Join server at:     %s\n" \
                        "Join Discord at:    %s\n" \
                        "Best Role:          %s\n" \
                        "Roles:              %s\n" \
                        "%s" \
                        "```" % (user_name, user_nickname, user_id, user_tag, user_mention, user_is_bot, user_status,
                                 user_game, user_joinserv, user_joindiscord, user_best_role, user_roles, user_roles_list)
            embed.add_field(name=f"Statistics of __***{user_name}***__", value=content + " ***[Icon Link]({})***".format(avatar_url), inline=True)
            embed.set_footer(text=f"Requested by: { ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        elif lang_server == "de":
            content =   "```autohotkey\n" \
                        "Name:               %s\n" \
                        "Spitzname:          %s\n" \
                        "ID:                 %s\n" \
                        "Tag:                %s\n" \
                        "Erwähnung:          %s\n" \
                        "Bot:                %s\n" \
                        "Status:             %s\n" \
                        "Spielt:             %s\n" \
                        "Trat Server bei:    %s\n" \
                        "Trat Discord bei:   %s\n" \
                        "Primaire Rolle:     %s\n" \
                        "Rollen:             %s\n" \
                        "%s" \
                        "```" % (user_name, user_nickname, user_id, user_tag, user_mention, user_is_bot, user_status,
                                 user_game, user_joinserv, user_joindiscord, user_best_role, user_roles, user_roles_list)
            embed.add_field(name=f"__***{user_name}***__'s Statistiken", value=content + " ***[Symbolverbindung]({})***".format(avatar_url), inline=True)
            embed.set_footer(text="Angefordert von : " + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        return await ctx.send(embed=embed)

@client.command(pass_context=True, aliases=["botstat", "statsbot", "statbot"])
async def botstats(ctx):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name, start_time
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        if lang_server == "fr":
            msg_day = "Jours"
            msg_hour = "Heures"
            msg_minutes = "Minutes"
            msg_seconds = "Secondes"
        elif lang_server == "en":
            msg_day = "Days"
            msg_hour = "Hours"
            msg_minutes = "Minutes"
            msg_seconds = "Seconds."
        elif lang_server == "de":
            msg_day = "Tage"
            msg_hour = "Stunden"
            msg_minutes = "Minuten"
            msg_seconds = "Sekunden"

        bot_host = "Raspberry Pi"
        bot_owner = "QuentiumYT#0207"
        bot_version = "Debian 8.0 (Raspbian)"
        time = round((datetime.now() - start_time).total_seconds())
        m, s = divmod(int(time), 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        bot_uptime = f"{d} {msg_day}, {h} {msg_hour}, {m} {msg_minutes}, {s} {msg_seconds}"
        bot_memory = int(psutil.virtual_memory()[0] / int(2 ** 20)) - int(psutil.virtual_memory()[4] / int(2 ** 20))
        if isinstance(ctx.channel, discord.TextChannel):
            bot_commands_get = commands_server
        else:
            if "fr" in clean_line:
                bot_commands_get = "Indisponible en MP"
            elif "en" in clean_line:
                bot_commands_get = "Not available in PM"
            elif "de" in clean_line:
                bot_commands_get = "In PN nicht verfügbar"
        commands_server_total = 0
        with open("extra/data.txt", encoding="utf-8") as file:
             for line in file:
                 clean_line = line.rstrip().split(sep, 999)[3]
                 commands_server_total += int(clean_line)
        bot_commands_get_total = commands_server_total
        users = 0
        for serv in client.guilds:
            users += len(serv.members)
        bot_users_total = str(users)
        bot_servers_total = len(client.guilds)
        with open("extra/data.txt", encoding="utf-8") as file:
            bot_lang_fr = bot_lang_en = bot_lang_de = 0
            for line in file:
                clean_line = line.rstrip().split(sep, 999)[2]
                if "fr" in clean_line:
                    bot_lang_fr += 1
                elif "en" in clean_line:
                    bot_lang_en += 1
                elif "de" in clean_line:
                    bot_lang_de += 1

        embed = discord.Embed(url="https://quentium.fr/discord/", color=0x0026FF)
        embed.set_thumbnail(url="https://quentium.fr/+img/logoBot.png")
        if lang_server == "fr":
            content =   "```autohotkey\n" \
                        "Hébergée sur:         %s\n" \
                        "Propriétaire:         %s\n" \
                        "Linux version:        %s\n" \
                        "Durée fonctionnement: %s\n" \
                        "Mémoire utilisée:     %s Mo\n" \
                        "Commandes reçues:     %s (serveur)\n" \
                        "Commandes reçues:     %s (total)\n" \
                        "Statistiques:         %s utilisateurs dans %s serveurs\n" \
                        "Serveurs FR:          %s\n" \
                        "Serveurs EN:          %s\n" \
                        "Serveurs DE:          %s\n" \
                        "```" % (bot_host, bot_owner, bot_version, bot_uptime, bot_memory, bot_commands_get,
                                 bot_commands_get_total, bot_users_total, bot_servers_total, bot_lang_fr, bot_lang_en, bot_lang_de)
            embed.add_field(name="Statistiques du __***QuentiumBot***__", value=content, inline=True)
            embed.set_footer(text=f"Demandé par : {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        elif lang_server == "en":
            content =   "```autohotkey\n" \
                        "Hosted on:            %s\n" \
                        "Owner:                %s\n" \
                        "Linux version:        %s\n" \
                        "Uptime:               %s\n" \
                        "Memory used:          %s MB\n" \
                        "Commands recieved:    %s (server)\n" \
                        "Commands recieved:    %s (total)\n" \
                        "Stats:                %s users on %s servers\n" \
                        "Servers FR:           %s\n" \
                        "Servers EN:           %s\n" \
                        "Servers DE:           %s\n" \
                        "```" % (bot_host, bot_owner, bot_version, bot_uptime, bot_memory, bot_commands_get,
                                 bot_commands_get_total, bot_users_total, bot_servers_total, bot_lang_fr, bot_lang_en, bot_lang_de)
            embed.add_field(name="Statistics of __***QuentiumBot***__", value=content, inline=True)
            embed.set_footer(text=f"Requested by: { ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        elif lang_server == "de":
            content =   "```autohotkey\n" \
                        "Gehostet auf:         %s\n" \
                        "Inhaber:              %s\n" \
                        "Linux Version:        %s\n" \
                        "Betriebszeit:         %s\n" \
                        "Arbeitsspeicher:      %s MB\n" \
                        "Befehle bekommen:     %s (server)\n" \
                        "Befehle bekommen:     %s (insgesammt)\n" \
                        "Statistiken:          %s Benutzer in %s Servers\n" \
                        "Servers FR:           %s\n" \
                        "Servers EN:           %s\n" \
                        "Servers DE:           %s\n" \
                        "```" % (bot_host, bot_owner, bot_version, bot_uptime, bot_memory, bot_commands_get,
                                 bot_commands_get_total, bot_users_total, bot_servers_total, bot_lang_fr, bot_lang_en, bot_lang_de)
            embed.add_field(name="__***QuentiumBot***__'s Statistiken", value=content, inline=True)
            embed.set_footer(text="Angefordert von : " + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        return await ctx.send(embed=embed)

@client.command(pass_context=True, aliases=["av", "avatars"])
async def avatar(ctx, *, member : discord.Member=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

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
        if lang_server == "fr":
            embed.set_footer(text=f"Demandé par : {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        elif lang_server == "en":
            embed.set_footer(text=f"Requested by: { ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        elif lang_server == "de":
            embed.set_footer(text=f"Angefordert von: { ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        return await ctx.send(embed=embed)

@client.command(pass_context=True, aliases=["sharebot", "share"])
async def shareme(ctx):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        if lang_server == "fr":
            return await ctx.send("Tu peux partager ce lien pour m'inviter sur d'autres serveurs :", config["PUBLIC"]["invite"])
        elif lang_server == "en":
            return await ctx.send("You can share this link to invite me to other servers:", config["PUBLIC"]["invite"])
        elif lang_server == "de":
            return await ctx.send("Sie können diesen Link teilen, um mich zu anderen Servern einzuladen:", config["PUBLIC"]["invite"])

@client.command(pass_context=True, aliases=["pong"])
async def ping(ctx):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        before = time.perf_counter()
        await ctx.trigger_typing()
        ping = round((time.perf_counter() - before) * 500)
        before = time.monotonic()
        tmp = await ctx.send("***Ping message***")
        ping1 = round((time.monotonic() - before) * 500)
        await tmp.delete()
        if lang_server == "fr":
            return await ctx.send(f":ping_pong: Pong!\n- Latence du bot : `{ping}ms`\n- Latence d'envoi de message : `{ping1}ms`")
        elif lang_server == "en":
            return await ctx.send(f":ping_pong: Pong!\n- Bot's latency: `{ping}ms`\n- Message sending latency: `{ping1}ms`")
        elif lang_server == "de":
            return await ctx.send(f":ping_pong: Pong!\n- Bot's Latenz: `{ping}ms`\n- Nachrichtensende-Latenz: `{ping1}ms`")

@client.command(pass_context=True, aliases=["mc", "omg", "omgserv"])
@commands.cooldown(2, 10, commands.BucketType.channel)
async def minecraft(ctx, * , omg_id=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        # 22915
        if ctx.message.author.id == 247775235913285632: # SpaceDragon user ID
            omg_id = "236885"
        if not omg_id:
            if lang_server == "fr":
                return await ctx.send("Veuillez renseigner l'id de vôtre serveur OMGServ.")
            elif lang_server == "en":
                return await ctx.send("Please enter the id of your OMGServ server.")
            elif lang_server == "de":
                return await ctx.send("Bitte geben Sie die ID Ihres OMGServ-Server ein.")
        if not omg_id.isdigit():
            if lang_server == "fr":
                return await ctx.send("L'id OMGServ n'est pas un nombre.")
            elif lang_server == "en":
                return await ctx.send("The OMGServ id is not a number.")
            elif lang_server == "de":
                return await ctx.send("Die OMGServ-ID ist nicht ein Zahl.")
        data = requests.get(f"https://panel.omgserv.com/json/{omg_id}/players").json()
        data2 = requests.get(f"https://panel.omgserv.com/json/{omg_id}/status").json()
        if "Access denied" in str(data2):
            if lang_server == "fr":
                return await ctx.send("L'id OMGServ n'existe pas.")
            elif lang_server == "en":
                return await ctx.send("The OMGServ id does not exist.")
            elif lang_server == "de":
                return await ctx.send("Die OMGServ-ID existiert nicht!")
        if not "Invalid type" in str(data):
            list_players = sorted([x for x in eval(str(data["players"]))], key=lambda x: x.casefold())
        else:
            list_players = False

        ImageFile.MAXBLOCK = 2**20
        img = Image.open("extra/background.jpg")
        W, H = img.size
        font1 = ImageFont.truetype("extra/MikadoUltra.ttf", 120)
        font2 = ImageFont.truetype("extra/MikadoUltra.ttf", 90)
        font3 = ImageFont.truetype("extra/MikadoUltra.ttf", 70)
        draw = ImageDraw.Draw(img)
        if lang_server == "fr":
            msg_title = "Statistiques du Serveur"
        elif lang_server == "en":
            msg_title = "Server Statistics"
        elif lang_server == "de":
            msg_title = "Serverstatistik"
        w, h = draw.textsize(msg_title, font=font1)
        draw.text(((W - w)/2, 20), msg_title, font=font1, fill=(0, 255, 0))

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
            if lang_server == "fr":
                msg_empty_server = "Serveur vide !"
            elif lang_server == "en":
                msg_empty_server = "Empty server!"
            elif lang_server == "de":
                msg_empty_server = "Leerer Server!"
            draw.text((200, 300), msg_empty_server, font=font1, fill=(0, 0, 255))

        try:status = "Online" if str(data2["status"]["online"]) == "True" else "Offline"
        except:status = "Unknown"
        try:cpu_percent = str(data2["status"]["cpu"])
        except:cpu_percent = "Ø"
        try:ram_number = str(data2["status"]["ram"])
        except:ram_number = "Ø"
        try:max_players = str(data2["status"]["players"]["max"])
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

@client.command(pass_context=True, no_pm=True, aliases=["moves"])
async def move(ctx, *, number=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        if not ctx.message.author.guild_permissions.move_members:
            if lang_server == "fr":
                return await ctx.send(f":x: {ctx.message.author.name}, vous n'avez pas la permission **Déplacer des membres** !")
            elif lang_server == "en":
                return await ctx.send(f":x: {ctx.message.author.name}, you don't have the permission **Move members**!")
            elif lang_server == "de":
                return await ctx.send(f":x: {ctx.message.author.name}, Sie haben nicht die Berechtigung **Mitglieder verschieben**!")
        channel_list = [x for x in ctx.message.guild.channels if isinstance(x, discord.VoiceChannel)]
        if not number:
            if lang_server == "fr":
                content = "Merci de préciser un salon vocal par son numéro.\n\n"
            elif lang_server == "en":
                content = "Please specify a vocal room by its number.\n\n"
            elif lang_server == "de":
                content = "Bitte geben Sie einen Sprachkanäle anhand seiner Nummer an.\n\n"
            numero = 0
            for channel in channel_list:
                numero += 1
                content += "{}. {}\n".format(numero, channel)
            if lang_server == "fr":
                embed = discord.Embed(title="Salons vocaux :", description=content, color=0x3498DB)
            elif lang_server == "en":
                embed = discord.Embed(title="Voice channels:", description=content, color=0x3498DB)
            elif lang_server == "de":
                embed = discord.Embed(title="Sprachkanäle:", description=content, color=0x3498DB)
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
                        if not ctx.message.author.voice == None:
                            if channel.id != ctx.message.author.voice.channel.id:
                                if lang_server == "fr":
                                    await ctx.send("Déplacement dans : " + str(channel))
                                elif lang_server == "en":
                                    await ctx.send("Moving in: " + str(channel))
                                elif lang_server == "de":
                                    await ctx.send("Umzug in: " + str(channel))
                                list_members = []
                                for member in ctx.message.author.voice.channel.members:
                                    list_members.append(member)
                                for member in list_members:
                                    await member.edit(voice_channel=channel)
                            else:
                                if lang_server == "fr":
                                    return await ctx.send("Vous êtes déjà dans le même salon vocal.")
                                elif lang_server == "en":
                                    return await ctx.send("You are already in the same voice channel.")
                                elif lang_server == "de":
                                    return await ctx.send("Sie befinden sich bereits im selben Sprachkanäle.")
                        else:
                            if lang_server == "fr":
                                return await ctx.send("Vous n'êtes pas dans un salon vocal.")
                            elif lang_server == "en":
                                return await ctx.send("You are not in a voice channel.")
                            elif lang_server == "de":
                                return await ctx.send("Sie befinden sich nicht in einer Sprachkanäle.")
                    else:
                        if lang_server == "fr":
                            return await ctx.send("Le numéro de salon ne correspond à aucuns salons vocaux.")
                        elif lang_server == "en":
                            return await ctx.send("The salon number does not correspond to any voice channel.")
                        elif lang_server == "de":
                            return await ctx.send("Die Salonnummer entspricht keinem Sprachkanäle.")
                else:
                    if lang_server == "fr":
                        return await ctx.send("Il n'y à aucuns salons vocaux sur votre serveur.")
                    elif lang_server == "en":
                        return await ctx.send("There are no voice channel on your server.")
                    elif lang_server == "de":
                        return await ctx.send("Auf Ihrem Server sind keine Sprachkanäle vorhanden.")
            else:
                if lang_server == "fr":
                    content = "Merci de préciser un salon vocal par son numéro.\n\n"
                elif lang_server == "en":
                    content = "Please specify a vocal room by its number.\n\n"
                elif lang_server == "de":
                    content = "Bitte geben Sie einen Gesangsraum anhand seiner Nummer an.\n\n"
                numero = 0
                for channel in channel_list:
                    numero += 1
                    content += "{}. {}\n".format(numero, channel)
                if lang_server == "fr":
                    embed = discord.Embed(title="Salons vocaux :", description=content, color=0x3498DB)
                elif lang_server == "en":
                    embed = discord.Embed(title="Voice channels:", description=content, color=0x3498DB)
                elif lang_server == "de":
                    embed = discord.Embed(title="Sprachkanäle:", description=content, color=0x3498DB)
                return await ctx.send(embed=embed)

@client.command(pass_context=True, aliases=["minedt"])
async def dtmine(ctx, *, args=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        if not args:
            if lang_server == "fr":
                return await ctx.send("Il faut spécifier au moins un minerais.")
            elif lang_server == "en":
                return await ctx.send("At least one ore must be specified.")
            elif lang_server == "de":
                return await ctx.send("Es muss mindestens ein Erz angegeben werden.")
        args = args.lower()
        with open("extra/aliases_dt.json", "r", encoding="utf-8") as file:
            aliases_dt = json.load(file)
        with open("extra/mines_dt.json", "r", encoding="utf-8") as file:
            mines = json.load(file)

        try:args = aliases_dt[args]
        except:pass
        ores = mines["0"].keys()
        for area, stats in mines.items():
            for ore in ores:
                if mines[area].get(ore) is None:
                    mines[area].update({ore: 0})

        def best_mines(ore):
            ordered_mines = [(k, v) for k, v in mines.items()]
            ordered_mines.sort(key=lambda x: x[1][ore], reverse=True)
            return ordered_mines
        if args not in mines["0"].keys():
            if lang_server == "fr":
                return await ctx.send(f"Le minerais {args} n'existe pas :frowning:")
            elif lang_server == "en":
                return await ctx.send(f"The ore {args} does not exist :frowning:")
            elif lang_server == "de":
                return await ctx.send(f"Die Erze existieren nicht :Stirnrunzeln:")
        if lang_server == "fr":
            text = f"Voici les 10 meilleurs emplacements pour le minerais {args} :```"
        elif lang_server == "en":
            text = f"Here are the 10 best locations for {args} ores :```"
        elif lang_server == "de":
            text = f"Hier sind die 10 besten Standorte für {args} Erz :```"
        i = 0
        for mine in best_mines(args):
            if i >= 10:
                break
            if mine[0] == "0":
                continue
            text += mine[0].center(3, " ")
            text += " : " + str(round(mine[1][args] * 100, 2)) + "%\n"
            i += 1
        text += "```"
        return await ctx.send(text)

@client.command(pass_context=True, aliases=["triggers", "reaction", "customreaction", "customtrigger"])
async def trigger(ctx, *, args=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)

    if not ctx.message.author.bot == True:
        global triggers
        if not ctx.message.author.guild_permissions.administrator:
            if not args:
                if lang_server == "fr":
                    return await ctx.send(f":x: {ctx.message.author.name}, vous n'avez pas la permission **Administrateur** !")
                elif lang_server == "en":
                    return await ctx.send(f":x: {ctx.message.author.name}, you don't have the permission **Administrator**!")
                elif lang_server == "de":
                    return await ctx.send(f":x: {ctx.message.author.name}, Sie haben nicht die Berechtigung **Verwalter**!")
            else:
                if any(x in args.lower() for x in ["list", "liste"]):
                    if any(x == str(server_id) for x in triggers.keys()) and triggers[str(server_id)]:
                        content = "\n- ".join([x for x in triggers[str(server_id)].keys()])
                        if lang_server == "fr":
                            embed = discord.Embed(title=f"Réactions customisées ({len(triggers[str(server_id)].keys())}) :", description="- " + content, color=0xBFFF00)
                        elif lang_server == "en":
                            embed = discord.Embed(title=f"Customized reactions ({len(triggers[str(server_id)].keys())}) :", description="- " + content, color=0xBFFF00)
                        elif lang_server == "de":
                            embed = discord.Embed(title=f"Kundenspezifische Reaktionen ({len(triggers[str(server_id)].keys())}) :", description="- " + content, color=0xBFFF00)
                        return await ctx.send(embed=embed)
                    else:
                        if lang_server == "fr":
                            embed = discord.Embed(title="Il n'y à aucunes réactions customisées.", color=0xBFFF00)
                        elif lang_server == "en":
                            embed = discord.Embed(title="There are no custom reactions.", color=0xBFFF00)
                        elif lang_server == "de":
                            embed = discord.Embed(title="Es gibt keine benutzerdefinierten Reaktionen.", color=0xBFFF00)
                        return await ctx.send(embed=embed)

        if not args:
            if lang_server == "fr":
                embed = discord.Embed(title=None, description="Veuillez préciser un déclencheur et une réponse : `+trigger [\"déclancheur\" / liste / remove] [\"réponse\" / url]`", color=0xBFFF00)
            elif lang_server == "en":
                embed = discord.Embed(title=None, description="Please specify a trigger and an answer: `+trigger [\"trigger\" / list / remove] [\"answer\" / url]`", color=0xBFFF00)
            elif lang_server == "de":
                embed = discord.Embed(title=None, description="Bitte geben Sie eine Nachricht und eine Antwort an: `+trigger [\"Nachricht\" / list / remove] [\"Antwort\" / url]`", color=0xBFFF00)
            return await ctx.send(embed=embed)

        with open("extra/triggers.json", "r", encoding="utf-8") as file:
            triggers = json.load(file)

        if any(x in args.lower() for x in ["list", "liste", "remove", "delete"]):
            if args.lower() == "list" or args.lower() == "liste":
                if any(x == str(server_id) for x in triggers.keys()) and triggers[str(server_id)]:
                    content = "\n- ".join([x for x in triggers[str(server_id)].keys()])
                    if lang_server == "fr":
                        embed = discord.Embed(title=f"Réactions customisées ({len(triggers[str(server_id)].keys())}) :", description="- " + content, color=0xBFFF00)
                    elif lang_server == "en":
                        embed = discord.Embed(title=f"Customized reactions ({len(triggers[str(server_id)].keys())}) :", description="- " + content, color=0xBFFF00)
                    elif lang_server == "de":
                        embed = discord.Embed(title=f"Kundenspezifische Reaktionen ({len(triggers[str(server_id)].keys())}) :", description="- " + content, color=0xBFFF00)
                    return await ctx.send(embed=embed)
                else:
                    if lang_server == "fr":
                        embed = discord.Embed(title="Il n'y à aucunes réactions customisées.", color=0xBFFF00)
                    elif lang_server == "en":
                        embed = discord.Embed(title="There are no custom reactions.", color=0xBFFF00)
                    elif lang_server == "de":
                        embed = discord.Embed(title="Es gibt keine benutzerdefinierten Reaktionen.", color=0xBFFF00)
                    return await ctx.send(embed=embed)
            elif "remove" in args.lower() or "delete" in args.lower():
                if len(args.split()) == 1:
                    if lang_server == "fr":
                        embed = discord.Embed(title="Veuillez préciser un déclencheur à supprimer : `+trigger [remove / delete] [\"déclancheur\"]`", color=0xBFFF00)
                    elif lang_server == "en":
                        embed = discord.Embed(title="Please specify a trigger to delete: `+trigger [remove / delete] [\"trigger\"]`", color=0xBFFF00)
                    elif lang_server == "de":
                        embed = discord.Embed(title="Bitte geben Sie einen Reaktion zum Löschen an: `+trigger [remove / delete] [\"déclancheur\"]`", color=0xBFFF00)
                    return await ctx.send(embed=embed)
                if '"' in args:
                    remove = re.findall(r'["\'](.*?)["\']', args)[-1].lower()
                else:
                    remove = args.split(" ")[-1].lower()
                if any(x.lower() == remove for x in triggers[str(server_id)].keys()):
                    del triggers[str(server_id)][remove]
                    with open("extra/triggers.json", "w", encoding="utf-8") as file:
                        json.dump(triggers, file, indent=4)
                    if lang_server == "fr":
                        embed = discord.Embed(title="Réaction supprimée :", description=f"**{remove}**", color=0xBFFF00)
                    elif lang_server == "en":
                        embed = discord.Embed(title="Reaction deleted:", description=f"**{remove}**", color=0xBFFF00)
                    elif lang_server == "de":
                        embed = discord.Embed(title="Reaktion gelöscht:", description=f"**{remove}**", color=0xBFFF00)
                else:
                    if lang_server == "fr":
                        embed = discord.Embed(title="Aucune réaction ne correspond à celle choisie.", color=0xBFFF00)
                    elif lang_server == "en":
                        embed = discord.Embed(title="No reaction corresponds to that chosen.", color=0xBFFF00)
                    elif lang_server == "de":
                        embed = discord.Embed(title="Keine Reaktion entspricht der gewählten.", color=0xBFFF00)
                return await ctx.send(embed=embed)
        if not '"' in args and not "'" in args:
            if len(args.split()) == 2:
                trigger = args.split(" ")[0]
                response = args.split(" ")[1]
            elif len(args.split()) < 2:
                if lang_server == "fr":
                    embed = discord.Embed(title="Il n'y à pas assez d'arguments pour créer la réaction, ajoutez-en entre des guillements pour délimiter votre message.", color=0xBFFF00)
                elif lang_server == "en":
                    embed = discord.Embed(title="There are not enough arguments to create the reaction, add some quotes to delimit your message.", color=0xBFFF00)
                elif lang_server == "de":
                    embed = discord.Embed(title="Es gibt nicht genügend Argumente, um die Reaktion auszulösen. Fügen Sie einige in Anführungszeichen ein, um Ihre Nachricht einzugrenzen.", color=0xBFFF00)
                return await ctx.send(embed=embed)
            else:
                if lang_server == "fr":
                    embed = discord.Embed(title="Il y à trop d'arguments pour créer la réaction, mettez des guillements pour délimiter votre message.", color=0xBFFF00)
                elif lang_server == "en":
                    embed = discord.Embed(title="There are too many arguments to create the reaction, add some quotes to delimit your message.", color=0xBFFF00)
                elif lang_server == "de":
                    embed = discord.Embed(title="Es gibt zu viele Argumente, um die Reaktion auszulösen. Setzen Sie Anführungszeichen, um Ihre Nachricht einzugrenzen.", color=0xBFFF00)
                return await ctx.send(embed=embed)
        else:
            if len(re.findall(r'["\'](.*?)["\']', args)) == 2:
                trigger = re.findall(r'["\'](.*?)["\']', args)[0].lower()
                if "http://" in args or "https://" in args:
                    response = args.split(" ")[-1].replace('"', "").replace("'", "")
                else:
                    response = re.findall(r'["\'](.*?)["\']', args)[1]
            elif len(re.findall(r'["\'](.*?)["\']', args)) < 2:
                if lang_server == "fr":
                    embed = discord.Embed(title="Il n'y à pas assez d'arguments pour créer la réaction, ajoutez-en entre des guillements pour délimiter votre message.", color=0xBFFF00)
                elif lang_server == "en":
                    embed = discord.Embed(title="There are not enough arguments to create the reaction, add some quotes to delimit your message.", color=0xBFFF00)
                elif lang_server == "de":
                    embed = discord.Embed(title="Es gibt nicht genügend Argumente, um die Reaktion auszulösen. Fügen Sie einige in Anführungszeichen ein, um Ihre Nachricht einzugrenzen.", color=0xBFFF00)
                return await ctx.send(embed=embed)
            else:
                if lang_server == "fr":
                    embed = discord.Embed(title="Il y à trop d'arguments pour créer la réaction, mettez des guillements pour délimiter votre message.", color=0xBFFF00)
                elif lang_server == "en":
                    embed = discord.Embed(title="There are too many arguments to create the reaction, add some quotes to delimit your message.", color=0xBFFF00)
                elif lang_server == "de":
                    embed = discord.Embed(title="Es gibt zu viele Argumente, um die Reaktion auszulösen. Setzen Sie Anführungszeichen, um Ihre Nachricht einzugrenzen.", color=0xBFFF00)
                return await ctx.send(embed=embed)
        if not any(x == str(server_id) for x in triggers.keys()):
            triggers[str(server_id)] = {trigger: response}
        else:
            if trigger in triggers[str(server_id)].keys():
                if lang_server == "fr":
                    embed = discord.Embed(description="Il y a déjà un déclencheur pour ce message. Supprimer le puis refaites la commande.", color=0xBFFF00)
                elif lang_server == "en":
                    embed = discord.Embed(description="There is already a trigger for this message. Delete it and redo the command.", color=0xBFFF00)
                elif lang_server == "de":
                    embed = discord.Embed(description="Es gibt bereits einen Auslöser für diese Nachricht. Löschen Sie es und wiederholen Sie den Befehl.", color=0xBFFF00)
                return await ctx.send(embed=embed)
        triggers[str(server_id)][trigger] = response
        with open("extra/triggers.json", "w", encoding="utf-8") as file:
            json.dump(triggers, file, indent=4)
        if lang_server == "fr":
            embed = discord.Embed(title="Nouvelle réaction customisée :", color=0xBFFF00)
            embed.add_field(name="Déclencheur", value=trigger, inline=True)
            embed.add_field(name="Réponse", value=response, inline=True)
        elif lang_server == "en":
            embed = discord.Embed(title="New customized reaction:", color=0xBFFF00)
            embed.add_field(name="Trigger", value=trigger, inline=True)
            embed.add_field(name="Reply", value=response, inline=True)
        elif lang_server == "de":
            embed = discord.Embed(title="Neue angepasste Reaktion:", color=0xBFFF00)
            embed.add_field(name="Auslöser", value=trigger, inline=True)
            embed.add_field(name="Antwort", value=response, inline=True)
        return await ctx.send(embed=embed)

#----------------------------- SPECIFIC COMMANDS -----------------------------#

@client.command(pass_context=True, aliases=["roles"])
async def role(ctx, *, args=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        if server_id == 391272643229384705: # Insoumis server ID
            list_roles = ["Payday 2", "Diablo 3", "Gta 5", "The division", "Fortnite", "CS GO", "Farming simulator",
                          "Lol", "Dead by daylight", "Destiny 2", "Quake", "left 4 dead 2", "GRID 2", "Steep"]
            if not args:
                return await ctx.send("Merci de préciser un rôle à vous attribuer : `{}`".format(", ".join(list_roles)))
            if "payday" in args.lower():
                rolename = "Payday 2"
            elif "cs" in args.lower():
                rolename = "CS GO"
            elif "gta" in args.lower():
                rolename = "Gta 5"
            elif "diablo" in args.lower():
                rolename = "Diablo 3"
            elif "destiny" in args.lower():
                rolename = "Destiny 2"
            elif "division" in args.lower():
                rolename = "The division"
            elif "grid" in args.lower():
                rolename = "GRID 2"
            elif "left" in args.lower():
                rolename = "left 4 dead 2"
            elif "dead" in args.lower():
                rolename = "Dead by daylight"
            elif "list" in args.lower():
                return await ctx.send("Voiçi la liste des rôles : `{}`".format(", ".join(list_roles)))
            else:
                for role in list_roles:
                    if args.lower() in role.lower():
                        rolename = role
                        break
                    else:
                        rolename = None
            role = discord.utils.get(ctx.message.guild.roles, name=rolename)
            if role:
                if any(x in role.name for x in list_roles):
                    if role in ctx.message.author.roles:
                        await ctx.message.author.remove_roles(role)
                        result = f"Le rôle {role.name} à bien été enlevé."
                    else:
                        await ctx.message.author.add_roles(role)
                        result = f"Le rôle {role.name} à bien été mis."
                    return await ctx.send(result)
                else:
                    return await ctx.send("Vous n'avez pas le droit de vous attribuer ce rôle.")
            else:
                return await ctx.send("Ce rôle n'existe pas :frowning:")

        elif server_id == 342685946078167040: # Christopher server ID
            list_roles = ["Counter Strike: Global Offensive", "Warframe", "Rainbow Six Siège", "Dofus", "Fortnite",
                          "Minecraft", "Paladins", "PlayerUnknown's Battlegrounds", "Payday 2", "Overkill's The Walking Dead"]
            if not args:
                return await ctx.send("Merci de préciser un rôle à vous attribuer : `{}`".format(", ".join(list_roles)))
            if "payday" in args.lower():
                rolename = "Payday 2"
            elif "cs" in args.lower():
                rolename = "Counter Strike: Global Offensive"
            elif "r6" in args.lower():
                rolename = "Rainbow Six Siège"
            elif "pubg" in args.lower():
                rolename = "PlayerUnknown's Battlegrounds"
            elif "twd" in args.lower():
                rolename = "Overkill's The Walking Dead"
            elif "list" in args.lower():
                return await ctx.send("Voiçi la liste des rôles : `{}`".format(", ".join(list_roles)))
            else:
                for role in list_roles:
                    if args in role.lower():
                        rolename = role
                else:
                    rolename = None
            role = discord.utils.get(ctx.message.guild.roles, name=rolename)
            if role:
                if any(x in role.name for x in list_roles):
                    if role in ctx.message.author.roles:
                        await ctx.message.author.remove_roles(role)
                        result = f"Le rôle {role.name} à bien été enlevé."
                    else:
                        await ctx.message.author.add_roles(role)
                        result = f"Le rôle {role.name} à bien été mis."
                    return await ctx.send(result)
                else:
                    return await ctx.send("Vous n'avez pas le droit de vous attribuer ce rôle.")
            else:
                return await ctx.send("Ce rôle n'existe pas :frowning:")

        elif server_id == 350156033198653441: # TFI server ID
            list_roles = ["Chauffeur en Test", "Ami"]
            if not args:
                return await ctx.send("Merci de préciser un rôle à vous attribuer : `{}`".format(", ".join(list_roles)))
            if "test" in args.lower():
                rolename = "Chauffeur en Test"
            elif "list" in args.lower():
                return await ctx.send("Voiçi la liste des rôles : `{}`".format(", ".join(list_roles)))
            else:
                for role in list_roles:
                    if args in role.lower():
                        rolename = role
                else:
                    rolename = None
            role = discord.utils.get(ctx.message.guild.roles, name=rolename)
            if role:
                if any(x in role.name for x in list_roles):
                    if role in ctx.message.author.roles:
                        await ctx.message.author.remove_roles(role)
                        result = f"Le rôle {role.name} à bien été enlevé."
                    else:
                        await ctx.message.author.add_roles(role)
                        result = f"Le rôle {role.name} à bien été mis."
                    return await ctx.send(result)
                else:
                    return await ctx.send("Vous n'avez pas le droit de vous attribuer ce rôle.")
            else:
                return await ctx.send("Ce rôle n'existe pas :frowning:")

        elif server_id == 509028174013923339: # Solumon server ID
            list_roles = ["Payday 2", "Joueur", "Gmod"]
            if not args:
                return await ctx.send("Merci de préciser un rôle à vous attribuer : `{}`".format(", ".join(list_roles)))
            if "payday" in args.lower():
                rolename = "Payday 2"
            elif "list" in args.lower():
                return await ctx.send("Voiçi la liste des rôles : `{}`".format(", ".join(list_roles)))
            else:
                for role in list_roles:
                    if args in role.lower():
                        rolename = role
                else:
                    rolename = None
            role = discord.utils.get(ctx.message.guild.roles, name=rolename)
            if role:
                if any(x in role.name for x in list_roles):
                    if role in ctx.message.author.roles:
                        await ctx.message.author.remove_roles(role)
                        result = f"Le rôle {role.name} à bien été enlevé."
                    else:
                        await ctx.message.author.add_roles(role)
                        result = f"Le rôle {role.name} à bien été mis."
                    return await ctx.send(result)
                else:
                    return await ctx.send("Vous n'avez pas le droit de vous attribuer ce rôle.")
            else:
                return await ctx.send("Ce rôle n'existe pas :frowning:")

        elif server_id == 319533759894388736: # Exos_Team server ID
            if ctx.message.author.id == 246943045105221633: # Quentium user ID
                role = discord.utils.get(ctx.message.guild.roles, name=args)
                if role in ctx.message.author.roles:
                    return await ctx.message.author.remove_roles(role)
                else:
                    return await ctx.message.author.add_roles(role)

@client.command(pass_context=True, no_pm=True, aliases=["abs"])
async def absent(ctx, *, args=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        if server_id == 371687157817016331: # France Les Cités server ID
            if ctx.message.channel.id == 552484372251410437: # France Les Cités channel ID
                if not ctx.message.guild.me.guild_permissions.manage_roles:
                    return await ctx.send(":x: Il manque la permissions **Gérer les rôles** au bot.")
                role = discord.utils.get(ctx.message.guild.roles, name="Absent")
                if not role in ctx.message.author.roles:
                    if args is None:
                        await ctx.message.delete()
                        return await ctx.message.author.send("Pour vous mettre le statut d'absent, il faut que vous spécifiez une raison et une durée d'absence ! (ex : `-absent Vacances 7 jours`)")
                    await ctx.message.author.add_roles(role)
                    await ctx.send(f"**{ctx.message.author.name}** est désormais absent pour la raison : ***{args}***")
                    await ctx.message.author.send("Vous avez bien rejoint le statut d'absent !")
                    return await ctx.message.delete()
                else:
                    await ctx.message.author.remove_roles(role)
                    await ctx.message.author.send("Vous avez bien quitté le statut d'absent !")
                    await ctx.send(f"**{ctx.message.author.name}** est de retour parmis nous !")
                    return await ctx.message.delete()

@client.command(pass_context=True, aliases=["votes", "blasonsmax", "voteresults"])
async def vote(ctx, *, args=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        if server_id == 371687157817016331: # France Les Cités server ID
            if not args:
                await ctx.message.delete()
                return await ctx.message.author.send("Merci de bien vouloir préciser un blason par son numéro.")
            try:
                with open("blasons.txt", "r", encoding="utf-8") as file:
                    lines = file.readlines()
            except:
                open("blasons.txt", "a+", encoding="utf-8").close()
                lines = ""
            authorised = [348509601936834561, 358214022115360771, 246943045105221633] # Cityzoo / Scant / Quentium user ID
            if any(x == ctx.message.author.id for x in authorised):
                if "blasonsmax" in ctx.message.content:
                    lines[0] = args + "\n"
                    with open("blasons.txt", "w", encoding="utf-8") as file:
                        file.writelines(lines)
                    await ctx.message.delete()
                    return await ctx.message.author.send(f"Le nombre de blasons max à été mis à **{args}**")
                elif "voteresults" in ctx.message.content:
                    results = []
                    with open("blasons.txt", "r", encoding="utf-8") as file:
                        for line in file:
                            try:
                                results.append(line.split(" --> ")[1])
                            except:
                                pass
                    return await ctx.message.author.send("Resultats : \n" + "-".join(results))

            if not args.isdigit():
                await ctx.message.delete()
                return await ctx.message.author.send("Cet argument ne correspond pas au numéros de la liste des blasons.")
            else:
                if args > lines[0]:
                    await ctx.message.delete()
                    return await ctx.message.author.send("Ce nombre dépasse le nombre de blasons dans la liste.")
            with open("blasons.txt", "r", encoding="utf-8") as file:
                for line in file:
                    if str(ctx.message.author.id) in line:
                        await ctx.message.delete()
                        return await ctx.message.author.send("Vous avez déjà voté pour un blason, il est impossible de changer son vote.")
            with open("blasons.txt", "a", encoding="utf-8") as file:
                file.write(f"{ctx.message.author.id} --> {args}\n")
                await ctx.message.delete()
                return await ctx.message.author.send(f"Vous avez bien voté pour le blason **{args}**.")

@client.command(pass_context=True, aliases=["cookies", "cooki"])
async def cookie(ctx):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        if server_id == 199189022894063627: # TheSweMaster server ID
            not_cookie = ["MrCookie"]
            cookies = [x for x in client.emojis if "cookie" in str(x.name).lower() and not any(y == str(x.name) for y in not_cookie)]
            msg_cookies = "".join([str(x) for x in cookies])
            return await ctx.send("Here are your cookies ***" + str(ctx.message.author.name) + "*** :cookie:" + msg_cookies)

#----------------------------- ADMIN COMMANDS -----------------------------#

@client.command(pass_context=True, no_pm=True, aliases=["clearmsg"])
async def clear(ctx, *args):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        if not ctx.message.author.guild_permissions.manage_messages:
            if lang_server == "fr":
                return await ctx.send(f":x: {ctx.message.author.name}, vous n'avez pas la permission **Gérer les messages** !")
            elif lang_server == "en":
                return await ctx.send(f":x: {ctx.message.author.name}, you don't have the permission **Manage messages**!")
            elif lang_server == "de":
                return await ctx.send(f":x: {ctx.message.author.name}, Sie haben nicht die Berechtigung **Nachrichten verwalten**!")
        if not ctx.message.guild.me.guild_permissions.manage_messages:
            if lang_server == "fr":
                return await ctx.send(":x: Il manque la permissions **Gérer les messages** au bot.")
            elif lang_server == "en":
                return await ctx.send(":x: The bot is missing **Manage messages** permissions.")
            elif lang_server == "de":
                return await ctx.send(":x: Dem Bot fehlen **Nachrichten verwalten** Berechtigungen.")
        if not args:
            if lang_server == "fr":
                return await ctx.send("Merci de préciser un nombre.")
            elif lang_server == "en":
                return await ctx.send("Please specify a number.")
            elif lang_server == "de":
                return await ctx.send("Bitte geben Sie eine Nummer an.")
        else:
            if args[0].isdecimal():
                number = int(args[0])
                if number < 99 and number >= 1:
                    limit = number + 1
                    await ctx.message.channel.purge(limit=limit)
                else:
                    if lang_server == "fr":
                        return await ctx.send("Le nombre doit être compris entre 1 et 99 pour limiter les erreurs.")
                    elif lang_server == "en":
                        return await ctx.send("The number must be between 1 and 99 to prevent errors.")
                    elif lang_server == "de":
                        return await ctx.send("Die Nummer muss zwischen 1 und 99 liegen um Fehler zu begrenzen.")
            else:
                if lang_server == "fr":
                    return await ctx.send("Nombre inconnu, merci de rentrer un nombre correct.")
                elif lang_server == "en":
                    return await ctx.send("Unknown number, please enter a valid number.")
                elif lang_server == "de":
                    return await ctx.send("Unbekannte Nummer, bitte geben Sie eine korrekte Nummer ein.")

@client.command(pass_context=True, no_pm=True)
async def kick(ctx, *, member : discord.Member=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        if not ctx.message.author.guild_permissions.kick_members:
            if lang_server == "fr":
                return await ctx.send(f":x: {ctx.message.author.name}, vous n'avez pas la permission **Expulser des membres** !")
            elif lang_server == "en":
                return await ctx.send(f":x: {ctx.message.author.name}, you don't have the permission **Kick members**!")
            elif lang_server == "de":
                return await ctx.send(f":x: {ctx.message.author.name}, Sie haben nicht die Berechtigung **Kick-Mitglieder**!")
        if not ctx.message.guild.me.guild_permissions.kick_members:
            if lang_server == "fr":
                return await ctx.send(":x: Il manque la permissions **Expulser des membres** au bot.")
            elif lang_server == "en":
                return await ctx.send(":x: The bot is missing **Kick members** permissions.")
            elif lang_server == "de":
                return await ctx.send(":x: Dem Bot fehlen **Kick-Mitglieder** Berechtigungen.")
        if not member:
            if lang_server == "fr":
                return await ctx.send(f":x: {ctx.message.author.name}, mentionnez la personne à expulser !")
            elif lang_server == "en":
                return await ctx.send(f":x: {ctx.message.author.name}, mention the member to kick!")
            elif lang_server == "de":
                return await ctx.send(f":x: {ctx.message.author.name}, erwähnen Sie das ausgestoßende Mitglied!")
        await member.kick()
        if lang_server == "fr":
            embed = discord.Embed(description=f"**{member.name}** à été kick !", color=0xFF0000)
        elif lang_server == "en":
            embed = discord.Embed(description=f"**{member.name}** has been kicked!", color=0xFF0000)
        elif lang_server == "de":
            embed = discord.Embed(description=f"**{member.name}** wurde rausgeschmissen!", color=0xFF0000)
        return await ctx.send(embed=embed)

@client.command(pass_context=True, no_pm=True)
async def ban(ctx, *, member : discord.Member=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        if not ctx.message.author.guild_permissions.ban_members:
            if lang_server == "fr":
                return await ctx.send(f":x: {ctx.message.author.name}, vous n'avez pas la permission **Bannir des membres** !")
            elif lang_server == "en":
                return await ctx.send(f":x: {ctx.message.author.name}, you don't have the permission **Ban members**!")
            elif lang_server == "de":
                return await ctx.send(f":x: {ctx.message.author.name}, Sie haben nicht die Berechtigung **Verbot von Mitgliedern**!")
        if not ctx.message.guild.me.guild_permissions.ban_members:
            if lang_server == "fr":
                return await ctx.send(":x: Il manque la permissions **Bannir des membres** au bot.")
            elif lang_server == "en":
                return await ctx.send(":x: The bot is missing **Ban members** permissions.")
            elif lang_server == "de":
                return await ctx.send(":x: Dem Bot fehlen **Verbot von Mitgliedern** Berechtigungen.")
        if not member:
            if lang_server == "fr":
                return await ctx.send(f":x: {ctx.message.author.name}, mentionnez la personne à bannir !")
            elif lang_server == "en":
                return await ctx.send(f":x: {ctx.message.author.name}, mention the member to ban!")
            elif lang_server == "de":
                return await ctx.send(f":x: {ctx.message.author.name}, erwähnen Sie das zu verbannende Mitglied!")
        await member.ban()
        if lang_server == "fr":
            embed = discord.Embed(description=f"**{member.name}** à été bannis !", color=0xFF0000)
        elif lang_server == "en":
            embed = discord.Embed(description=f"**{member.name}** has been banned!", color=0xFF0000)
        elif lang_server == "de":
            embed = discord.Embed(description=f"**{member.name}** wurde verboten!", color=0xFF0000)
        return await ctx.send(embed=embed)

@client.command(pass_context=True, no_pm=True)
async def autorole(ctx, *, args=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        if not ctx.message.author.guild_permissions.manage_roles:
            if lang_server == "fr":
                return await ctx.send(f":x: {ctx.message.author.name}, vous n'avez pas la permission **Gérer les rôles** !")
            elif lang_server == "en":
                return await ctx.send(f":x: {ctx.message.author.name}, you don't have the permission **Manage roles**!")
            elif lang_server == "de":
                return await ctx.send(f":x: {ctx.message.author.name}, Sie haben nicht die Berechtigung **Rollen verwalten**!")
        if not ctx.message.guild.me.guild_permissions.manage_roles:
            if lang_server == "fr":
                return await ctx.send(":x: Il manque la permissions **Gérer les rôles** au bot.")
            elif lang_server == "en":
                return await ctx.send(":x: The bot is missing **Manage roles** permissions.")
            elif lang_server == "de":
                return await ctx.send(":x: Dem Bot fehlen **Rollen verwalten** Berechtigungen.")
        if not args:
            if lang_server == "fr":
                return await ctx.send("Merci de préciser un argument. `+autorole <role>/show/remove`")
            elif lang_server == "en":
                return await ctx.send("Please specify an argument. `+autorole <role>/show/remove`")
            elif lang_server == "de":
                return await ctx.send("Bitte geben Sie eine argument. `+autorole <role>/show/remove`")
        else:
            rolename = args.lower()
            if rolename == "remove" or rolename == "show":
                role = rolename
            else:
                for role in ctx.message.guild.roles:
                    if "<@" in rolename:
                        role = discord.utils.get(ctx.message.guild.roles, id=int(rolename[3:-1]))
                        break
                    if rolename == role.name.lower():
                        role = discord.utils.get(ctx.message.guild.roles, name=role.name)
                        break
                else:
                    role = None
            if role == None:
                if lang_server == "fr":
                    await ctx.send("Merci d'entrer un rôle valide existant sur ce serveur !")
                elif lang_server == "en":
                    await ctx.send("Please enter a valid role existing on this server!")
                elif lang_server == "de":
                    await ctx.send("Bitte geben Sie eine gültige Rolle ein, die auf diesem Server existiert!")
            else:
                try:
                    with open("extra/data.txt", encoding="utf-8") as file:
                        for line in file:
                            if str(server_id) in line:
                                clean_line = line.rstrip().split(sep, 999)
                                if role == "remove":
                                    clean_line[4] = "@everyone"
                                    if lang_server == "fr":
                                        await ctx.send("L'autorole à été correctement supprimé.")
                                    elif lang_server == "en":
                                        await ctx.send("Autorole has been correctly deleted.")
                                    elif lang_server == "de":
                                        await ctx.send("Die Autorole wurde korrekt gelöscht.")
                                elif role == "show":
                                    role_file = clean_line[4]
                                    if role_file == "@everyone":
                                        if lang_server == "fr":
                                            return await ctx.send("L'autorole n'a pas été défini !")
                                        elif lang_server == "en":
                                            return await ctx.send("Autorole is not defined!")
                                        elif lang_server == "de":
                                            return await ctx.send("Die Autorole wurde nicht definiert!")
                                    else:
                                        role = discord.utils.get(ctx.message.guild.roles, id=int(role_file))
                                        if not role == None:
                                            if lang_server == "fr":
                                                return await ctx.send(f"L'autorole est défini sur `{role.name}`.")
                                            elif lang_server == "en":
                                                return await ctx.send(f"Autorole is set to `{role.name}`.")
                                            elif lang_server == "de":
                                                return await ctx.send(f"Die Autorole ist auf `{role.name}` gesetzt.")
                                #elif role == "multiple":
                                    #clean_line[4] = "272369384520024065/450728369848582167"
                                    #list_roles = []
                                    #for roles in clean_line[4].split("/"):
                                        #role = discord.utils.get(ctx.message.guild.roles, id=int(roles))
                                        #if not role == None:
                                            #list_roles.append(role.name)
                                    #await ctx.send("L'autorole à été définis sur `%s` avec succès." % ", ".join(list_roles))"""
                                else:
                                    clean_line[4] = str(role.id)
                                    if lang_server == "fr":
                                        await ctx.send(f"L'autorole à été définis sur `{role.name}` avec succès.")
                                    elif lang_server == "en":
                                        await ctx.send(f"Successfully set autorole to role `{role.name}`.")
                                    elif lang_server == "de":
                                        await ctx.send(f"Die Autorolle wurde erfolgreich auf `{role.name}` gesetzt.")
                                with open("extra/data.txt", "r", encoding="utf-8") as file:
                                    filedata = file.read()
                                filedata = filedata.replace(str(line), str(sep.join(clean_line) + "\n"))
                                with open("extra/data.txt", "w", encoding="utf-8") as file:
                                    file.write(filedata)
                except:
                    if lang_server == "fr":
                        return await ctx.send("Un problème est survenu lors de la sauvegarde de l'autorole !")
                    elif lang_server == "en":
                        return await ctx.send("Something went wrong while saving autorole!")
                    elif lang_server == "de":
                        return await ctx.send("Beim Sichern des Autorollers ist ein Problem aufgetreten!")

@client.command(pass_context=True, no_pm=True, aliases=["langs", "language"])
async def lang(ctx, *, arg):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        if not ctx.message.author.guild_permissions.administrator:
            if lang_server == "fr":
                return await ctx.send(f":x: {ctx.message.author.name}, vous n'avez pas la permission **Administrateur** !")
            elif lang_server == "en":
                return await ctx.send(f":x: {ctx.message.author.name}, you don't have the permission **Administrator**!")
            elif lang_server == "de":
                return await ctx.send(f":x: {ctx.message.author.name}, Sie haben nicht die Berechtigung **Verwalter**!")
        if arg == "":
            if lang_server == "fr":
                return await ctx.send("Merci de préciser la langue à changer. `(fr / en / de)`")
            elif lang_server == "en":
                return await ctx.send("Please specify the language to change. `(fr / en / de)`")
            elif lang_server == "de":
                return await ctx.send("Bitte geben Sie die gewünschte Sprache ein. `(fr / en / de)`")
        else:
            if arg == "fr" or arg == "en" or arg == "de":
                with open("extra/data.txt", encoding="utf-8") as file:
                    for line in file:
                        if str(server_id) in line:
                            clean_line = line.rstrip().split(sep, 999)
                            lang_server = clean_line[2]
                            if lang_server == arg:
                                if arg == "fr":
                                    await ctx.send("La langue du bot était déjà définie sur **Français**.")
                                elif arg == "en":
                                    await ctx.send("Language of the bot is already set to **English**.")
                                elif arg == "de":
                                    await ctx.send("Die Sprache des Bots ist bereits auf **Deutsch** eingestellt.")
                                break
                            else:
                                clean_line[2] = str(arg)
                                with open("extra/data.txt", "r", encoding="utf-8") as file:
                                    filedata = file.read()
                                filedata = filedata.replace(str(line), str(sep.join(clean_line) + "\n"))
                                with open("extra/data.txt", "w", encoding="utf-8") as file:
                                    file.write(filedata)
                                if arg == "fr":
                                    return await ctx.send("La langue du bot a été changée en **Français**.")
                                elif arg == "en":
                                    return await ctx.send("Language of bot has been changed to **English**.")
                                elif arg == "de":
                                    return await ctx.send("Die Sprache des Bots wurde auf **Deutsch** geändert.")
                                break
            else:
                if lang_server == "fr":
                    return await ctx.send("Cette langue n'existe pas, merci de rentrer une language correcte : `(fr / en / de)`.")
                elif lang_server == "en":
                    return await ctx.send("This language doesn't exist, please enter a correct language : `(fr / en / de)`.")
                elif lang_server == "de":
                    return await ctx.send("Diese Sprache existiert nicht, bitte geben Sie eine korrekte Sprache ein : `(fr / en / de)`.")

#----------------------------- FEEDBACK COMMANDS -----------------------------#

@client.command(pass_context=True, aliases=["bug", "ideas"])
@commands.cooldown(2, 30, commands.BucketType.channel)
async def idea(ctx, *args):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        cmd_recieved = ctx.message.content.replace("+", "").split()[0]
        if not args:
            if cmd_recieved == "idea":
                if lang_server == "fr":
                    return await ctx.send("Merci de préciser une idée.")
                elif lang_server == "en":
                    return await ctx.send("Please specify an idea.")
                elif lang_server == "de":
                    return await ctx.send("Bitte geben Sie eine Idee an.")
            elif cmd_recieved == "bug":
                if lang_server == "fr":
                    return await ctx.send("Merci de préciser un bug.")
                elif lang_server == "en":
                    return await ctx.send("Please specify a bug.")
                elif lang_server == "de":
                    return await ctx.send("Bitte geben Sie eine Bug an.")
        idea_infos = str(ctx.message.author) + sep + cmd_recieved + sep
        idea = " ".join(list(args))
        with open("feedback.txt", "a", encoding="utf-8") as file:
            file.write(idea_infos + args + "\n")
        if lang_server == "fr":
            return await ctx.send("Merci de contribuer à l'amélioration du bot !")
        elif lang_server == "en":
            return await ctx.send("Thank you for contributing to improve the bot!")
        elif lang_server == "de":
            return await ctx.send("Danke, dass Sie zur Verbesserung des Bot beigetragen haben!")

@client.command(pass_context=True, aliases=["logs", "showlog", "changelog", "whatsnew", "whatnew"])
async def showlogs(ctx):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if not ctx.message.author.bot == True:
        if lang_server == "fr":
            embed = discord.Embed(title="Logs de mise à jour du bot :", url="https://quentium.fr/discord/", color=0xFFFF00)
        elif lang_server == "en":
            embed = discord.Embed(title="Changelog of the bot:", url="https://quentium.fr/en/discord/", color=0xFFFF00)
        elif lang_server == "de":
            embed = discord.Embed(title="Bot Update-Protokolle:", url="https://quentium.fr/de/discord/", color=0xFFFF00)
        counter = 1
        with open("extra/logs.txt", "r", encoding="utf-8") as file:
            for line in file:
                line_time = line.split(sep, 999)[0]
                line_content = line.split(sep, 999)[1]
                embed.add_field(name="#" + str(counter) + " / " + line_time, value=line_content.replace("..",    ".\n"), inline=True)
                counter += 1
        if lang_server == "fr":
            embed.set_footer(text="Les logs sont publiées dès qu'une nouvelle mise à jour importante du bot a lieu.", icon_url="https://quentium.fr/+img/logoBot.png")
        elif lang_server == "en":
            embed.set_footer(text="Logs are shared when the bot gets a new important update.", icon_url="https://quentium.fr/+img/logoBot.png")
        elif lang_server == "de":
            embed.set_footer(text="Die Protokolle werden veröffentlicht, sobald eine wichtig neue Update der Bots stattfindet.", icon_url="https://quentium.fr/+img/logoBot.png")
        return await ctx.send(embed=embed)

#----------------------------- QUENTIUM COMMANDS -----------------------------#

@client.command(name="exec", pass_context=True, hidden=True, aliases=["execute"])
async def _exec(ctx, *, args=None):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

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
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    if ctx.message.author.id == 246943045105221633: # Quentium ID
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
async def data4tte(ctx, *args):
    if isinstance(ctx.channel, discord.TextChannel):
        global lang_server, commands_server, autorole_server, server_id, server_name
        server_id = ctx.message.guild.id
        server_name = ctx.message.guild.name
        await async_data(server_id, server_name)
    else:
        lang_server = "fr"

    authorised = [246943045105221633, 224928390694567936, 272412092248752137]
    if any(x == ctx.message.author.id for x in authorised): # Quentium / vectokse / Jaguar AF user ID
        if args:
            if args[0].isdecimal():
                number = args[0]
        else:
            number = 130

        temp = await ctx.send("Sending requests, it may take long")
        await async_command("python3 data4tte.py " + str(number), ctx.message)
        await asyncio.sleep(5)
        await ctx.message.delete()
        return await temp.delete()
    else:
        return await ctx.message.delete()

client.run(config["PUBLIC"]["token"])
