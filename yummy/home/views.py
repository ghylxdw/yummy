from django.shortcuts import render


# Create your views here.
def home(request):
    context = {}

    # print context['user']
    return render(request, 'home/home.html', context)