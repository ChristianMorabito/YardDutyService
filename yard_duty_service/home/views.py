from django.shortcuts import render


def about(request):

    return render(request, 'home/about.html', {'title': 'About'})


def home(request):

    context = {'title': 'Home'}

    return render(request, 'home/home.html', context)
