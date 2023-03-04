import openai
import os
from pathlib import Path

class Segment:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        print("openai apy ket", openai.api_key)

    def generate_script(self):
        raise NotImplementedError()


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
