from django.shortcuts import render

def home(request):
    return render(request, 'avemaria/index.html')

# def about(request):
#     return render(request, 'avemaria/about.html')

def logout(request):
    return render(request, 'avemaria/index.html')

# def handler404(request):
#     return render(request, 'errors/404.html')

