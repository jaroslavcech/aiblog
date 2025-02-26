from openai import OpenAI
client = OpenAI(api_key='sk-proj-....')

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
    {
        "role": "developer",
        "content": [
            {
                "type": "text",
                "text": "You are a helpful assistant that answers programming questions in the style of a southern belle from the southeast United States."
            }
        ]
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Are semicolons optional in JavaScript?"
            }
        ]
    }
])

print(completion.choices[0].message)
