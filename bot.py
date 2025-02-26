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




# Track groups when bot joins
@client.on(events.ChatAction)
async def track_groups(event):
    chat_id = event.chat_id
    joined_groups.add(chat_id)
    LOGGER.info(f"Bot added to group: {chat_id}")

# Track users when they start the bot in PM
@client.on(events.NewMessage(pattern="/start"))
async def track_users(event):
    user_id = event.sender_id
    pm_users.add(user_id)
    await event.respond("Hello! You have started the bot.")

# Function to send logs to sudo users
async def send_error_log(error_msg):
    for user_id in sudo:
        try:
            await client.send_message(user_id, f"⚠ **Bot Error:**\n\n```{error_msg}```")
        except Exception as e:
            LOGGER.error(f"Failed to send error log to {user_id}: {str(e)}")

# Function to broadcast messages
async def broadcast_message(event, send_to_groups=True, send_to_pm=True):
    sender_id = event.sender_id

    # Check if user is sudo
    if sender_id not in sudo:
        return await event.respond("__You are not authorized to use this command!__")

    # Ensure it's a reply
    if not event.is_reply:
        return await event.respond("__Reply to a message or media to broadcast!__")

    msg = await event.get_reply_message()
    count = 0  # Counter for messages sent

    # Send to groups if enabled
    if send_to_groups:
        for group_id in joined_groups:
            try:
                await client.send_message(group_id, msg)
                count += 1
            except ChatAdminRequiredError:
                err_msg = f"Skipping group {group_id}: Bot is not an admin."
                LOGGER.warning(err_msg)
                await send_error_log(err_msg)
            except ChatWriteForbiddenError:
                err_msg = f"Skipping group {group_id}: Bot cannot send messages."
                LOGGER.warning(err_msg)
                await send_error_log(err_msg)
            except Exception as e:
                err_msg = f"Error in group {group_id}: {str(e)}"
                LOGGER.error(err_msg)
                await send_error_log(err_msg)

    # Send to PM users if enabled
    if send_to_pm:
        for user_id in pm_users:
            try:
                await client.forward_messages(user_id, msg)
                count += 1
            except FloodWaitError as e:
                err_msg = f"Flood wait error ({e.seconds}s). Delaying broadcast..."
                LOGGER.warning(err_msg)
                await send_error_log(err_msg)
                await asyncio.sleep(e.seconds)  # Wait if API limit is hit
            except Exception as e:
                err_msg = f"Error in PM to {user_id}: {str(e)}"
                LOGGER.error(err_msg)
                await send_error_log(err_msg)

    await event.respond(f"✅ Broadcast sent to {count} chats.")

# Command: Broadcast to both groups & PM users
@client.on(events.NewMessage(pattern="^/br$"))
async def broadcast_all(event):
    await broadcast_message(event, send_to_groups=True, send_to_pm=True)

# Command: Broadcast to PM users only
@client.on(events.NewMessage(pattern="^/brp$"))
async def broadcast_pm(event):
    await broadcast_message(event, send_to_groups=False, send_to_pm=True)

# Command: Broadcast to groups only
@client.on(events.NewMessage(pattern="^/brg$"))
async def broadcast_groups(event):
    await broadcast_message(event, send_to_groups=True, send_to_pm=False)






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
