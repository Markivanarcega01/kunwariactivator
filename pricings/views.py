from django.shortcuts import render

# Create your views here.
def pricing_list(request):
    return render(request, 'pricings/pricing.html')