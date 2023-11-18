import openai

openai.api_key = "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"

def chat_with_chatgpt(prompt, model="text-davinci-003"):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message

print(chat_with_chatgpt("Say shakespeare was alive today, give me a poem he would write about today's online social media world"))