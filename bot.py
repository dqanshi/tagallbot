import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantsAdmins


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

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply(K, 
                    buttons=(
                      [Button.url('🧞‍♂️ owner', 'https://t.me/am_dq_fan'),   
                      Button.url('♻️ add me', 'http://t.me/Miss_mention_bot?startgroup=true')]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  await event.reply(helptext,
                    buttons=(
                      [Button.url('🧞‍♂️ owner', 'https://t.me/am_dq_fan'),
                      Button.url('📦 Source', 'https://t.me/DQ_fanz')]
                    ),
                    link_preview=False
                   )
  
@client.on(events.NewMessage(pattern="^/all ?(.*)"))
async def all(event):
  if event.is_private:
    return await event.respond("__This command can be use in groups and channels!__")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("__Only admins can mention all!__")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__I can't mention members for older messages! (messages which are sent before I'm added to group)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Give me one argument!__")
  else:
    return await event.respond("__Reply to a message or give me some text to mention others!__")
  
  if mode == "text_on_cmd":
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  if mode == "text_on_reply":
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
print(">> BOT STARTED <<")
client.run_until_disconnected()
