from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'pages/set/index.html')

def member(request):
    return render(request, 'pages/set/member.html')