from openai import OpenAI

client = OpenAI()

resp = client.responses.create(
    model="gpt-4.1-mini",
    input="Say OK in one word."
)

print(resp.output_text)
