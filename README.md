# StarService

This repo contains a collection of scripts required to produce action card functionality for HVAC or other companies utilizing [Service Titan](https://servicetitan.com), currently only for Part Order Forms.

You must have a [Rocket.Chat](http://rocket.chat) server installed and configured. Along with several channels (#PARTS, #PARTS_HISTORY), which can be renamed to fit your needs. 

You first need to configure email notifications in Service Titan for technicians part order forms completions. 

Then, you need to compile the "Outlook2RocketChat.py" file to an exe (through the use of pyinstaller or some other tool)

Once built into a executable file, you need to configure MS Outlook (or whichever mail client you'll be using), to run the exe each time a part order form email comes in.

Next you need to configure an incoming webhook on your Rocket.Chat server (see the [documentation](https://docs.rocket.chat/guides/administrator-guides/integrations) for that if required). Utilize the contents of the webhook.js file as your script for the webhook.

Finally, you need to configure and run partsbot.py on your Rocket.Chat system. The lines which you must configure start at 7 and ends at line 11.

This is not an easy system to configure and setup, and requires some experience in Python and Javascript development. 

Better results can be achieved through the use of having Service Titan setup outgoing webhooks directly to your Rocket.Chat server, which would then negate the need to parse emails from MS Outlook.

A decent amount of work to setup functionality that's close to what [MyHVACTools](https://www.myhvactools.com/) offers.
