"""
llm_server.py - local OpenAI-compatible server for the chat + embedding models (llama.cpp).

Models are listed in llm_server_config.json. Start with start_llm_server.bat and keep it open.
The two model files must be in the models/ folder (they are not in git). Their sources, licenses and the
one-line download command are at the top of config.py.

Server software: llama.cpp (https://github.com/ggml-org/llama.cpp, MIT) through its Python binding
llama-cpp-python (https://github.com/abetlen/llama-cpp-python, MIT); install command in requirements.txt.

Small adapter: Microsoft GraphRAG asks for JSON output using the newer
response_format "json_schema", while llama.cpp expects "json_object" + "schema".
We translate it, and llama.cpp then FORCES the output to match the schema,
so even a tiny model returns valid JSON. We also add length limits to the
schema, so small models can't ramble past the token limit and break the JSON.
"""
import json

MAX_STRING_CHARS = 200
MAX_LIST_ITEMS = 2


def add_limits(schema):
    """Recursively give every string a maxLength and every list a maxItems."""
    if isinstance(schema, dict):
        if schema.get("type") == "string":
            schema.setdefault("maxLength", MAX_STRING_CHARS)
        if schema.get("type") == "array":
            schema.setdefault("maxItems", MAX_LIST_ITEMS)
        for value in schema.values():
            add_limits(value)
    elif isinstance(schema, list):
        for value in schema:
            add_limits(value)
    return schema

import uvicorn
from llama_cpp.server.app import create_app
from llama_cpp.server.settings import ConfigFileSettings, ServerSettings


class JsonSchemaAdapter:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope["path"] != "/v1/chat/completions":
            return await self.app(scope, receive, send)

        body, more = b"", True                      # read the whole request body
        while more:
            message = await receive()
            body += message.get("body", b"")
            more = message.get("more_body", False)

        try:
            data = json.loads(body)
            fmt = data.get("response_format") or {}
            if fmt.get("type") == "json_schema":
                data["response_format"] = {"type": "json_object",
                                           "schema": add_limits(fmt["json_schema"].get("schema"))}
                body = json.dumps(data).encode()
        except (ValueError, KeyError, AttributeError):
            pass

        headers = [(k, v) for k, v in scope["headers"] if k != b"content-length"]
        scope = dict(scope, headers=headers + [(b"content-length", str(len(body)).encode())])
        delivered = False

        async def new_receive():
            nonlocal delivered
            if not delivered:
                delivered = True
                return {"type": "http.request", "body": body, "more_body": False}
            return await receive()

        await self.app(scope, new_receive, send)


if __name__ == "__main__":
    with open("llm_server_config.json", "rb") as f:
        file_settings = ConfigFileSettings.model_validate_json(f.read())
    server = ServerSettings.model_validate(file_settings)
    app = create_app(server_settings=server, model_settings=file_settings.models)
    print(f"LLM server running on http://{server.host}:{server.port}/v1  (Ctrl+C to stop)")
    uvicorn.run(JsonSchemaAdapter(app), host=server.host, port=server.port)
