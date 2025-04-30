import openai
import time

from openai import OpenAI

client = OpenAI(
  api_key="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"
)

def generate_haiku(prompt):
    max_retries = 3
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                store=True,
                messages=[{"role": "user", "content": prompt}]
            )
            return completion.choices[0].message.content
        except openai.RateLimitError as e:
            print(f"RateLimitError: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                print("Max retries reached.  Please check your OpenAI account and usage.")
                return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

haiku = generate_haiku("write a haiku about ai")

if haiku:
    print(haiku)