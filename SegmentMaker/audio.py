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
            "stability": 0.1,
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
    file_name = "1678693121"
    create_audio_file(file_name,  """Alright folks, hold onto your freakin' seats because this is some insane shit I'm about to lay on you. Apparently, scientists have discovered a bunch of goddamn aliens who can communicate telepathically through interpretive dance.

I mean, seriously? What the f*ck? Who knew aliens could be such fucking hipsters? I bet they're all wearing skinny jeans and drinking soy lattes too.

But in all seriousness, this is actually some pretty impressive stuff. Just imagine being able to communicate without ever having to open your damn mouth. Can you even imagine the possibilities? No more awkward small talk at parties, no more pointless conference calls, and heaven forbid, no more cringe-worthy first dates where you're struggling to come up with something to say.

Honestly, I'm a little jealous. I wish I could communicate through interpretive dance. I mean, I already have some pretty killer moves, but imagine if I could convey actual messages through them.

But let's not get ahead of ourselves here. These alien freaks might have some sweet dance moves, but we still don't know what the hell they're saying. For all we know, they're just out there busting a move and we're all sitting here like "oh wow, they're so talented" while they're actually plotting to take over the earth.

Okay, okay, I'm just kidding (kind of). But seriously, this is some pretty groundbreaking shit. Who knows what other kinds of crazy communication methods we'll discover in the future? Maybe in a few years we'll find out that cats have actually been trying to tell us important things through their random meows and we've just been ignoring them this whole time.

In conclusion, let's all take a moment to appreciate the universal language of dance and these telepathic alien freaks. And if any of them happen to be reading this, feel free to hit me up for a dance-off anytime. I'll bring the glow sticks.""")
