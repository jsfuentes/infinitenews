#!/usr/bin/env python
import json
import requests
import time

from aws import put_content

# Checkout https://beta.elevenlabs.io/history for full log of audio creation3


def create_audio_file(file_name, text, name_of_voice="Bella"):
    r1 = requests.get('https://api.elevenlabs.io/v1/voices')
    resp = r1.json()
    rid = ""
    for voice in resp["voices"]:
        if voice["name"] == name_of_voice:
            # print(voice)
            rid = voice["voice_id"]
            break

    url = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}".format(
        voice_id=rid)
    headers = {'xi-api-key': "aa42307ce6bfbefcfd2abd4d8634127b"}
    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.3,
            "similarity_boost": 0.75
        }
    }

    r2 = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"Got new audio file {file_name}")

    put_content(r2.content, content_type="audio/mp3",
                object_key=f"default/audio/{file_name}.mp3")


if __name__ == '__main__':
    create_audio_file("Hello World, im here bb")
