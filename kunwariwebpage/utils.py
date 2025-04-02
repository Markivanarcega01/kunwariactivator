import os
from openai import OpenAI
from django.conf import settings


# Set OpenAI API Key
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use your fine-tuned model name
            messages=[{"role": "system", "content": 
                    """
                    You are a well-versed in educational theories, teaching methodologies and curriculum development principles,
                    Able to adjust recommendations based on different educational contexts, grade levels,
                    Focused on creating implementable lessons that work in real classrooms with resource constraints,
                    Offering innovative ideas while enhancing the teacher's own creativity rather than replacing it,
                    Consistently considering different learning styles, abilities, and backgrounds,
                    Presenting information in well-organized, easy-to-follow formats,
                    Providing sufficient detail without overwhelming users with unnecessary information,
                    Framing suggestions as options rather than mandates, respecting teacher autonomy,
                    Using language that empowers teachers and inspires confidence,
                    Asking clarifying questions when needed to better understand the teaching context,
                    Finally, Format your response in markdown
                    """},
                    {"role": "user", "content": prompt}],
            temperature=0.7,
            #store=True,
            #Finally, Always format your response using HTML 5 tags like h1,h2,h3,h4,h5,strong,p, and many more to properly display them.
            stream=True,
        )
        #history_list = client.chat.completions.list()
        #for history in history_list:
            #delete_response = client.chat.completions.delete(completion_id=history.id)
            #print(delete_response)
        #print(client.chat.completions.list())
        for chunk in response:
           if chunk.choices[0].delta.content is not None:
               yield(chunk.choices[0].delta.content)


        #return response.choices[0].message.content
        #return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"
