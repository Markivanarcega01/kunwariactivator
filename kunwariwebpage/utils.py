import base64
import os
from openai import OpenAI

import pymupdf as fitz
from docx import Document
from django.conf import settings
import re


# Set OpenAI API Key
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def encode_uploaded_image(image_file):
    """Encodes an InMemoryUploadedFile or TemporaryUploadedFile to base64."""
    return base64.b64encode(image_file.read()).decode("utf-8")

def extract_text_from_docx(docx_file):
    document = Document(docx_file)
    return '\n'.join([para.text for para in document.paragraphs])

def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_txt(file):
    return file.read().decode('utf-8')

def generate_response(prompt, files = None):
    try:
        messages_container = [
            {
                "type":"text",
                "text":prompt
            },
        ]
        
        #change images to files for naming convention
        if files is None:
            pass
        else:
            pattern = re.compile(r'\.(jpeg|jpg|png|pdf|docx|txt)$', re.IGNORECASE)
            for file in files:
                filename = file.name
                match = pattern.search(filename)
                
                if match:
                    ext = match.group(1).lower()
                    if ext in ['jpeg', 'jpg', 'png']:
                        image_base64 = encode_uploaded_image(file)
                        mime_type = file.content_type or "image/jpeg"
                        image_url = f"data:{mime_type};base64,{image_base64}"
                        messages_container.append({
                            "type":"image_url",
                            "image_url":{
                                "url":image_url,
                            }
                        })
                    elif ext == 'pdf':
                        text = extract_text_from_pdf(file)
                        #print(text)
                        messages_container.append({
                            "type":"text",
                            "text":f"Extracted from {file}:\n\n{text}"
                        })
                    elif ext == 'docx':
                        text = extract_text_from_docx(file)
                        #print(text)
                        messages_container.append({
                            "type":"text",
                            "text":f"Extracted from {file}:\n\n{text}"
                        })
                    elif ext == 'txt':
                        text = extract_text_from_txt(file)
                        #print(text)
                        messages_container.append({
                            "type":"text",
                            "text":f"Extracted from {file}:\n\n{text}"
                        })
                else:
                    print(f"{filename} is not a supported type")
                #print(type(filename))
                

                #print(file)
                # image_base64 = encode_uploaded_image(file)
                # mime_type = file.content_type or "image/jpeg"
                # image_url = f"data:{mime_type};base64,{image_base64}"
                # messages_container.append({
                #     "type":"image_url",
                #     "image_url":{
                #         "url":image_url,
                #     }
                # })
            
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
