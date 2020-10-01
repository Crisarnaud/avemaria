from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import UserForm,UserProfileInfoForm
from django.template import RequestContext
from django.db.models import Q

from .models import Book
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login

from django.core.files import File
from io import BytesIO
from django.http import FileResponse, Http404

from datetime import datetime

import pdfkit

# Create your views here.
def index(request):
    books = Book.objects.all()
    search_term = ''
    context = {'books': books, 'search_term': search_term}
    if 'search' in request.GET:
        search_term = request.GET['search']
        books = Book.objects.all().filter(title__icontains=search_term)

    return render(request, 'avemaria/index.html', {'books': books})


def book(request, book_id):
    book = Book.objects.get(pk=book_id)
    return render(request, "avemaria/index.html", {
        "book" : book,
    })

def show_book(request, id):
    books = get_object_or_404(Book, pk=id)

    #     raise Http404('Sorry the post #{} was not found.'.format(id))
    return render(request, 'avemaria/book.html', {'books': books})


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            username = request.POST['username']
            #         firstname = request.POST['first_name']
            #         lastname = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'email' in request.FILES:
                print('found it')
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'avemaria/register.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'avemaria/login.html', {})


def about(request):
    return render(request, 'avemaria/about.html')

def passwd_forgot(request):
    return render(request, 'avemaria/passwd_forgot.html')


def user_profile(request):
    return render(request, 'avemaria/user_profile.html')

@login_required
def invoicepdf(request, d):
    if path.exists('media/profile_pics/%s.pdf'%d)==True:
        return HttpResponseRedirect('media/profile_pics/%s.pdf'%d)
    else:
        inv=cart.objects.filter(Q(ordeno=d)&Q(user=request.user))
        if inv:
            cookie_list = request.COOKIES
            options = {
                'cookie': [
                    ('csrftoken', cookie_list['csrftoken']),
                    ('sessionid', cookie_list['sessionid']),
                ],
                'page-size':'A4',
                'margin-top': '0',
                'margin-right': '0',
                'margin-bottom': '0',
                'margin-left': '0',
                'encoding': 'UTF-16',
            }
            config = pdfkit.configuration(wkhtmltopdf='C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
            pdfkit.from_url(request.get_host()+'%s'%d, 'media/profile_pics/%s.pdf'%d, configuration=config, options=options)
            return HttpResponseRedirect('media/profile_pics/%s.pdf'%d)


# def pdf_viewer(request):
#     return render(request, 'avemaria/lecture.html')
#

#     obj = get_object_or_404(PDF, pk=id)
#
#     path_to_pdf = pdf.url
#     return FileResponse(open('/pdf', 'rb'), content_type='/pdf')
    # pdf_full_path = settings.BASE_DIR + obj.pdf.url
    # with open(pdf_full_path, 'r') as pdf:
    #     response = HttpResponse(pdf.read(), content_type='avemaria/pdf')
    #     response['Content-Disposition'] = 'filename=%s' % obj.pdf.name
    #     return response
    # pdf.closed


# def file_pdf(request):
#     return FileResponse(open('/media/', 'rb'), content_type='/pdf')

    # context = {'books': books}
    # book = Book.objects.get(pk=book_id)
    # pdf = Book.pdf
    # path_to_pdf = pdf.url
    # print('pdf/')
    # return FileResponse(open('/media/pdf', 'rb'), content_type='/pdf')

    # books = Book.objects.all()
    # books = get_object_or_404(Book, pk=pdf)


# the above path_to_pdf is a valid link to my s3 bucket file
# results in a FileNotFound error