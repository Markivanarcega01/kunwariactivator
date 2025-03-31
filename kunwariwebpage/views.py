from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import generate_response

def index(request):
    if 'user' in request.session:
        current_user = request.session['user']
        param = {'current_user': current_user}
        return render(request, 'kunwariwebpage/index.html', param)
    else:
        return redirect('login')


#def register(request):
#    return render(request, 'kunwariwebpage/registration.html')

#def forgotpassword(request):
#    return render(request, 'kunwariwebpage/forgotpass.html')



@csrf_exempt
def chatbot_view(request):
        memory = []
        try:
            if request.method == "POST":
                data = request.POST.get("prompt")
                response = generate_response(data+
                                             """
                                             1. Create analogies and laymanized examples to teach the topics and lessons.
                                             2. Create Detailed Teaching and Learning Games, Activities, and Exercises aligned with the created analogies and
                                                laymanized examples that teaches the topics and lessons
                                             3. Create detailed gamified quizzes and exams aligned with the created analogies and
                                                laymanized examples that teaches the topics and lessons
                                             4. Generate Morals or Values arc that you want the students to learn
                                             5. Create a story or premise based on the Narrative and the analogies and the laymanized examples that
                                                teaches the topics and lessons.
                                             6. Highlight the conflict in the given story/presents the challenges/mission of the protagonists.
                                             7. Automatically transforms the Learning Objectives into Game Mechanics which applies to the narrative/story.
                                             7.1. Objective 1: Learning Objectives and Verb-based Game Mechanics hybrid related to the story.
                                             7.2. Objective 2: Another learning goal tied to the narrative arc.
                                             """)
                return render(request, "kunwariwebpage/index.html", {"response": response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        return JsonResponse({"error": "Invalid request"}, status=400)
