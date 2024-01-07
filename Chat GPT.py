import os
from openai import OpenAI

client = OpenAI(
    api_key="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",
)
def get_user_input():
    return input("User: ")
def get_model_response(user_message):
    return client.chat.completions.create(
        messages=[
            {"role": "user", "content": user_message},
        ],
        model="gpt-3.5-turbo",
    )["choices"][0]["message"]["content"]

print("Chat with GPT-3.5-turbo. Type 'q' to end the conversation.")
while True:
    user_input = get_user_input()

    if user_input.lower() == 'q':
        print("Conversation ended.")
        break
    model_response = get_model_response(user_input)
    print(f"AI: {model_response}")