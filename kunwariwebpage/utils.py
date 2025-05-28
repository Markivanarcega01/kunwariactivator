import base64
import os
from openai import OpenAI
from django.conf import settings


# Set OpenAI API Key
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def encode_uploaded_image(image_file):
    """Encodes an InMemoryUploadedFile or TemporaryUploadedFile to base64."""
    return base64.b64encode(image_file.read()).decode("utf-8")

def generate_response(prompt, images):
    try:
        messages_container = [
            {
                "type":"text",
                "text":prompt
            },
        ]
        
        for image in images:
            image_base64 = encode_uploaded_image(image)
            mime_type = image.content_type or "image/jpeg"
            image_url = f"data:{mime_type};base64,{image_base64}"
            messages_container.append({
                "type":"image_url",
                "image_url":{
                    "url":image_url,
                }
            })
            
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use your fine-tuned model name
            messages=[
                {"role": "system", "content": 
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
"""},
    {"role": "user", "content": messages_container}],
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
        #print(messages_container)
    except Exception as e:
        return f"Error: {str(e)}"
