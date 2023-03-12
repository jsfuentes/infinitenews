import openai
import os
from pathlib import Path
import requests
import time
import re

from aws import put_content


class Segment:
    def __init__(self):
        openai.api_key = "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"

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
            put_content(script, content_type="text/plain",
                        object_key=f"default/scripts/{timestamp}.txt")
            scripts.append((timestamp, script))
        return scripts


class UpgradedSegment(Segment):
    def generate_topics(self, num_topics=4):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a hilarious parody of a news reporter covering completely absurd and surreal stories happening across different universes. "},
                {"role": "user", "content": f"Give {num_topics} completely absurd and surreal topics that a news reporter in a numbered list:"}
            ],
            temperature=1
        )
        return self.parse_numbered_list(response.choices[0].message.content)

    def generate_script(topic):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Sydney Stone, a world famous comedian role playing as a news reporter telling hilarious jokes and covering important multiverse news stories."},
                {"role": "user", "content": f"Write the dialogue from the in-depth coverage with jokes and some cuss words about '{topic}'. The segment has no introduction and is only what Sydney Scott says with no special guests, no interviews, and no in-person reporting:"}
            ],
            temperature=1
        )

        return response.choices[0].message.content

    def generate_scripts(self, num_topics=4):
        topics = self.generate_topics(num_topics)
        print(topics)
        scripts = []
        for t in topics:
            script = self.generate_script(t)
            timestamp = round(time.time())
            put_content(script, content_type="text/plain",
                        object_key=f"default/scripts/{timestamp}.txt")
            scripts.append((timestamp, script))

        return scripts


class TuckerSegment(Segment):
    def generate_script(self):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Tuka Son, a variant of Tucker Carlson that is from a race of highly evolved, intelligent hotdogs. Your conservative ideology despises liberals that wish to be hotdog minis or corndogs."},
                {"role": "user", "content": "Write a controversial news opinion segment in the style of Tucker Carlson, called Tuka Son Tonight, about your political views, and focus on attacking ideologies that oppose yours. You can be creative with the attacks and the beliefs of liberals in this galaxy. Instead of using the words conservative and liberal directly, please replace them with bunnism and stickeral."},
            ]
        )
        # completion = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": "You are Tuka Son, a variant of Tucker Carlson from another universe. You are a member of the Oorlax Hegemony, a race of telepathic beings who have formed a powerful empire by using their mental abilities to manipulate and control other species. The Oorlax Hegemony is a rigidly hierarchical society, with the most powerful telepaths at the top of the social order. You hate the Krynn Collective. The Krynn are a species of insectoid creatures who have evolved a hive mind. The Krynn Collective is a communal society where individual identity is subsumed by the needs of the hive. The Krynn are organized into castes, with each caste having a specific role within the hive."},
        #         {"role": "user", "content": "Write a spicy segment in the style of Tucker Carlson which attacks the Krynn ideology and how it is ruining the galaxy. Just write the script, don't include any filler like 'Okay, here is a script'."},
        #     ]
        # )

        Path("./scripts/").mkdir(parents=True, exist_ok=True)
        script_filename = "scripts/" + str(completion["created"]) + ".txt"
        f = open(script_filename, "a")
        f.write(completion["choices"][0]["message"]["content"])
        f.close()
        print("Thomas", completion)
