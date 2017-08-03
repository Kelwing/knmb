import argparse
import discord
import asyncio
from models import *

superadmin = '109710323094683648'

parser = argparse.ArgumentParser(description='Auttaja Music Bot')
parser.add_argument('token', type=str, help='The Discord bot token you want to run as')
parser.add_argument('--database', type=str, help='Path to the sqlite database to use, defaults to musicbot.db')

args = parser.parse_args()

def create_tables():
    db.connect()
    db.create_tables([Song, Playlist, Mapping, Operator, Server], True)

create_tables()

client = discord.Client()

running = True

npmap = dict() # map of now playing queues
plmap = dict() # map of active playlists
csmap = dict() # map of the current song in the playlist
players = dict()

@client.event
async def on_ready():
    for s in client.servers:
        try:
            Server.get(server_id == s.id)
        except:
            new_server = Server.create(
                    server_id=s.id
                    )
            new_server.save()
        npmap[s.id] = asyncio.Queue(loop=client.loop)
        client.loop.create_task(music_loop(s.id))

@client.event
async def on_message():
    pass

# Plays a song from YouTube
async def play(video, server_id):
    await npmap[server_id].put(video)

# Pauses playback
async def pause():
    pass
# Loads a playlist by name
async def load(playlist):
    pass

# Adds a song to a playlist
async def add(playlist, song):
    pass

# Returns the name of the currently playing song
async def np():
    pass

# Returns the next 10 songs that will be played
async def list():
    pass

# Per server music loop :-)
async def music_loop(server_id):
    await client.wait_until_ready()
    s = client.get_server(server_id)
    ds = Server.get(Server.server_id==server_id)
    while running:
        await asyncio.sleep(1)
        if not client.is_voice_connected(s):
            if ds.autojoin:
                c = client.get_channel(f'{ds.music_channel}')
                players[server_id] = await client.join_voice_channel(c)
        if server_id in players and not players[server_id].is_done():
            continue
        try:
            song = npmap[server_id].get_nowait()
        except KeyError as e:
            print(f"[ERROR] Now playing queue for {s.name} not created")
            continue
        except asyncio.QueueEmpty as e:
            print(f"[WARN] Now playing queue for {s.name} is empty")
            continue

        if 'http:' in song or 'https:' in song:
            players[server_id] = await client.voice_client(s).create_ytdl_player(song)
        else:
            players[server_id] = await client.voice_client(s).create_ytdl_player(f"ytsearch:{song}")



client.run(args.token)
