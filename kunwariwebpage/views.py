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
                                """
                #try concatenating the message with the memory and ask another question
                #data = request.POST.get("prompt")
                response = StreamingHttpResponse(generate_response(message), status=200, content_type='text/plain')
                #return render(request, "kunwariwebpage/index.html", {"response": 'response'})
                return response
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        return JsonResponse({"error": "Invalid request"}, status=400)
