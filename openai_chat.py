import openai
import json
import os
import sys

def get_openai_response(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()

def save_chat_to_json(input_text, output_text, file_name="chat_history.json"):
    chat_data = {
        "input": input_text,
        "output": output_text
    }

    with open(file_name, "a+") as f:
        f.seek(0)
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []

        data.append(chat_data)

        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=2)

def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set the OPENAI_API_KEY environment variable.")
        sys.exit(1)

    while True:
        user_input = input("You: ")
        if user_input.lower() in ("quit", "exit", "bye"):
            break

        openai_response = get_openai_response(user_input)
        print(f"AI: {openai_response}")

        save_chat_to_json(user_input, openai_response)

if __name__ == "__main__":
    main()
