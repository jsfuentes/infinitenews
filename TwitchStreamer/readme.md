# Overview
## How Twitch Streaming works
- Twitch has an rtmp endpoint unique for each user
- If we send a video stream to that endpoint, our stream is live

# How we programmatically stream our videos
- We use OBS to create a long-running stream
    - OBS basically creates a video stream in real-time that consists of whatever pictures / videos we add to our "scene" in the app
    - This is better than us feeding the videos directly using rtmp because that requires somehow sending all the vids in a continuous stream (and overlaying other things like donations)
- OBS has support for sending API commands over a websocket, so remote servers can control our stream, as well as ourselves in code via localhost
- We use a python wrapping over this API to send commands over the websocket

# What does this script do?
- Keeps track of videos to play using a deque
- Periodically, it will read from a predefined folder (currently ```videos/```) and add new videos to the front of the deque
- Plays the current video in OBS
- OBS sends a video playback end event, to which we then add the next video into OBS

# Setup

## Prereqs for the script to run
- You need OBS installed
- Your OBS needs to have a scene called "Scene"
- (Optional) Add a "browser source" to the scene with url https://streamelements.com/overlay/64051a1b8a11460c86b9287b/IpDQK2UXMN1Xem3Txg13-Ex2z1q24PZmHtEY7uGLHe01SRPU for donations

## Enable Websocket controls in OBS
- In OBS, go to tools -> WebSocket Server Settings
- Click "Enable WebSocket Server"
- Leave other settings as default and copy the password that OBS gives
- Create a .env file in the ```TwitchStreamer``` folder with ```OBS_PASSWORD="your_password"```

## Run the stream
In the ```TwitchStreamer``` folder, run:

```
source venv/bin/activate
python main.py
```

*The script does not start the stream (it could in the future)* To start the stream, setup OBS
for streaming with your Twitch key and start it through OBS

- Add your Twitch stream key to OBS
- Press "Start streaming"











# Old instructions
Put the twitch key TWITCH_STREAM_KEY="key" in a ```.env``` file.

The script will read a list of video files from the file videos.txt. Put the videos that you want streamed in there

Run the script:
```
source twitchstreamer/bin/activate
source .env && python demo.py -s $TWITCH_STREAM_KEY
```
