# Instagram-to-discord-1

This script executes 3 actions:

1. Monitors for new image posted in a instagram account.
2. If found new image, a bot posts new instagram image in a discord channel.
3. Repeat after set interval.

<details><summary><b>Changelog (basic vs fork) :</b></summary>
<p>

- Add multi-user support
- File support
- Improved embed
- Bypass instagram's anti-bot security
- Sends all the photos and videos that have been published during the interval (example: if the user sends 3 photos in the same minute, the bot will send the 3 photos)
- Detection of a video
- Ignore the 1st verification
- Minor changes (optimization of functions, removal of comments, useless dependencies and environment variables, reduction of the verification interval, ...)
</p>
</details>

## Requirements:

- Python v3
- requests (`pip install requests` or `pip3 install requests`)

## Usage:

Variable settings:

- In the "users.txt" file : 
    - Put the usernames of all the Instagram accounts you want to monitor (respect the list formatting)

- In the script : 
    - Set WEBHOOK_URL to Discord Webhook URL. To know how, just Google: "how to create webhook discord".
    - Set TIME_INTERVAL to the time in seconds in between each check for a new post. Example: 1.5, 600 (default=300)

## Collaborations:

Collaborations to improve script are always welcome.
