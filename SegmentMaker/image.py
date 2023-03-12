import subprocess
import time
import requests
import json
import openai
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
import platform

import subprocess32 as sp
# task_id = beam_prompt("Majestic, gigantic, beautiful space whales shimmering in wide array of colors in starry space background, stunning, highly detailed, 8k, ornate, intricate, cinematic, dehazed, atmospheric, (oil painting:0.75), (splash art:0.75),(teal:0.2),(orange:0.2), (by Jeremy Mann:0.5), (by John Constable:0.1),(by El Greco:0.5),(acrylic paint:0.75) ")

if platform.system() == "Linux":
    FFMPEG_LOCATION = "/usr/bin/ffmpeg"
else:
    FFMPEG_LOCATION = "/opt/homebrew/bin/ffmpeg"

openai.api_key = "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"


def beam_create_image(topic):
    url = "https://beam.slai.io/4vx9m"
    payload = {"topic": topic}
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Authorization": "Basic NWM3N2VkODQyNzI3NDBhODlhNjk3MjI5YzRhZDRhOGI6OTQxMjk1MGQ2NThhNGUxMzNmNzc1NGVjZjNjMzYxMzA=",
        "Connection": "keep-alive",
        "Content-Type": "application/json"
    }

    response = requests.request(
        "POST", url, headers=headers, data=json.dumps(payload))
    return response.json()["task_id"]


def beam_poll(task_id):
    url = "https://api.slai.io/beam/task"
    payload = {
        "action": "retrieve",
        "task_id": task_id
    }

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Authorization": "Basic NWM3N2VkODQyNzI3NDBhODlhNjk3MjI5YzRhZDRhOGI6OTQxMjk1MGQ2NThhNGUxMzNmNzc1NGVjZjNjMzYxMzA=",
        "Connection": "keep-alive",
        "Content-Type": "application/json"
    }

    while True:
        print("Polling ", task_id)
        resp = requests.request(
            "POST", url, headers=headers, data=json.dumps(payload)).json()
        if resp["status"] == "COMPLETE":
            break
        time.sleep(1)

    if "myimage" not in resp["outputs"]:
        print("Probably Error in image generation")
        return None
    else:
        return resp["outputs"]["myimage"]


def beam_get_image(prompt):
    task_id = beam_create_image(prompt)
    return beam_poll(task_id)


def add_image_to_video(input_image, input_video, output_file, start_time=1, end_time=100, x=675, y=100):
    commands_list = [
        FFMPEG_LOCATION,
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        input_video,
        "-i",
        input_image,
        "-filter_complex",
        f"[0:v][1:v] overlay={x}:{y}:enable='between(t,{start_time},{end_time})'",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "copy",
        output_file
    ]

    if subprocess.run(commands_list).returncode == 0:
        return
    else:
        print("ERROR: Error running ffmpeg add_image_to_video")


def download_and_unzip(url, extract_to='.'):
    http_response = urlopen(url)
    zipfile = ZipFile(BytesIO(http_response.read()))
    zipfile.extractall(path=extract_to)

# https://stackoverflow.com/questions/3844430/how-to-get-the-duration-of-a-video-in-python


def duration(vid_file_path):
    if type(vid_file_path) != str:
        raise Exception('Gvie ffprobe a full file path of the video')

    command = ["ffprobe",
               "-loglevel",  "quiet",
               "-print_format", "json",
               "-show_format",
               "-show_streams",
               vid_file_path
               ]

    pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT)
    out, err = pipe.communicate()
    _json = json.loads(out)

    if 'format' in _json:
        if 'duration' in _json['format']:
            return float(_json['format']['duration'])

    if 'streams' in _json:
        # commonly stream 0 is the video
        for s in _json['streams']:
            if 'duration' in s:
                return float(s['duration'])

    # if everything didn't happen,
    # we got here because no single 'return' in the above happen.
    return 60


def add_images_to_video(topic, video):
    start = time.time()

    video_duration = duration("./wav2lip_beta_whales.mp4")
    image_duration = 15
    number_of_images = round(video_duration // image_duration) - 1
    print(f"Making {number_of_images} images for {video_duration} sec video")
    current_video = video
    for i in range(1, number_of_images + 1):
        url = beam_get_image(topic)
        print("Got image:", url)
        download_and_unzip(url, f"./sd_images/{i}/")
        start_time = i*image_duration
        end_time = i*image_duration+image_duration
        if i != number_of_images:
            new_video = f"./sd_images/output{i}.mp4"
        else:
            new_video = "./sd_images/final_output.mp4"
        add_image_to_video(f"./sd_images/{i}/myimage/output.png",
                           current_video, new_video, start_time=start_time, end_time=end_time)

        current_video = new_video
        print(
            f"Added image {i} to video successfully between {start_time} and {end_time} seconds")

    end = time.time()
    print(f"Completed adding images in: {(end - start)/60} mins")

    return current_video


if __name__ == "__main__":
    add_images_to_video(
        "multidimensional space whales invading our universe", "./wav2lip_beta_whales.mp4")
