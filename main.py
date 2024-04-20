import sqlite3
import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
from pyjokes import get_joke as gjoke
from load import json

with open('token.json') as tj:
    tn=load(tj)
client = commands.Bot(command_prefix="+", intents = discord.Intents.all())
databasev=1.1
conn = sqlite3.connect(f'vouch_db_{databasev}.sql')
cursor = conn.cursor()

# Create a table to store vouch data if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS vouches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        commenter_id INTEGER,
        comment TEXT
    )
''')
conn.commit()
@client.event
async def on_ready():
    print(f"Vouch Bot nammed {client.user.name} on!")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name =f"{client.command_prefix}help"))



@client.command(aliases=['rep'])
async def vouch(ctx:commands.Context, user: discord.Member, *, comment=""):
    created_at_naive = user.created_at.replace(tzinfo=None)
    # Calculate the age of the user account
    age = datetime.utcnow() - created_at_naive
    if age < timedelta(days=14) and user.id not in [1223837675841261669,1106799324450521161,893488595992739880,990886544208433163]:
        await ctx.message.add_reaction("❌")
        aaa=discord.Embed(
            title="Vouch Failed",
            description=f"Vouch Failed Your account is too Young"
        )
        await ctx.send(embed=aaa)
        return
    if ctx.author.id == user.id:
        await ctx.message.add_reaction("❌")
        raaa=discord.Embed(
            title="Vouch Failed",
            description=f"Vouch Failed, You cant vouch urself!"
        )
        await ctx.send(embed=raaa)
        return
    if ctx.channel.id != 1227225137489645641:
        await ctx.message.add_reaction("❌")
        raaa=discord.Embed(
            title="Vouch Failed",
            description=f"Vouch Failed, Vouch in correct channel <#1227225137489645641>"
        )
        await ctx.send(embed=raaa)
        return
    if comment == "":
        await ctx.message.add_reaction("❌")
        aaa=discord.Embed(
            title="Vouch Failed",
            description=f"Vouch Failed Comment can't be empty!"
        )
        await ctx.send(embed=aaa)
        return
    cursor.execute('''
        INSERT INTO vouches (user_id, commenter_id, comment)
        VALUES (?, ?, ?)
    ''', (user.id, ctx.author.id, comment))
    conn.commit()
    await ctx.message.add_reaction("✅")
    aaa=await ctx.send(f"Vouch added for {user.display_name}: {comment}")
    await asyncio.sleep(5)
    await aaa.delete()
@client.command()
async def avouch(ctx:commands.Context,user1:discord.Member ,user: discord.Member, *, comment=""):
    if ctx.author.id not in [893488595992739880]:
        return
    if comment == "":
        await ctx.message.add_reaction("❌")
        aaa=discord.Embed(
            title="Vouch Failed",
            description=f"Vouch Failed Comment can't be empty!"
        )
        await ctx.send(embed=aaa)
        return
    cursor.execute('''
        INSERT INTO vouches (user_id, commenter_id, comment)
        VALUES (?, ?, ?)
    ''', (user.id, user1.id, comment))
    conn.commit()
    aaa=await ctx.send(f"Vouch added for {user.display_name}: {comment}")
    await asyncio.sleep(5)
    await aaa.delete()
@client.command()
async def joke(ctx):
    await ctx.send(gjoke())
@client.command()
async def say(ctx,*,mesg):
    if ctx.author.id ==1223837675841261669:
        await ctx.message.delete()
        await ctx.channel.send(mesg)
@client.command()
async def rvouch(ctx, user: discord.Member,*,comment:str):
    # Check if the command invoker is you
    if ctx.author.id not in [1223837675841261669,893488595992739880]:
        await ctx.send("You are not authorized to use this command.")
        return
    
    # Delete the vouch data from the database for the specified user
    cursor.execute('''
    SELECT id
    FROM vouches
    WHERE comment = ?
    ''', (comment,))
    vouch_ids = cursor.fetchall()  # Fetch all records instead of just one

    if not vouch_ids:
        await ctx.send("Vouch comment not found.")
        return

    # Delete the vouch data from the database
    for vouch_id in vouch_ids:
        cursor.execute('''
            DELETE FROM vouches
            WHERE id = ?
        ''', (vouch_id[0],))
    
    await ctx.send(f"Vouch comment for {user.display_name} has been deleted.")
@client.command(aliases=['reps'])
async def vouches(ctx:commands.Context,user:discord.User="self"):
    if user == "self":
        user=ctx.author
    cursor.execute('''
        SELECT commenter_id, comment
        FROM vouches
        WHERE user_id = ?
    ''', (user.id,))
    vouches = cursor.fetchall()
    
    if not vouches:
        await ctx.send(f"No vouches found for {user.display_name}")
        return
    shit=[f"{client.get_user(commenter_id)}: {comment}" for commenter_id, comment in vouches]
    vouch_list = '\n'.join(shit)
    await ctx.send(f"Vouches for {user.display_name}:\n{vouch_list}")


client.run(tn[0])
