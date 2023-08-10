# Writes a backup of a discord server as a json string.
# Inspired by https://www.youtube.com/watch?v=xh28F6f-Cds
# This was useful too:
# https://gist.github.com/hackermondev/5c928ca12b4f4e6320100b11f798c23b
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
serverId = '1116612173767135342'  # AI chat

def get(url):
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        sys.exit(r.text)
    return json.loads(r.text)

channels = get(f'https://discord.com/api/v9/guilds/{serverId}/channels')
allMessages = []
for channel in channels:
    messages = get(f'https://discord.com/api/v9/channels/{channel["id"]}/messages')
    for message in messages:
        message['threadMessages'] = []
        if 'thread' in message:
            threadId = message['thread']['id']
            threadMessages = get(f'https://discord.com/api/v9/channels/{threadId}/messages')
            message['threadMessages'] += [t for t in threadMessages if t['content'] != '']
    allMessages.append({'channel': channel, 'messages': messages})
print(json.dumps(allMessages, indent=4))
