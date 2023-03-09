import requests
import openai
import re

openai.api_key = "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"


def get_promptable_config(prompt_id):
    url = f"https://promptable.ai/api/prompt/{prompt_id}/deployment/active"
    r = requests.get(url)
    return r.json()


def get_promptable(prompt_id, inputs={}):
    promptable_resp = get_promptable_config(prompt_id)
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
    print(response)
    return response["choices"][0]["text"].strip()


def get_topics(num_topics=3):
    response = get_promptable("cleajvpum0n04i7eh9ybq72ms", {
                              "num_topics": num_topics})
    # print(response)
    number_regex = r"[0-9]+\. *"
    new_line_seperated_response = re.sub(number_regex, "", response)
    # print(new_line_seperated_response)
    new_line_regex = r"(\n)+"
    topics = re.sub(new_line_regex, "\n",
                    new_line_seperated_response).split("\n")
    # print(topics)
    if len(topics) != num_topics:
        print("Issue parsing topics")
        return []

    return [topic.strip() for topic in topics]


def get_news_segment(topic):
    response = get_promptable("cleak4nv10n06i7ehgvkk03hm", {"topic": topic})
    return response


def generate_news_segments(num_topics):
    topics = get_topics(num_topics)
    print(topics)
    return [get_news_segment(topic) for topic in topics]
