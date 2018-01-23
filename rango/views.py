from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    # chapter 4, remove the following line
    # return HttpResponse("Rango says here is the about page. <br/> <a href='/rango/'>Index</a>")
    #replace with a pointer to the about.html template
    return render(request, 'rango/about.html',{})