from __future__ import print_function

import ffmpeg

import argparse

#  Reading s3 https://stackoverflow.com/questions/2677317/how-to-read-remote-video-on-amazon-s3-using-ffmpeg
# Using ffmpeg-python https://stackoverflow.com/questions/68382868/how-can-i-convert-an-ffmpeg-command-line-to-ffmpeg-python-code

# ffmpeg twitch command from chatgpt
# ffmpeg -re -i input.mp4 -c:v libx264 -preset veryfast -maxrate 3000k -bufsize 6000k -pix_fmt yuv420p -g 60 -c:a aac -b:a 128k -ar 44100 -f flv rtmp://live.twitch.tv/app/STREAM_KEY

# Figures out next video
# Creates a signed s3 url
# Returns
def get_next_video_url(prev_video_name=None):
    return {"name": "videoplayback.mp4", "url": "videoplayback.mp4"}

# Creates the video stream from the url and returns it without running it
def prepare_video_stream(video_url):
    stream = ffmpeg.input(video_url)
    stream = ffmpeg.output(stream, rtmp_endpoint, vcodec="libx264", preset="veryfast", maxrate="3000k", bufsize="6000k",
                           pix_fmt="yuv420p", g="60", **{"b:v": "5M"}, acodec="aac", **{"b:a": "128k"}, ar="44100",
                           f="flv")
    return stream

# Example usage: source .env && python demo.py -s $TWITCH_STREAM_KEY
# Reading env variable with python or virtualenv not working idk why
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    required = parser.add_argument_group('required arguments')
    required.add_argument('-s', '--streamkey',
                          help='twitch streamkey',
                          required=True)
    required.add_argument('-e', '--endpoint',
                          help='twitch rtmp endpoint to stream to. See https://stream.twitch.tv/ingests/. Defaults to LAX',
                          default="rtmp://lax.contribute.live-video.net/app/")
    args = parser.parse_args()

    # STREAM_KEY = os.getenv("TWITCH_STREAM_KEY")

    rtmp_endpoint = args.endpoint + args.streamkey

    # ffmpeg [your input parameters] -vcodec libx264 -b:v 5M -acodec aac -b:a 256k -f flv [your RTMP URL]
    prev_video_name = None
    while True:
        next_video = get_next_video_url(prev_video_name)
        prev_video_name = next_video["name"]
        stream = prepare_video_stream(next_video["url"])
        # stream = ffmpeg.input("videoplayback.mp4")
        # stream = ffmpeg.output(stream, rtmp_endpoint, vcodec="libx264", preset="veryfast", maxrate="3000k", bufsize="6000k", pix_fmt="yuv420p", g="60", **{"b:v": "5M"}, acodec="aac", **{"b:a": "128k"}, ar="44100", f="flv")
        stream.run()
    # print("THOMAS", stream.compile())
