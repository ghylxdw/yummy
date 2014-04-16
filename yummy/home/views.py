from django.shortcuts import render


# Create your views here.
def home(request):
    context = {}
    if request.user.is_authenticated():
        context['user'] = request.user
    return render(request, 'home/home.html', context)