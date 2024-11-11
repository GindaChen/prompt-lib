from typing import Union, Literal
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI
import httpx
from langchain.schema import (
    HumanMessage
)
import openai

def patch_completions__getitem__():
    def __getitem__(self, item):
        try:
            return self.__dict__[item]
        except:
            if item == 'text':
                return self.message.content
            breakpoint()
            pass
    
    def __setitem__(self, item, value):
        try:
            self.__dict__[item] = value
        except:
            breakpoint()
            pass
    
    openai.Completion.__getitem__ = __getitem__
    openai.Completion.__setitem__ = __setitem__

    openai.types.chat.chat_completion.ChatCompletion.__getitem__ = __getitem__
    openai.types.chat.chat_completion.ChatCompletion.__setitem__ = __setitem__

    openai.types.completion.Completion.__getitem__ = __getitem__
    openai.types.completion.Completion.__setitem__ = __setitem__

    openai.types.completion_choice.CompletionChoice.__getitem__ = __getitem__
    openai.types.completion_choice.CompletionChoice.__setitem__ = __setitem__
    
    openai.types.completion_choice.Logprobs.__getitem__ = __getitem__
    openai.types.completion_choice.Logprobs.__setitem__ = __setitem__

    openai.types.chat.chat_completion.Choice.__getitem__ = __getitem__
    openai.types.chat.chat_completion.Choice.__setitem__ = __setitem__

patch_completions__getitem__()

import os
openai.api_key = os.getenv("OPENAI_API_KEY", "sk-proj-1234567890")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "http://localhost:30000/v1/")
print(f"{OPENAI_BASE_URL = }")
# OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "http://localhost:30000/")

class AnyOpenAILLM:
    def __init__(self, *args, **kwargs):
        self.model = openai.OpenAI(
            base_url=OPENAI_BASE_URL,   
            api_key=openai.api_key,
        )

    def __call__(
        self, 
        model=None,
        prompt=None,
        messages=None,
        temperature=None,
        max_tokens=None,
        top_p=None,
        stop=None,
        n=None,
        logprobs=None,
        best_of=None,
    ):
        # breakpoint()
        if prompt:
            result = self.model.completions.create(
                model="default",
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                stop=stop,
                n=n,
                logprobs=logprobs,
                best_of=best_of,
            )
        else:
            result = self.model.chat.completions.create(
                model="default",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                stop=stop,
                n=n,
                logprobs=logprobs,
                best_of=best_of,
            )
        return result
        

    chat = __call__
    completions = __call__


if __name__ == '__main__':
    client = AnyOpenAILLM()
    output = client(
        prompt="Hello, world!",
        logprobs=True,
    )
    print(output)