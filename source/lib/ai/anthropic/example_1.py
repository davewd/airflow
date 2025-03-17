import anthropic

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="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",
)
dd = "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"
message_batch = client.beta.messages.batches.create(
    requests=[
        {
            "custom_id": "first-prompt-in-my-batch",
            "params": {
                "max_tokens": 100,
                "messages": [
                    {
                        "role": "user",
                        "content": "Hey Claude, tell me a short fun fact about video games!",
                    }
                ],
            },
        },
        {
            "custom_id": "second-prompt-in-my-batch",
            "params": {
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": 100,
                "messages": [
                    {
                        "role": "user",
                        "content": "Hey Claude, tell me a short fun fact about bees!",
                    }
                ],
            },
        },
    ]
)
print(message_batch)
