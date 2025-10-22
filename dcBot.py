import os
import discord
import random
from dotenv import load_dotenv

load_dotenv()
Token = os.getenv("DISCORD_TOKEN")
Guild = os.getenv("DISCORD_GUILD")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
random_number_array = []
u_guess_array = []
random_cat_picture_array = [
    "",
    "https://i1.sndcdn.com/avatars-000600452151-38sfei-t240x240.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTOFQpA5TsoOWUxPdpMPyx09N5gQ6Pj_VK6pvjw8oPbow&s",
    "https://www.travelandleisure.com/thmb/EX2GMaNj47Cd0nCTiKMW205mCWQ=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/kitten-litter-cat-names-CATNAMES0521-338c6363384c46af850c71f57c66559d.jpg",
]
trys = 0
player_won = False
active = False
previous_cat_picture_url = ""


@client.event
async def on_ready():
    print(f"hello {client.user} you are ready")
    game = discord.Game("waiting to drop cute cats")
    await client.change_presence(activity=game)


@client.event
async def on_message(message):

    if message.author == client.user and message.channel.id == 1059532526902857788:
        return

    if message.channel.id == 1059532526902857788:
        global random_number_array
        global u_guess_array
        global trys
        global random_number
        global u_guess
        global channel
        global player_won
        global random_cat_picture_array
        global cat_picture
        global active

        random_number = random.randint(1, 4)
        random_index = random.randint(1, 3)
        u_guess = message.content
        präfix = "!cat"
        channel = message.channel
        u_name = message.author.name
        cat_picture = random_cat_picture_array[random_index]

        print(str(random_index) + " is random index")

        if message.content.startswith(präfix):
            active = True
            player_won = False
            await user_info(u_name)
            return active

        if trys <= 10 and player_won != True and "!" not in u_guess:

            print(f"proccess active? {active}\n")
            await check_guess(u_guess, message, präfix)
            trys += 1
            random_number_array.append(random_number)
            u_guess_array.append(u_guess)
            print(f"{trys}: trys\n")

            print(f"[random number {str(random_number)}]"),
            print(f"{message.author.mention} won ? {player_won}"),
            print(f"[user number {str(u_guess)}]\n")
        else:
            active = False
            random_number_array = []
            u_guess_array = []
            trys = 0
            return active


async def check_duplicate(previous_cat_picture_url, message):
    if cat_picture != previous_cat_picture_url:
        await channel.send(
            f"{message.author.mention} you won random number was {random_number} @here i gift a cat \n {cat_picture} \n again?"
        )
        previous_cat_picture_url = cat_picture
        return
    else:
        await channel.send(f"[{cat_picture}] duplicate detected")

    await channel.send(f"[random_number] -->{random_number_array} \n")
    await channel.send(f"[u_guess]          -->{u_guess_array} \n")


async def user_info(u_name):
    await channel.send(f"{u_name} guess a number from 1 to 10")
    await channel.send("good luck ! :blush:")
    return True


async def check_guess(u_guess, message, präfix):
    global player_won
    global cat_picture
    global previous_cat_picture_url

    if str(u_guess) == str(random_number) and präfix:
        player_won = True
        await check_duplicate(previous_cat_picture_url, message)

    elif str(u_guess) != str(random_number):

        player_won = False

        await channel.send(f"{message.author.mention} you lost\n")
        return True

    else:
        return


client.run(Token)
