from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import generate_response

def index(request):
    context = {
        'name': 'Mark Ivan Arcega',
    }
    return render(request, 'kunwariwebpage/index.html', context)


#def register(request):
#    return render(request, 'kunwariwebpage/registration.html')

#def forgotpassword(request):
#    return render(request, 'kunwariwebpage/forgotpass.html')



@csrf_exempt
def chatbot_view(request):
        try:
            if request.method == "POST":
                data = request.POST.get("prompt")
                response = generate_response(data)
                return render(request, "kunwariwebpage/index.html", {"response": response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        return JsonResponse({"error": "Invalid request"}, status=400)
