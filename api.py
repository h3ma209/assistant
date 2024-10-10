import requests
import json

CLAUDE_API_KEY = "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"

def send_to_claude(prompt):
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        result = response.json()
        # Parse the response to get the assistant's message
        assistant_response = parse_assistant_response(result)
        return assistant_response
    else:
        return f"Error: {response.status_code}, {response.text}"

def parse_assistant_response(response):
    if "content" in response and isinstance(response["content"], list):
        # Extract the text content from the assistant's response
        assistant_text = "".join([msg["text"] for msg in response["content"] if msg["type"] == "text"])
        return assistant_text
    return "No content available."

# Test the API with a sample prompt
# if __name__ == "__main__":
#     sample_prompt = "Hello, world"
#     response = send_to_claude(sample_prompt)
#     print("Response from Claude:", response)
