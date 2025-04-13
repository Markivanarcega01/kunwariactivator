import os
from django.conf import settings
from django.http.response import StreamingHttpResponse
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import generate_response
from django.contrib.auth import get_user_model
import json
from pptx import Presentation
from pptx.util import Inches
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

def generate_pptx(request):
    prs = Presentation()
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            message = data['message']
            parts = re.split(r'(?=\b(?:[1-9]|1[0-9]|2[0-3])\. )', message)
            blank_slide_layout = prs.slide_layouts[0]
            save_directory = os.path.join(settings.BASE_DIR, 'media')
            for part in parts:
                slide = prs.slides.add_slide(blank_slide_layout)
                left = Inches(3)
                top = Inches(1)
                width = Inches(4)
                height = Inches(1)
                txBox = slide.shapes.add_textbox(left, top, width, height)
                tf = txBox.text_frame
                p = tf.add_paragraph()
                p.text = part
            prs.save(os.path.join(save_directory,"output.pptx"))
            return JsonResponse({"message": message}, status=200)
    except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def chatbot_view(request):
        memory = []
        try:
            if request.method == "POST":
                data = json.loads(request.body)
                message = data['message']
                message += """
                1. Create analogies and laymanized examples to teach the topics and lessons.
2. Create Detailed Teaching and Learning Games, Activities, and Exercises aligned with the created analogies and laymanized examples that teaches the topics and lessons.
3. Create detailed gamified quizzes and exams aligned with the created analogies and
laymanized examples that teaches the topics and lessons.
4. Generate Morals or Values arc that you want the students to learn.
5. Create a story or premise based on the Narrative and the analogies and the laymanized examples that teaches the topics and lessons.
6. Highlight the conflict in the given story/presents the challenges/mission of the protagonists.
7. Transforms the Learning Objectives into Game Mechanics which applies to the narrative/story, Objective 1: Learning Objectives and Verb-based Game Mechanics hybrid related to the story,
Objective 2: Another learning goal tied to the narrative arc.
8. Killer: Create Specific activities for competitive players.
9. Achiever: Create Specific activities Focused on accomplishment-based challenges.
10. Explorer: Create Specific activities Engages with discovery-based elements.
11. Socializer: Create Specific activities Collaborative and team-oriented tasks.
12. Tailor the games according to applicable skills.
13. Generate Props, Manipulatives, and Learning Materials: Suggestions for physical or virtual game materials.
14. Generate Background/Set: Virtual or physical space design ideas.
15. Generate Costume/Attire: Suggestions for character costumes or thematic attire.
16. Generate Dance/Music/SFX: Tailored sound design suggestions for immersion.
17. Generate Food, Taste, and Scents: Olfactory enhancements for deeper engagement.
18. Assign roles to students, teachers, and NPCs in alignment with the narrative/story.
19. Create a final stage with a BOSS challenge that integrates all learning outcomes and analogies.
20. Generated discussion questions to facilitate meaninful reflection.
21. Generate answers to this question from real world scenarios or United Nations Sustainable Development Group.
22. Generate a challenge from real world scenarios or United Nations Sustainable Development Group that students can solve from what they’ve learned from the topic - make this PISA creative thinking format.
23. Generate Achievements based on performance and engagement.
24. Create Game Design Document.
25. Create Facilitator’s Script.
                """
                #data = request.POST.get("prompt")
                response = StreamingHttpResponse(generate_response(message), status=200, content_type='text/plain')
                #return render(request, "kunwariwebpage/index.html", {"response": 'response'})
                return response
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        return JsonResponse({"error": "Invalid request"}, status=400)
