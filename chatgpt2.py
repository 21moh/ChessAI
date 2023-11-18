import openai

openai.api_key = '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'

def chat_with_chatgpt(message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt = message,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )  
    answer = response.choice[0].text.strip()
    return answer

print(chat_with_chatgpt("Say shakespeare was alive today, give me a poem he would write about today's online social media world"))
