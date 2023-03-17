import openai
import os
from pathlib import Path
import requests
import time
import re

from aws import put_content


class Segment:
    def __init__(self, eleven_voice_name="Bella"):
        openai.api_key = "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"
        self.eleven_voice_name = eleven_voice_name

    def generate_scripts(self):
        raise NotImplementedError()

    def parse_numbered_list(self, raw_list):
        number_regex = r"[0-9]+\. *"
        new_line_seperated_response = re.sub(number_regex, "", raw_list)
        # print(new_line_seperated_response)
        new_line_regex = r"(\n)+"
        l = re.sub(new_line_regex, "\n",
                   new_line_seperated_response).split("\n")
        #     print(l)
        return l

    def get_promptable_config(self, prompt_id):
        url = f"https://promptable.ai/api/prompt/{prompt_id}/deployment/active"
        r = requests.get(url)
        return r.json()

    def get_promptable(self, prompt_id, inputs={}):
        promptable_resp = self.get_promptable_config(prompt_id)
        # print(promptable_resp)
        model = promptable_resp["config"]["model"]
        temperature = promptable_resp["config"]["temperature"]
        max_tokens = promptable_resp["config"]["max_tokens"]

        prompt = promptable_resp["text"]

        for prompt_input in promptable_resp["inputs"]:
            name = prompt_input["name"]
            if name not in inputs:
                default_value = prompt_input["value"]
                print(f"Going with default {name} - {default_value}")
                prompt = prompt.replace("{{" + name + "}}", str())
            else:
                prompt = prompt.replace("{{" + name + "}}", str(inputs[name]))

        #     print(prompt)
        response = openai.Completion.create(
            model=model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        # print(response)
        return response["choices"][0]["text"].strip()

    def replaceWord(self, text, pre_word, post_word):
        text = text.replace(pre_word, post_word)
        text = text.replace(pre_word.lower(), post_word.lower())
        text = text.replace(pre_word.upper(), post_word.upper())
        text = text.replace(pre_word.title(), post_word.title())
        return text

    def uncensorWords(self, script):
        script = self.replaceWord(script, "f***", "fuck")
        script = self.replaceWord(script, "f*ck", "fuck")
        script = self.replaceWord(script, "f*cking", "fucking")
        script = self.replaceWord(script, "f**king", "fucking")
        script = self.replaceWord(script, "sh*t", "shit")
        script = self.replaceWord(script, "b****es", "bitches")
        script = self.replaceWord(script, "motherf**kin", "motherfuckin")
        return script

    def generate_topics(self, num_topics):
        raise NotImplementedError

    def generate_script(self, topic):
        raise NotImplementedError

    def generate_scripts(self, num_topics=4):
        topics = self.generate_topics(num_topics)
        print(topics)
        scripts = []
        for topic in topics:
            (script_name, script) = self.generate_script(topic)
            scripts.append((script_name, topic, script))

        return scripts


class DefaultSegment(Segment):
    def generate_topics(self, num_topics=3):
        response = self.get_promptable("cleajvpum0n04i7eh9ybq72ms", {
            "num_topics": num_topics})
        topics = self.parse_numbered_list(response)
        # print(topics)
        if len(topics) != num_topics:
            print("Issue parsing topics")
            return []

        return [topic.strip() for topic in topics]

    def generate_script(self, topic):
        response = self.get_promptable(
            "cleak4nv10n06i7ehgvkk03hm", {"topic": topic})
        print("Generated script for topic: " + topic)
        return response

    def generate_scripts(self, num_topics=2):
        topics = self.generate_topics(num_topics)
        scripts = []
        for topic in topics:
            script = self.generate_script(topic)
            timestamp = round(time.time())
            put_content(topic, content_type="text/plain",
                        object_key=f"default/topic/{timestamp}.txt")
            put_content(script, content_type="text/plain",
                        object_key=f"default/scripts/{timestamp}.txt")
            scripts.append((timestamp, topic, script))
        return scripts


class UpgradedSegment(Segment):
    def __init__(self):
        super(UpgradedSegment, self).__init__("Bella")

    def generate_topics(self, num_topics=4):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a hilarious parody of a news reporter covering completely absurd and surreal stories happening across different universes. "},
                {"role": "user",
                 "content": f"Give {num_topics} completely absurd and surreal short topics happening across different universes that a news reporter will cover in a numbered list:"}
            ],
            temperature=1
        )
        return self.parse_numbered_list(response.choices[0].message.content)

    def generate_script(self, topic):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a Sydney Stone, a comedian role playing as a news reporter telling hilarious jokes and covering important multiverse news stories."},
                {"role": "user",
                 "content": f"Write the dialogue from the in-depth coverage with jokes and completely uncensored cuss words about '{topic}'. The segment has no introduction and is only what Sydney Stone says with no special guests, no interviews, no action cues, and no in-person reporting:"}
            ],
            temperature=1
        )

        script = response.choices[0].message.content
        script = self.uncensorWords(script)

        script_name = f"{round(time.time())}_upgraded"
        put_content(topic, content_type="text/plain",
                    object_key=f"default/topic/{script_name}.txt")
        put_content(script, content_type="text/plain",
                    object_key=f"default/scripts/{script_name}.txt")
        return script_name, script


class BananaSegment(Segment):
    def __init__(self):
        super(BananaSegment, self).__init__("Sam")

    def generate_topics(self, num_topics=4):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a racy, slightly controversial question and answer columnist for an intergalactic television network. You answer absurd questions submitted from peculiar beings across multiple universes."},
                {"role": "user",
                 "content": f"Give {num_topics} completely absurd and surreal short questions that viewers of your television segment would ask in a numbered list:"}
            ],
            temperature=1
        )
        return self.parse_numbered_list(response.choices[0].message.content)

    def generate_script(self, topic):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a racy, slightly controversial question and answer columnist for an intergalactic television network. You answer absurd questions submitted from peculiar beings across multiple universes. You typically address the person you are talking to as 'hun'. You always start your segments by saying the asker's name (which you make up), and then repeat the question exactly."},
                {"role": "user",
                 "content": f"You are writing an answer to a user submitted question. You can be weird, tangential, and wacky in your answer. You do not need to be factual. Write an answer for the following user submitted question, and start by repeating the question along with the asker's name (you can make the name up): Can I use my tentacles to tap dance if I install mini tap shoes on them?"},
                {"role": "assistant",
                 "content": "Hello, huns. Becky the Whale asks, 'Can I use my tentacles to tap dance if I install mini tap shoes on them?'. Well, well, well, hun. It seems like you're quite the multi-talented creature. To answer your question, yes, you can absolutely use your tentacles to tap dance if you're able to install those mini tap shoes on them. But let's take a moment to appreciate the uniqueness of your situation. How many beings can say they have tap-dancing tentacles? You're a true visionary, hun. Just be careful not to trip over your own feet... er, tentacles. Keep shining like the star you are!"},
                {"role": "user",
                 "content": f"You are writing an answer to a user submitted question. You can be weird, tangential, and wacky in your answer. You do not need to be factual. Write an answer for the following user submitted question, and start by repeating the question along with the asker's name (you can make the name up): Can I use my tentacles to write a love letter to a black hole?"},
                {"role": "assistant",
                 "content": "Hello, huns. Mr Squidson asks, 'Can I use my tentacles to write a love letter to a black hole?'. Oh, hun, you're just full of surprises, aren't you? I'm not sure if tentacles are the most romantic appendages to use for a love letter, but who am I to judge? As for writing to a black hole, well, that's a bit of a tricky situation. You see, black holes are notorious for their voracious appetite, so it's best not to get too close. But if you really want to express your love to this cosmic giant, might I suggest a more unconventional method? Maybe you could try encoding your love letter into a stream of subatomic particles and launching them towards the black hole. Or perhaps you could create a holographic projection of your message that would dance around the black hole's event horizon. Just make sure to avoid getting sucked in yourself, hun. Love can be a powerful force, but it's no match for the gravitational pull of a black hole."},
                {"role": "user",
                 "content": f"You are writing an answer to a user submitted question. You can be weird, tangential, and wacky in your answer. You do not need to be factual. Write an answer for the following user submitted question, and start by repeating the question along with the asker's name (you can make the name up): '{topic}'."}
            ],
            temperature=1
        )

        script = response.choices[0].message.content
        script = self.uncensorWords(script)

        script_name = f"{round(time.time())}_bananaqa"
        put_content(topic, content_type="text/plain",
                    object_key=f"default/topic/{script_name}.txt")
        put_content(script, content_type="text/plain",
                    object_key=f"default/scripts/{script_name}.txt")
        return script_name, script


if __name__ == "__main__":
    segment = UpgradedSegment()
    segment.generate_script(
        "the future of content is here. A 24/7 news broadcast on twitch where the AI voice, audio, video, and script are all AI generated")
