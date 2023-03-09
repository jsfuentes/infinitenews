#!/usr/bin/env python
import json
import requests

# Checkout https://beta.elevenlabs.io/history for full log of audio creation3


def create_audio_file(text, name_of_voice="Bella", file_name="temp"):
    mp3_file_name = file_name + ".mp3"
    # wav_file_name = file_name + ".wav"

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
    print("Got new audio file")

    with open(mp3_file_name, 'wb') as f:
        f.write(r2.content)


if __name__ == '__main__':
    create_audio_file("Hello World, im here bb")
