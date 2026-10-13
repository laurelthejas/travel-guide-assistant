"""
llm.py - a tiny wrapper around the LLM server.

Both the chat model and the embedding model are called through the standard
OpenAI-compatible API, so the same code works with llama.cpp or Ollama.
"""
from functools import lru_cache

from openai import OpenAI

import config


@lru_cache
def _client():
    return OpenAI(base_url=config.LLM_BASE_URL, api_key=config.API_KEY, timeout=300)


def chat(prompt, system="You are a helpful travel assistant.", max_tokens=200, temperature=0.1):
    """Send one prompt to the chat model and return its text reply."""
    response = _client().chat.completions.create(
        model=config.CHAT_MODEL,
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()


def embed(texts):
    """Turn a list of texts into a list of embedding vectors."""
    response = _client().embeddings.create(model=config.EMBED_MODEL, input=texts)
    return [item.embedding for item in response.data]


def server_is_up():
    try:
        _client().models.list()
        return True
    except Exception:
        return False
