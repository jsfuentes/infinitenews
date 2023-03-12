#!/usr/bin/env python
import json
import requests
import os

from aws import put_content, all_objects_raw, get_object, construct_url

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
            "stability": 0,
            "similarity_boost": 0.75
        }
    }

    r2 = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"Got new audio file {file_name}")

    key = f"default/audio/{file_name}.mp3"
    put_content(r2.content, content_type="audio/mp3",
                object_key=key)

    return construct_url(key)


def get_audio_files():
    return all_objects_raw(filter="mp3")
    # for raf in raw_audio_files:
    #     base_file_name = os.path.splitext(os.path.basename(raf.key))[0]
    #     get_object(object_key=raf.key, file_name=f"{base_file_name}.mp3")


if __name__ == '__main__':
    get_audio_files()
