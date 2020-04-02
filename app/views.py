from app.models import Donor, Hospital, Story, Booking, Review, User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http.response import JsonResponse

from django.urls import reverse
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as usr_login
from django.contrib.auth.decorators import login_required

from django.db.utils import IntegrityError
from datetime import datetime

import json


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
    context_dict = {}

    # If the user is logged in redirect to the app dashboard
    if request.user.is_authenticated:
        return redirect("app:app")

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        if username is not None:
            if user:
                # Is the account active? It could have been disabled.
                if user.is_active:
                    usr_login(request, user)
                    return JsonResponse(
                        {'success': True, 'message': "Logged in successfully!"})  # redirect(reverse('app:index'))
                else:
                    # An inactive account was used - no logging in!
                    # return HttpResponse("Your account is disabled.")
                    return JsonResponse({'success': False, 'message': "Your account is disabled!"})
            else:
                print(f"Invalid login details: {username}, {password}")
                # return HttpResponse("Invalid login details supplied.")
                return JsonResponse({'success': False, 'message': "The provided login details are incorrect!"})
        else:
            # return render(request, 'app/login.html')
            return JsonResponse({'success': False, 'message': "The provided login details are incorrect!"})
    else:
        return render(request, 'app/login.html')


def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('app:index'))


def signup(request):
    context_dict = {}

    # If the user is logged in redirect to the app dashboard
    if request.user.is_authenticated:
        return redirect("app:app")

    if request.method == 'POST':
        qd = dict(request.POST)
        if 'username' in qd:
            for k, v in qd.items():
                qd[k] = v[0]

            # print(qd)
            new_donor = Donor()

            r = new_donor.new_donor(data=qd)
            # Try to create a new Donor and handle any errors which may occur
            if r['error'] == None:
                return JsonResponse(
                    {'success': True, 'message': "Account was successfully created. You can now log in!"})
            else:
                return JsonResponse({'success': False, 'message': r['error']})

        elif 'hospital_name' in qd:
            for k, v in qd.items():
                qd[k] = v[0]

            new_hopt = Hospital()
            # Try to create a new Hospital and handle any errors which may occur
            try:
                new_hopt.new_hospital(data=qd)
                return JsonResponse(
                    {'success': True, 'message': "Account was successfully created. You can now log in!"})
            except IntegrityError as e:
                return JsonResponse({'success': False, 'message': "This email has already been used!"})

    if request.method == 'GET':
        # Check if GET parameter has been used in the url to show hospital sign up form directly
        hospital = request.GET.get('hospital', '')
        if hospital == "true":
            context_dict['hospital'] = "true"
            response = render(request, 'app/signup.html', context=context_dict)

    else:
        return render(request, 'app/signup.html')

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


@login_required
def app(request):
    context_dict = {}
    # Get 4 most liked stories
    stories = Story.objects.order_by('-likes')[:4]

    # Get all reviews of by the donor
    reviews = Review.objects.all()

    context_dict["stories"] = stories
    context_dict["reviews"] = reviews

    if request.user.is_donor:
        donor = Donor.objects.filter(donor=request.user).first()
        print(donor)
        # context_dict["donor"] = donor
    else:
        hospital = Hospital.objects.filter(hospital=request.user).first()
        context_dict["hospital"] = hospital

    response = render(request, 'app/app.html', context=context_dict)
    # Return a rendered response to send to the client.
    return response


@login_required
def story(request):
    context_dict = {}

    if request.method == 'GET':
        # Check if valid story id has been provided in the url
        story_id = request.GET.get('id', '')
        story = Story.objects.get(pk=story_id)
        if story:
            context_dict["story"] = story
            return render(request, 'app/story.html', context=context_dict)
        else:
            return redirect("app:app")
    else:
        return redirect("app:app")


@login_required
def review(request):
    context_dict = {}

    if request.method == 'GET':
        # Check if valid review id has been provided in the url
        review_id = request.GET.get('id', '')
        review = Review.objects.get(pk=review_id)
        if review:
            context_dict["review"] = review
            return render(request, 'app/review.html', context=context_dict)
        else:
            return redirect("app:app")
    else:
        return redirect("app:app")


@login_required
def hospital_map(request):
    context_dict = {}

    response = render(request, 'app/map.html', context=context_dict)
    # Return a rendered response to send to the client.
    return response


@login_required
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


@login_required
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


@login_required
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


def all_hospitals(request):
    hospitals = Hospital.objects.all()
    # print(hospitals)

    context_dict = {}
    # context_dict["hospitals"] = hospitals
    for h in hospitals:
        # print(h.hospital_id)
        context_dict[h.name] = [h.hospital_id, h.location]
    # print()
    # response = render(request, 'app/map.html', context=context_dict)
    return JsonResponse(context_dict)


def cancel_booking(request):
    print(Booking.objects.all())

    if request.method == 'GET':
        # Check if GET parameter has been used in the url to show hospital sign up form directly
        booking_id = request.GET.get('id', '')
        try:
            booking = Booking.objects.get(pk=booking_id)
            if booking:
                booking.delete()
                return JsonResponse({'success': True, 'message': "The booking has been cancelled successfully!"})
        except:
            return JsonResponse({'success': False, 'message': "Booking with given id does not exist!"})
        # if booking:
        #     booking.delete()
        #     return JsonResponse({'success': True, 'message': "The booking has been cancelled successfully!"})
        # else:
        #     return redirect("app:app")
    else:
        return redirect("app:app")
