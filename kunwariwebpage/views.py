from django.http.response import StreamingHttpResponse
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import generate_response
from django.contrib.auth import get_user_model
import json

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



@csrf_exempt
def chatbot_view(request):
        memory = []
        try:
            if request.method == "POST":
                data = json.loads(request.body)
                message = data['message']
                #data = request.POST.get("prompt")
                response = StreamingHttpResponse(generate_response(message), status=200, content_type='text/plain')
                #return render(request, "kunwariwebpage/index.html", {"response": 'response'})
                return response
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        return JsonResponse({"error": "Invalid request"}, status=400)
