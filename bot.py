from pyrogram import Client, filters
from pyrogram.types import *
from pymongo import MongoClient
from metaapi import META
import requests
import aiohttp
import asyncio

import os

meta = META()

video_group = 3
photo_group = 4

# 😂 Asewsome Module Made By Moezilla 😉
# Fun Fact - Moezilla Is Gay
# Copyright By MetaVoid

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URL = os.environ.get("MONGO_URL")
LOG = os.environ.get("LOG_CHANNEL")

app = Client(
    "Sfw" ,
    api_id = API_ID ,
    api_hash = API_HASH ,
    bot_token = BOT_TOKEN
)


regex_video = r"^((?i)slap|bully|cuddle|cry|hug|kiss|smile|pat|kill|bite|kick|happy|dance|cringe)$"
regex_photo = r"^((?i)waifu|neko|awoo|shinobu|megumin)$"



async def is_admins(chat_id: int):
    return [
        member.user.id
        async for member in bot.iter_chat_members(
            chat_id, filter="administrators"
        )
    ]

@app.on_message(
    filters.command("togglesfw", prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def levelsystem(_, message): 
    sfwdb = MongoClient(MONGO_URL)
   
    toggle = sfwdb["SfwDb"]["Sfw"] 
    if message.from_user:
        user = message.from_user.id
        chat_id = message.chat.id
        if user not in (
            await is_admins(chat_id)
        ):
            return await message.reply_text(
                "You are not admin"
            )
    is_sfw = toggle.find_one({"chat_id": message.chat.id})
    if not is_sfw:
        toggle.insert_one({"chat_id": message.chat.id})
        await message.reply_text("Sfw System Enable")
        await app.send_message(LOG, f"#SFW-ENABLE\nCHAT -  @{message.chat.username}\n ADMIN - [{message.from_user.first_name}](tg://user?id={message.from_user.id})")
    else:
        toggle.delete_one({"chat_id": message.chat.id})
        await message.reply_text("Sfw System Disable")
        await app.send_message(LOG, f"#SFW-DISABLE\nCHAT -  @{message.chat.username}\n ADMIN - [{message.from_user.first_name}](tg://user?id={message.from_user.id})")


@app.on_message(
    filters.text
    & filters.reply
    & filters.regex(regex_video),
    group=video_group,
)                              
async def video(client, message): 
    Msg = message.text
    sfwdb = MongoClient(MONGO_URL)    
    mainuser = sfwdb["SfwDb"][f"{Msg}"]
    toggle = sfwdb["SfwDb"]["Sfw"] 
    otheruser = sfwdb["UserSfwDb"][f"{Msg}"]
    replyuser = message.reply_to_message.from_user.id
    user = message.from_user.id
    is_sfw = toggle.find_one({"chat_id": message.chat.id})
    if is_sfw:
        k = mainuser.find_one({"user": replyuser})
        n = otheruser.find_one({"user": user})

        if not message.reply_to_message.from_user.is_bot:
            if k is None:             
                x = requests.get(f"https://api.waifu.pics/sfw/{Msg}").json()
                x = x['url']
                if not n:
                    input = {"user": replyuser, "time": 1}
                    input1 = {"user": user, "time": 1}
                    mainuser.insert_one(input)
                    otheruser.insert_one(input1)
                    await message.reply_video(video=x, caption=f"{message.from_user.mention} is giving {message.reply_to_message.from_user.mention} a {Msg}!\n {message.reply_to_message.from_user.mention} has been {Msg} 1 times and {message.from_user.mention} has {Msg} others 1 times")
                if n:
                    input = {"user": replyuser, "point": 1}
                    mainuser.insert_one(new)
                    t = n["time"] + 1
                    other.update_one({"user": user}, {
                    "$set": {"time": t}})
                    await message.reply_video(video=x, caption=f"{message.from_user.mention} is giving {message.reply_to_message.from_user.mention} a {Msg}!\n {message.reply_to_message.from_user.mention} has been {Msg} 1 times and {message.from_user.mention} has {Msg} others {t} times")           
            else:
                if not n:                
                    t = k["time"] + 1
                    x = requests.get(f"https://api.waifu.pics/sfw/{Msg}").json()
                    x = x['url'] 
                    input = {"user": replyuser, "time": 1}
                    mainuser.insert_one(input)            
                    otheruser.update_one({"user": fuser}, {
                        "$set": {"time": t}})
                    time = t
                    await message.reply_video(video=x, caption=f"{message.from_user.mention} is giving {message.reply_to_message.from_user.mention} a {Msg}!\n {message.reply_to_message.from_user.mention} has been {Msg} {time} times and {message.from_user.mention} has {Msg} others 1 times")
                if n:
                    t = k["time"] + 1
                    t1 = n["time"] + 1
                    x = requests.get(f"https://api.waifu.pics/sfw/{Msg}").json()
                    x = x['url']
                    mainuser.update_one({"user": replyuser}, {
                        "$set": {"time": t}})            
                    other.update_one({"user": user}, {
                        "$set": {"time": t2}})
                    time = t
                    await message.reply_video(video=x, caption=f"{message.from_user.mention} is giving {message.reply_to_message.from_user.mention} a {Msg}!\n {message.reply_to_message.from_user.mention} has been {Msg} {time} times and {message.from_user.mention} has {Msg} others {t1} times")
                

@app.on_message(
    filters.text
    & filters.reply
    & filters.regex(regex_photo),
    group=image_group,
)                              
async def image(client, message): 
    Msg = message.text
    sfwdb = MongoClient(MONGO_URL)    
    mainuser = sfwdb["SfwDb"][f"{Msg}"]
    toggle = sfwdb["SfwDb"]["Sfw"] 
    otheruser = sfwdb["UserSfwDb"][f"{Msg}"]
    replyuser = message.reply_to_message.from_user.id
    user = message.from_user.id
    is_sfw = toggle.find_one({"chat_id": message.chat.id})
    if is_sfw:
        k = mainuser.find_one({"user": replyuser})
        n = otheruser.find_one({"user": user})

        if not message.reply_to_message.from_user.is_bot:
            if k is None:             
                x = requests.get(f"https://api.waifu.pics/sfw/{Msg}").json()
                x = x['url']
                if not n:
                    input = {"user": replyuser, "time": 1}
                    input1 = {"user": user, "time": 1}
                    mainuser.insert_one(input)
                    otheruser.insert_one(input1)
                    await message.reply_photo(photo=x, caption=f"{message.from_user.mention} is giving {message.reply_to_message.from_user.mention} a {Msg}!\n {message.reply_to_message.from_user.mention} has been {Msg} 1 times and {message.from_user.mention} has {Msg} others 1 times")
                if n:
                    input = {"user": replyuser, "point": 1}
                    mainuser.insert_one(new)
                    t = n["time"] + 1
                    other.update_one({"user": user}, {
                    "$set": {"time": t}})
                    await message.reply_photo(photo=x, caption=f"{message.from_user.mention} is giving {message.reply_to_message.from_user.mention} a {Msg}!\n {message.reply_to_message.from_user.mention} has been {Msg} 1 times and {message.from_user.mention} has {Msg} others {t} times")           
            else:
                if not n:                
                    t = k["time"] + 1
                    x = requests.get(f"https://api.waifu.pics/sfw/{Msg}").json()
                    x = x['url'] 
                    input = {"user": replyuser, "time": 1}
                    mainuser.insert_one(input)            
                    otheruser.update_one({"user": fuser}, {
                        "$set": {"time": t}})
                    time = t
                    await message.reply_photo(photo=x, caption=f"{message.from_user.mention} is giving {message.reply_to_message.from_user.mention} a {Msg}!\n {message.reply_to_message.from_user.mention} has been {Msg} {time} times and {message.from_user.mention} has {Msg} others 1 times")
                if n:
                    t = k["time"] + 1
                    t1 = n["time"] + 1
                    x = requests.get(f"https://api.waifu.pics/sfw/{Msg}").json()
                    x = x['url']
                    mainuser.update_one({"user": replyuser}, {
                        "$set": {"time": t}})            
                    other.update_one({"user": user}, {
                        "$set": {"time": t2}})
                    time = t
                    await message.reply_photo(photo=x, caption=f"{message.from_user.mention} is giving {message.reply_to_message.from_user.mention} a {Msg}!\n {message.reply_to_message.from_user.mention} has been {Msg} {time} times and {message.from_user.mention} has {Msg} others {t1} times")
                
  

@app.on_message(
    filters.command("check", prefixes=["/", ".", "?", "-"])
& filters.reply)
async def hi(client, message): 
    sfwdb = MongoClient(MONGO_URL)
    Msg = message.command[1]
    toggle = sfwdb["SfwDb"]["Sfw"] 
    mainuser = sfwdb["SfwDb"][f"{Msg}"]
    otheruser = sfwdb["UserSfwDb"][f"{Msg}"]    
    user = message.from_user.id
    is_sfw = toggle.find_one({"chat_id": message.chat.id})
    if is_sfw:
        k = mainuser.find_one({"user": user})
        n = otheruser.find_one({"user": user})
        if not message.reply_to_message.from_user.is_bot:
            if k is None:
                if not n:
                    await message.reply_text("Nothing Data")
                if n:
                    t = n["time"] 
                    await message.reply_text(f"{message.reply_to_message.from_user.mention} has {Msg} others {t} times")
            else:
                if not n:
                    t = k["time"]
                    await message.reply_text(f"{message.reply_to_message.from_user.mention} has been {Msg} {t} times")
                if n:
                    t = k["time"]
                    t1 = n["time"]
                    await message.reply_text(f"{message.reply_to_message.from_user.mention} has been {Msg} {t} times and {message.reply_to_message.from_user.mention} has {Msg} others {t1} times")
                


app.run()
