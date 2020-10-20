import win32com.client
import re
from rocketchat_API.rocketchat import RocketChat

rocket = RocketChat('botname', 'botpassword', server_url="https://rockertchaturl.com")

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
folder = outlook.Folders("partsorderemail@domain.com")
inbox = folder.Folders("Inbox")

msg = inbox.Items
msg.sort("[ReceivedTime]", False)
msgs = msg.GetLast()

body = msgs.Body

links = re.findall(r'(https?://\S+)', body)

link = links[1]
link = link[:-1]

msg = "!parts \""+ link + "\""

rocket.chat_post_message(msg, channel="parts", alias="INCOMING PARTS REQUEST").json()
