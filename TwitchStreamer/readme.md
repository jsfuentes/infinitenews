Put the twitch key TWITCH_STREAM_KEY="key" in a ```.env``` file.

The script will read a list of video files from the file videos.txt. Put the videos that you want streamed in there

Run the script:
```
source twitchstreamer/bin/activate
source .env && python demo.py -s $TWITCH_STREAM_KEY
```
