import discord
from discord.ext import commands
from vps_manager import deploy_ipv4, list_vps, list_all, delete_vps
import json

with open("config.json") as f:
    config = json.load(f)

TOKEN = config["token"]
admins = config["admins"]

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

def is_admin(ctx):
    return str(ctx.author.id) in admins

@bot.event
async def on_ready():
    print(f"Bot ready: {bot.user}")

@bot.command()
async def deployipv4(ctx, userid: str):
    if str(ctx.author.id) != userid and not is_admin(ctx):
        return await ctx.send("Unauthorized.")
    vps = deploy_ipv4(userid)
    await ctx.author.send(
        f"**Your VPS is ready:**\n"
        f"`ssh root@{vps['ip']} -p {vps['port']}`\n"
        f"Password: `{vps['password']}`"
    )

@bot.command()
async def list(ctx):
    vps_list = list_vps(str(ctx.author.id))
    if not vps_list:
        await ctx.send("You have no VPS.")
        return
    for vps in vps_list:
        await ctx.send(f"IP: {vps['ip']} | Port: {vps['port']} | User: root | Pass: {vps['password']}")

@bot.command()
@commands.check(is_admin)
async def nodeadmin(ctx):
    all_data = list_all()
    for user, vps_list in all_data.items():
        await ctx.send(f"{user}: {len(vps_list)} VPS")

@bot.command()
@commands.check(is_admin)
async def nodes(ctx):
    all_data = list_all()
    for user, vps_list in all_data.items():
        for vps in vps_list:
            await ctx.send(f"{user}: ssh root@{vps['ip']} -p {vps['port']} | pass: {vps['password']}")

@bot.command()
@commands.check(is_admin)
async def delvps(ctx, userid: str):
    if delete_vps(userid):
        await ctx.send(f"Deleted all VPS for user: {userid}")
    else:
        await ctx.send("No VPS found for that user.")

@bot.command()
async def dropipv4(ctx):
    all_data = list_all()
    lines = []
    for user, vps_list in all_data.items():
        for vps in vps_list:
            lines.append(f"{user}: ssh root@{vps['ip']} -p {vps['port']} | pass: {vps['password']}")
    await ctx.author.send("\n".join(lines) or "No VPS found.")

@bot.command()
@commands.check(is_admin)
async def botadmin(ctx):
    await ctx.send(f"Current admins: {', '.join(admins)}")

@bot.command()
@commands.check(is_admin)
async def botadmin_add(ctx, userid: str):
    if userid not in admins:
        admins.append(userid)
        with open("config.json", "w") as f:
            json.dump({"token": TOKEN, "admins": admins}, f)
        await ctx.send(f"Added bot admin: {userid}")
    else:
        await ctx.send("User is already an admin.")

@bot.command()
async def botinfo(ctx):
    await ctx.send("Bot: LP VPS Deployer | Version 1.0 | Dev: lpnodes")

bot.run(config["token"])
