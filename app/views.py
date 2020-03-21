from django.shortcuts import render, redirect
from django.http import HttpResponse

# from app.models import Category, Page
# from app.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from datetime import datetime

# Create your views here.

def index(request):
    # category_list = Category.objects.order_by('-likes')[:5]
    # pages_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    # context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    # context_dict['categories'] = category_list
    # context_dict['pages'] = pages_list

    # visitor_cookie_handler(request)

    response = render(request, 'app/index.html', context=context_dict)
    # Return a rendered response to send to the client.
    return response

def login(request):
    # category_list = Category.objects.order_by('-likes')[:5]
    # pages_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    # context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    # context_dict['categories'] = category_list
    # context_dict['pages'] = pages_list

    # visitor_cookie_handler(request)

    response = render(request, 'app/login.html', context=context_dict)
    # Return a rendered response to send to the client.
    return response

def signup(request):
    # category_list = Category.objects.order_by('-likes')[:5]
    # pages_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    # context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    # context_dict['categories'] = category_list
    # context_dict['pages'] = pages_list

    # visitor_cookie_handler(request)

    response = render(request, 'app/signup.html', context=context_dict)
    # Return a rendered response to send to the client.
    return response

def contact(request):
    # category_list = Category.objects.order_by('-likes')[:5]
    # pages_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    # context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    # context_dict['categories'] = category_list
    # context_dict['pages'] = pages_list

    # visitor_cookie_handler(request)

    response = render(request, 'app/contact.html', context=context_dict)
    # Return a rendered response to send to the client.
    return response

def sitemap(request):
    # category_list = Category.objects.order_by('-likes')[:5]
    # pages_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    # context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    # context_dict['categories'] = category_list
    # context_dict['pages'] = pages_list

    # visitor_cookie_handler(request)

    response = render(request, 'app/site-map.html', context=context_dict)
    # Return a rendered response to send to the client.
    return response

def app(request):
    # category_list = Category.objects.order_by('-likes')[:5]
    # pages_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    # context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    # context_dict['categories'] = category_list
    # context_dict['pages'] = pages_list

    # visitor_cookie_handler(request)

    response = render(request, 'app/app.html', context=context_dict)
    # Return a rendered response to send to the client.
    return response
def hospital_map(request):
    # category_list = Category.objects.order_by('-likes')[:5]
    # pages_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    # context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    # context_dict['categories'] = category_list
    # context_dict['pages'] = pages_list

    # visitor_cookie_handler(request)

    response = render(request, 'app/map.html', context=context_dict)
    # Return a rendered response to send to the client.
    return response
def profile(request):
    # category_list = Category.objects.order_by('-likes')[:5]
    # pages_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    # context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    # context_dict['categories'] = category_list
    # context_dict['pages'] = pages_list

    # visitor_cookie_handler(request)

    response = render(request, 'app/profile.html', context=context_dict)
    # Return a rendered response to send to the client.
    return response
def profile_edit(request):
    # category_list = Category.objects.order_by('-likes')[:5]
    # pages_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    # context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    # context_dict['categories'] = category_list
    # context_dict['pages'] = pages_list

    # visitor_cookie_handler(request)

    response = render(request, 'app/edit.html', context=context_dict)
    # Return a rendered response to send to the client.
    return response
def hospital(request, hospital_slug):
    context_dict = {}
    # try:
    #     hospital = Hospital.objects.get(slug=hospital_slug)


    #     context_dict['hospital'] = hospital

    # except Hospital.DoesNotExist:

    #     context_dict['hospital'] = None

    return render(request, 'app/login.html', context=context_dict)

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(
        request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(
        last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1

        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits