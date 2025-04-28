import os
from django.conf import settings
from django.http.response import StreamingHttpResponse
from django.shortcuts import redirect, render
from django.http import FileResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import generate_response
from django.contrib.auth import get_user_model
import json
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE
import re


def index(request):
    if 'user' in request.session:
        db = get_user_model()
        current_user = request.session['user']
        isUserAdmin = db.objects.filter(username = current_user, is_superuser = 1).exists()
        params = {'current_user': current_user, "isAdmin": isUserAdmin}
        return render(request, 'kunwariwebpage/index.html', {"params":params})
    else:
        return redirect('login')


#def register(request):
#    return render(request, 'kunwariwebpage/registration.html')

#def forgotpassword(request):
#    return render(request, 'kunwariwebpage/forgotpass.html')

def emu_to_inches(emu):
    return emu / 914400

@csrf_exempt
def chatbot_view(request):
        memory = []
        try:
            if request.method == "POST":
                data = json.loads(request.body)
                message = data['message']
                message += """
Create lessons - Automatically create analogies and laymanized examples to teach the topics and lessons

Create teaching and learning activities - Automatically Create Detailed Teaching and learning Games, Activities, and Exercises aligned with the created analogies and laymanized examples that teach the topics and lessons

Create assessments - Automatically create detailed gamified quizzes and exams aligned with the created analogies and laymanized examples that teaches the topics and lessons

Key moral lesson/values(Narrative) - Automatically generate the Morals or Values arc that you want the students to learn.

Key Story/Premise - Automatically Create a story or premise based on the Narrative and the analogies and the laymanized examples that teaches the topics and lessons.

Key Plot/Conflict/Obstacle - Highlight the conflict in the given story/presents the challenges/mission of the protagonists. 

Learning Objectives (Bloom Verb-Based) to Verb-Based Game Mechanics - Automatically transforms the Learning Objectives into Game Mechanics that apply to the narrative/story. Objective 1: Learning Objectives and Verb-based Game Mechanics hybrid related to the story. Objective 2: Another learning goal tied to the narrative arc.

Player Types (Segmentation) - Killer: Automatically Create Specific activities for competitive players.  Achiever: Automatically Create Specific activities Focused on accomplishment-based challenges. Explorer: Automatically creates specific activities Engages with discovery-based elements. Socializer: Automatically Create Specific Activities Collaborative and team-oriented tasks.

Life Skills, Soft Skills, Creative Skills, 5 C’s of 21st-century learning Application - Automatically tailor the games according to applicable skills. 

Key Resources - Automatically generate the following: Props, Manipulatives, and Learning Materials: Suggestions for physical or virtual game materials. Background/Set: Virtual or physical space design ideas. Costume/Attire: Suggestions for character costumes or thematic attire. 

Activities - Automatically generate the following: Dance/Music/SFX: Tailored sound design suggestions for immersion. Food, Taste, and Scents: Olfactory enhancements for deeper engagement.

Student/Teacher Roles (Kalaro)  - Assigns roles to students, teachers, and NPCs in alignment with the narrative/story.

Reflection and Discussion - Discussion Questions: Auto-generated to facilitate meaningful reflection. 

Main Challenge (Summative Assessment)  - Create a final stage with a BOSS challenge that integrates all learning outcomes and analogies.

What’s In It For You?/ Why is this relevant? - Automatically generate answers to this question from real-world scenarios or UN SDG 

Bonus Challenge - Automatically generate a challenge from real-world scenarios or UN SDG that students can solve from what they’ve learned from the topic - MAKE THIS PISA CREATIVE THINKING FORMAT 

Rewards and Badges - Automatically unlock Achievements based on performance and engagement.

Do not forgot to put <hr> to separate the topics
"""
#Finally, Format your response in markdown
#Use this exact structure: use h1 for lesson title, use h3 for the each dashed line
                #try concatenating the message with the memory and ask another question
                #data = request.POST.get("prompt")
                response = StreamingHttpResponse(generate_response(message), status=200, content_type='text/plain')
                #return render(request, "kunwariwebpage/index.html", {"response": 'response'})
                return response
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def generate_episodes(request):
     try:
        if request.method == "POST":
            data = json.loads(request.body)
            #Message should be the response of the bot + the Episodes
            message = data['message']
            message += """Please transform the lesson plan above following the format of Episodes:
Episode 1: Gamified Lessons - automatically create slides from lesson modules.
Episode 2: Gamified Teaching and Learning Activities - Create slides for interactive activities. 
Episode 3: Gamified Assessments - Create slides for narrative-based assessments. 
Repeat as needed for further episodes -  Tailored lessons, activities, and assessments in sequence.
Do not forgot to put <hr> to separate the topics
            """
            response = StreamingHttpResponse(generate_response(message), status=200, content_type='text/plain')
            return response
     except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
     return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def generate_content(request):
     try:
        if request.method == "POST":
            data = json.loads(request.body)
            message = data['message']
            message += """Please generate detailed content for the Episode slides above.
Do not forgot to put <hr> to separate the topics
            """
            response = StreamingHttpResponse(generate_response(message), status=200, content_type='text/plain')
            return response
     except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
     return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def generate_facilitator_script(request):
     try:
        if request.method == "POST":
            data = json.loads(request.body)
            message = data['message']
            message += """Please generate a complete facilitator script for the Episode slides above.
Do not forgot to put <hr> to separate the topics 
            """
            response = StreamingHttpResponse(generate_response(message), status=200, content_type='text/plain')
            return response
     except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
     return JsonResponse({"error": "Invalid request"}, status=400)


def generate_pptx(request):
    prs = Presentation()
    dimension_width = emu_to_inches(prs.slide_width)
    dimension_height = emu_to_inches(prs.slide_height)
    left_offset = 1
    top_offset = 2
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            message = data['message']
            #parts = re.split(r'(?=\b(?:[1-9]|1[0-9]|2[0-3])\. )', message)
            #parts = re.split(r'<h3>', message)
            fileName = data['filename']
            parts = re.split('<hr>', message)
            blank_slide_layout = prs.slide_layouts[6]
            #save_directory = os.path.join(settings.BASE_DIR, 'media')
            #save_directory = os.path.join(os.path.expanduser("~"),"Downloads")
            # for part in parts:
            #     trim_part = re.sub(r'<[^>]+>', '', part)
            #     slide = prs.slides.add_slide(blank_slide_layout)
            #     left = Inches(left_offset)
            #     top = Inches(top_offset)
            #     width = Inches(dimension_width - 2)
            #     height = Inches(dimension_height - 1)
            #     txBox = slide.shapes.add_textbox(left, top, width, height)
            #     tf = txBox.text_frame
            #     tf.word_wrap = True
            #     p = tf.add_paragraph()
            #     #p.font.size = Pt(20)
            #     p.text = trim_part
            #     #tf.fit_text()
            # prs.save(os.path.join(settings.MEDIA_ROOT,fileName))
            # return JsonResponse({"message": "File generated", "filename":fileName}, status=200)
        
            #For testing
            """
            Find the HTML tags =  r'<(h[1-3]|p)>(.*?)</\1>', ['h4', 'Key Plot/Conflict/Obstacle']
            Use the index[0] as indicator
                If tag is h1,h2,h3 use layout[5] Title only
                If tag is h4,h5,h6 use layout[1] Title and content
                If tag is p, insert it to layout[1]
            Finally, trim each sentence before inserting to pptx
            """
            #pattern = r'<(h[1-6]|p)>(.*?)</\1>'
            pattern = r'<([a-zA-Z][a-zA-Z0-9]*)[^>]*>(.*?)</\1>'
            title_slide = prs.slides.add_slide(prs.slide_layouts[0])
            run_once = True
            for part in parts:
                slide = prs.slides.add_slide(prs.slide_layouts[1])
                content_placeholder = slide.placeholders[1]
                matches = re.findall(pattern, part) #[('h1', 'Title One'), ('p', 'This is a paragraph.'), ('h2', 'Subtitle'), ('h3', 'Section')]
                #print(matches)
                for i in matches: 
                    print(i)
                    if run_once:
                         title_slide.shapes.title.text = i[1]
                         run_once = False
                    #['h4', 'Key Plot/Conflict/Obstacle']
                    if i[0] in ['h1','h2', 'h3', 'h4', 'h5', 'h6']:
                        #print('Title Match')
                        slide.shapes.title.text = i[1]
                        
                    #elif match[0] in ['h4', 'h5', 'h6', 'p']:
                    # elif i[0] in ['h4', 'h5', 'h6']:
                    #     #slide = prs.slides.add_slide(prs.slide_layouts[1])
                    #     print('Subheading match')
                    #     slide.shapes.title.text = i[1]
                    else:
                        trim_part = re.sub(r'<[^>]+>', '', i[1])
                        content_placeholder.text = trim_part
                        

            prs.save(os.path.join(settings.MEDIA_ROOT,fileName))
            return JsonResponse({"message": "File generated", "filename": fileName}, status=200)
              
    except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
def download_from_media(request, filename):
     file_path = os.path.join(settings.MEDIA_ROOT, filename)
     try:
        return FileResponse(open(file_path,'rb'),as_attachment=True, filename=filename)
     except:
        raise Http404("File not found")
