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

@client.on(events.NewMessage(pattern="^/br$"))
async def broadcast(event):
    chat_id = event.chat_id
    sender_id = event.sender_id

    # Check if the user is in the sudo list
    if sender_id not in sudo:
        return await event.respond("__You are not authorized to use this command!__")

    if event.is_reply:
        # If it's a reply, get the original message
        msg = await event.get_reply_message()
        if not msg:
            return await event.respond("__You need to reply to a message!__")
    else:
        return await event.respond("__Reply to a message or media to broadcast!__")

    # Get all the groups the bot is a member of
    all_groups = await client.get_dialogs()
    target_chats = [dialog for dialog in all_groups if dialog.is_group]

    # Get all users who have started the bot in PM
    pm_users = []
    async for user in client.iter_participants('me'):  # 'me' refers to the bot's own user
        pm_users.append(user)

    # Start forwarding the message to all groups and PM users
    for group in target_chats:
        if group.is_group:
            try:
                await client.forward_messages(group.id, msg)
            except Exception as e:
                LOGGER.error(f"Failed to forward to group {group.id}: {str(e)}")

    for user in pm_users:
        try:
            await client.forward_messages(user.id, msg)
        except Exception as e:
            LOGGER.error(f"Failed to forward to user {user.id}: {str(e)}")

    return await event.respond(f"Broadcast message has been sent to all groups and PM users.")




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
