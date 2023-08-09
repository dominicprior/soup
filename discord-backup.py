# Writes a backup of a discord server as a json string.
# Inspired by https://www.youtube.com/watch?v=xh28F6f-Cds
# It is currently hardwired to backup the "AI chat" server.
# The auth argument can be found by examining the network
# traffic in the browser devtools as shown in the YouTube video.
import argparse
import requests
import json
import sys
parser = argparse.ArgumentParser(description='Prints the channels and messages')
parser.add_argument('auth')
args = parser.parse_args()
headers = { 'authorization': args.auth }
serverId = '1138791781106978866'  # AI chat server
r = requests.get(f'https://discord.com/api/v9/guilds/{serverId}/channels',
        headers=headers)
if r.status_code != 200:
    sys.exit(r.text)
channels = json.loads(r.text)
messages = []
for channel in channels:
    channelId = channel['id']
    r = requests.get(f'https://discord.com/api/v9/channels/{channelId}/messages',
                    headers=headers)
    m = json.loads(r.text)
    messages.append({'channel': channel, 'messages': m})
print(json.dumps(messages, indent=4))
