import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError


K = (
    "───▄▀▀▀▄▄▄▄▄▄▄▀▀▀▄───\n"
    "───█▒▒░░░░░░░░░▒▒█───\n"
    "────█░░█░░░░░█░░█────\n"
    "─▄▄──█░░░▀█▀░░░█──▄▄─\n"
    "█░░█─▀▄░░░░░░░▄▀─█░░█\n"
    "█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█\n"
    "█░░╦─╦╔╗╦─╔╗╔╗╔╦╗╔╗░░█\n"
    "█░░║║║╠─║─║─║║║║║╠─░░█\n"
    "█░░╚╩╝╚╝╚╝╚╝╚╝╩─╩╚╝░░█\n"
    "█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█\n"
   " __**I'm MentionAll Bot**, I can mention almost all members in group or channel 👻\nClick **/help** for more information\n if you whant this bot source contact me on @am_dq_fan \n\n"
)

helptext = (
           "╭━━━━╮╱╱╱╱╱╭╮╱╱╱╱╭╮\n"
           "┃╭╮╭╮┃╱╱╱╱╱┃┃╱╱╱╭╯╰╮\n"
           "╰╯┃┃┣┻━┳━━╮┃╰━┳━┻╮╭╯\n"
           "╱╱┃┃┃╭╮┃╭╮┃┃╭╮┃╭╮┃┃\n"
           "╱╱┃┃┃╭╮┃╰╯┃┃╰╯┃╰╯┃╰╮\n"
           "╱╱╰╯╰╯╰┻━╮┃╰━━┻━━┻━╯\n"
           "╱╱╱╱╱╱╱╭━╯┃\n"
           "╱╱╱╱╱╱╱╰━━╯\n"
"**Help Menu of MentionAllBot**\n\nCommand: /all\n__You can use this command with text what you want to mention others.__\n`Example: /all Good Morning!`\n__You can you this command as a reply to any message. Bot will tag users to that replied messsage__.\n\n"
)


logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = 1747534
api_hash = "5a2684512006853f2e48aca9652d83ea"
bot_token = "2079366679:AAE3APD7eFXbNVRnJ26XLTtLv37gXOQ-Gxw"
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply(
    K,
    link_preview=False,
    buttons=(
      [
        Button.url('🧞‍♂️ owner', 'https://t.me/am_dq_fan'),
        Button.url('♻️ add me', 'http://t.me/Miss_mention_bot?startgroup=true')
      ]
    )
  )

@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):    
  await event.reply(
    helptext,
    link_preview=False,
    buttons=(
      [
        Button.url('🧞‍♂️ OWNER', 'https://t.me/am_dq_fan'),
        Button.url('📢updates ', 'https://t.me/TeamFoxBotz')
      ]
    )
  )
  
@client.on(events.NewMessage(pattern="^/all ?(.*)"))
async def mentionall(event):
  chat_id = event.chat_id
  if event.is_private:
    return await event.respond("__This command can be use in groups and channels!__")
  
  is_admin = False
  try:
    partici_ = await client(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.respond("__Only admins can mention all!__")
  
  if event.pattern_match.group(1) and event.is_reply:
    return await event.respond("__Give me one argument!__")
  elif event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.is_reply:
    mode = "text_on_reply"
    msg = await event.get_reply_message()
    if msg == None:
        return await event.respond("__I can't mention members for older messages! (messages which are sent before I'm added to group)__")
  else:
    return await event.respond("__Reply to a message or give me some text to mention others!__")
  
  spam_chats.append(chat_id)
  usrnum = 0
  usrtxt = ''
  async for usr in client.iter_participants(chat_id):
    if not chat_id in spam_chats:
      break
    usrnum += 1
    usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
    if usrnum == 5:
      if mode == "text_on_cmd":
        txt = f"{usrtxt}\n\n{msg}"
        await client.send_message(chat_id, txt)
      elif mode == "text_on_reply":
        await msg.reply(usrtxt)
      await asyncio.sleep(2)
      usrnum = 0
      usrtxt = ''
  try:
    spam_chats.remove(chat_id)
  except:
    pass

# Define sudo users
sudo = [820596651,6248131995]
import os
import logging
import asyncio

# Store groups and users in memory
joined_groups = set()
pm_users = set()

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(name)s - [%(levelname)s] - %(message)s")
LOGGER = logging.getLogger(__name__)


# Event: When bot joins a group
@client.on(events.ChatAction)
async def track_groups(event):
    if event.user_added or event.user_joined:
        chat_id = event.chat_id
        joined_groups.add(chat_id)
        LOGGER.info(f"Bot added to group: {chat_id}")

# Event: When user starts bot in PM
@client.on(events.NewMessage(pattern="/start"))
async def track_users(event):
    user_id = event.sender_id
    pm_users.add(user_id)
    await event.respond("Hello! You have started the bot.")

# Broadcast function (Only for sudo users)
@client.on(events.NewMessage(pattern="^/br$"))
async def broadcast(event):
    sender_id = event.sender_id

    # Check if user is sudo
    if sender_id not in sudo:
        return await event.respond("__You are not authorized to use this command!__")

    # Ensure it's a reply
    if not event.is_reply:
        return await event.respond("__Reply to a message or media to broadcast!__")

    msg = await event.get_reply_message()

    # Broadcast to groups
    for group_id in joined_groups:
        try:
            await client.forward_messages(group_id, msg)
        except Exception as e:
            LOGGER.error(f"Failed to send to group {group_id}: {str(e)}")

    # Broadcast to PM users
    for user_id in pm_users:
        try:
            await client.forward_messages(user_id, msg)
        except Exception as e:
            LOGGER.error(f"Failed to send to user {user_id}: {str(e)}")

    await event.respond("✅ Broadcast sent to all groups and PM users.")






@client.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('__There is no proccess on going...__')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('__Stopped.__')

        
print(">> BOT STARTED <<")
client.run_until_disconnected()
