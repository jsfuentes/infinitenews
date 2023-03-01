import os

import openai_wrapper


def get_completion(prompt, model="text-davinci-003", max_tokens=16, temperature=0.7, top_p=1, num_completions=1, stream=False, logprobs=None, echo=False, stop=None, presence_penalty=0, frequency_penalty=0, best_of=1):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.Model.retrieve("text-davinci-003")
    openai.Completion.create(
        model="text-davinci-003",
        prompt="Say this is a test",
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        n=num_completions,
        stream=stream,
        logprobs=logprobs,
        echo=echo,
        stop=stop,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty,
        best_of=best_of
    )