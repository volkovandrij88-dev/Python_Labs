from django.shortcuts import render

def home(request):
    context = {'zagolovok': 'Головна', 'text_main': 'Привіт!'}
    return render(request, 'blog/index.html', context)

def about(request):
    context = {'zagolovok': 'Про нас', 'text_other': 'Інфа тут.'}
    return render(request, 'blog/second.html', context)


