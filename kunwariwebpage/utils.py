import os
from openai import OpenAI
from django.conf import settings


# Set OpenAI API Key
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use your fine-tuned model name
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
        #return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"
