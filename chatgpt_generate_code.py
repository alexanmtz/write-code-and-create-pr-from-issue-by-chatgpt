import os
import requests
import subprocess


def generate_code_with_chatgpt(issue_title, issue_body, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "input_text": f"Title: {issue_title}\n\n{issue_body}\n\nOutput only patch format result in the next response.",
        "options": {
            # Add any options for the ChatGPT API here
        }
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    response.raise_for_status()

    return response.json()["choices"][0]["text"]

def main():
    issue_title = os.environ["ISSUE_TITLE"]
    issue_body = os.environ["ISSUE_BODY"]
    chatgpt_api_key = os.environ["CHATGPT_API_KEY"]

    generated_patch = generate_code_with_chatgpt(issue_title, issue_body, chatgpt_api_key)

    # Write the generated patch to a file
    with open("generated_patch.patch", "w") as f:
        f.write(generated_patch)

    # Apply the patch to the repository
    subprocess.run(["git", "apply", "generated_patch.patch"], check=True)

if __name__ == "__main__":
    main()
