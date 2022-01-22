import asyncio
import time
import discord
import os
import random
import pickle
from discord.message import Message
from dotenv import load_dotenv


load_dotenv()
token = os.getenv("TOKEN")
conf = "config.pkl"
messages = 0
joined = 0
temp = open(conf, "rb")
config = pickle.load(temp)
print(config)
greet = config["greet"]
activation = config["COMMANDWORD"]
temp.close()

print("Taking bot online")

client = discord.Client()

embed = discord.Embed(
    title="Command's Help",
    discription="Following are the set of commands available with the BOT",
)
embed.add_field(
    name=f"Activation Character: {activation}",
    value="This is character that must precedence before a command ",
    inline=False,
)
embed.add_field(
    name=f"{activation}greet", value="Greet User with customized messsage", inline=False
)
embed.add_field(
    name=f"{activation}user", value="Get member count on the server", inline=False
)
embed.add_field(
    name=f"{activation}change", value="Change Command Word of the BOT", inline=False
)
embed.add_field(name=f"{activation}helo", value="Bring up this menu", inline=False)


def changeactivation(newActivation):
    temp = open(conf, "rb")
    config = pickle.load(temp)
    config["COMMANDWORD"] = newActivation
    temp.close()
    temp1 = open(conf, "wb")
    pickle.dump(config, temp1)
    global activation
    activation = newActivation
    temp1.close()


async def updatestats():
    await client.wait_until_ready()
    global messages, joined
    with open("stats.txt", "a") as f:
        f.write(f"\n\nBot stated on {int(time.time())}\n")

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(
                    f"Time: {time.time()} , Messages:{messages}, Members:{joined}\n"
                )
                messages = 0
                joined = 0
                await asyncio.sleep(10)

        except Exception as e:
            print(e)

    with open("stats.txt", "a") as f:
        f.write(f"Bot closed on {int(time.time())}\n")


@client.event
async def on_ready():
    print("Logged on Sucessfully")


@client.event
async def on_member_join(member):
    global joined
    joined += 1
    await client.send_message(f"Welcome to {member.guild} , {member.mention}")


@client.event
async def on_message(message):
    global messages
    messages += 1
    if message.content.find(activation + "help") == 0:
        await message.channel.send(embed=embed)
    elif message.content.find(activation + "greet") == 0:
        await message.channel.send(
            f"{random.choice(greet)}, {(str(message.author))[:-5]}"
        )
    elif message.content.find(activation + "users") == 0:
        await message.channel.send(
            f"Number of members on {message.guild} are {message.guild.member_count}"
        )
    elif message.content.find(activation + "change") == 0:
        if len(message.content) <= 8:
            {
                await message.channel.send(
                    f"Error Processing your request \n usage : {activation}change NewActivationSymbol"
                )
            }
        else:
            newActivation = message.content[8:]
            if len(newActivation) <= 2:
                changeactivation(newActivation)
                await message.channel.send(
                    f"Command word has been changed to {newActivation}"
                )
            else:
                await message.channel.send("Command word greater than 2 is not allowed")
    elif message.content.find(activation) == 0:
        await message.channel.send(
            f"UnKnown Command Please Use {activation}help for list of valid command"
        )
        await message.channel.send(config)
    else:
        print("Message from {0.author}: {0.content}".format(message))


client.loop.create_task(updatestats())
client.run(token)
