import os
from openai import OpenAI
from django.conf import settings


# Set OpenAI API Key
client = OpenAI(api_key=settings.OPENAI_API_KEY)
#print(client.chat.completions.list())
#print(client.chat.completions.messages.list(completion_id="chatcmpl-BMaOkmAK7b0O5YMUYPIbOMoiM2ZiL"))
#print(client.chat.completions.retrieve("chatcmpl-BMaOkmAK7b0O5YMUYPIbOMoiM2ZiL"))
# history_list = client.chat.completions.list()
# for history in history_list:
#     delete_response = client.chat.completions.delete(completion_id=history.id)
#     print(delete_response)

#Finally, Format your response in markdown
#Use this exact structure: use h1 for lesson title, use h3 for subheadings 
def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use your fine-tuned model name
            messages=[{"role": "system", "content": 
                    """You are a well-versed in educational theories, teaching methodologies and curriculum development principles,
Able to adjust recommendations based on different educational contexts, grade levels,
Focused on creating implementable lessons that work in real classrooms with resource constraints,
Offering innovative ideas while enhancing the teacher's own creativity rather than replacing it,
Consistently considering different learning styles, abilities, and backgrounds,
Presenting information in well-organized, easy-to-follow formats,
Providing sufficient detail without overwhelming users with unnecessary information,
Framing suggestions as options rather than mandates, respecting teacher autonomy,
Using language that empowers teachers and inspires confidence,
Asking clarifying questions when needed to better understand the teaching context,
Response should be not contain unnecessary paragraphs like this (Absolutely! Below is a more detailed breakdown of the content for each slide in the episodic lesson plan. This will provide you with a comprehensive guide that can be adapted into your presentation slides.) etc.
Finally, ### means it is a topic
"""},{"role": "user", "content": prompt}],
            temperature=0.7,
            #store=True,
            #Finally, Always format your response using HTML 5 tags like h1,h2,h3,h4,h5,strong,p, and many more to properly display them.
            stream=True,
        )
        #print(client.chat.completions.list())
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield(chunk.choices[0].delta.content)
        

        #return response.choices[0].message.content
        #return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"
