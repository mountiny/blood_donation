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
                        {'success': True, 'message': "Logged in successfully!"})
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
    
    # Check if the logged in user is Donor or Hospital
    if request.user.is_donor:
        # Get the logged in donor
        donor = Donor.objects.get(pk=request.user.id)
        context_dict["donor"] = donor

        # Get 4 most liked stories
        stories = Story.objects.order_by('-likes')[:4]
        context_dict["stories"] = stories

        # Get all reviews of by the donor
        reviews = Review.objects.filter(donor=donor)
        if len(reviews) > 0:
            context_dict["reviews"] = reviews
        
        # Get bookings of this donor
        bookings = Booking.objects.filter(donor=donor)
        if len(bookings) > 0:
            context_dict["bookings"] = bookings

    else:
        # Get the logged in hospital
        hospital = Hospital.objects.get(pk=request.user.id)
        context_dict["hospital"] = hospital
        # Get bookings at this hospital
        bookings = Booking.objects.filter(hospital=hospital)
        if len(bookings) > 0:
            context_dict["bookings"] = bookings
        # Get stories written by this hospital
        stories = Story.objects.filter(hospital=hospital)
        if len(stories) > 0:
            context_dict["stories"] = stories
        # Get all reviews about this hospital
        reviews = Review.objects.filter(hospital=hospital)
        if len(reviews) > 0:
            context_dict["reviews"] = reviews
        

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

    context_dict = {}

    if request.user.is_donor:
        donor = Donor.objects.get(pk=request.user.id)
        context_dict["donor"] = donor

    else:
        hospital = Hospital.objects.get(pk=request.user.id)
        context_dict["hospital"] = hospital

    response = render(request, 'app/profile.html', context=context_dict)
    # Return a rendered response to send to the client.
    return response


@login_required
def profile_edit(request):

    context_dict = {}

    if request.method == 'POST':
        qd = dict(request.POST)
        if 'username' in qd:
            for k, v in qd.items():
                qd[k] = v[0]
            user = User.objects.get(pk=request.user.id)
            donor = Donor.objects.get(pk=request.user.id)

            # Check if this username has been used
            if user.username != qd['email']:
                user.username = qd['email']
            try:
                user.save()
            except IntegrityError as e:
                return JsonResponse({'success': False, 'message': "This email is already used"})

            user.first_name = qd['first_name']
            user.last_name = qd['last_name']

            donor.nickname = qd['username']
            donor.birth = (qd['birthday'])
            donor.age = donor.get_age(donor.birth)

            donor.address = qd['city']
            donor.height = qd['height']
            donor.weight = qd['weight']
            if qd['notification'] == "true":
                donor.notification = True
            else:
                donor.notification = False

            donor.blood_type = qd['blood_type']
            # self.notification = data['notification']

            # Try to create a save the changes
            try:
                user.save()
                donor.save()
                return JsonResponse({'success': True, 'message': "Updated successfully!"})
            except IntegrityError:
                return JsonResponse({'success': False, 'message': "This is already used"})
            except:
                return JsonResponse({'success': False, 'message': "Something went wrong"})
            

        elif 'hospital_name' in qd:
            print("hejhola")
            for k, v in qd.items():
                qd[k] = v[0]

            user = User.objects.get(pk=request.user.id)
            hospital = Hospital.objects.get(pk=request.user.id)

            # Check if this username has been used
            if user.username != qd['hospital_email']:
                user.username = qd['hospital_email']
            try:
                user.save()
            except IntegrityError:
                return JsonResponse({'success': False, 'message': "This email is already used"})
            print(qd['location'])
            hospital.name = qd['hospital_name']
            hospital.location = qd['location']
            # self.notified_types = data['notif_types']

            # Try to create a save the changes
            try:
                user.save()
                hospital.save()
                return JsonResponse(
                    {'success': True, 'message': "Updated successfully!"})
            except IntegrityError as e:
                return JsonResponse({'success': False, 'message': "This email has already been used!"})
            except:
                return JsonResponse({'success': False, 'message': "Something went wrong"})


    if request.user.is_donor:
        donor = Donor.objects.get(pk=request.user.id)
        context_dict["donor"] = donor

    else:
        hospital = Hospital.objects.get(pk=request.user.id)
        context_dict["hospital"] = hospital

    response = render(request, 'app/profile_edit.html', context=context_dict)
    # Return a rendered response to send to the client.
    return response


@login_required
def hospital(request, hospital_slug):
    context_dict = {}
    try:
        hospital = Hospital.objects.get(slug_name=hospital_slug)

        if request.user.is_hospital:
            user_hospital = Hospital.objects.get(pk=request.user.id)
            if user_hospital.slug_name == hospital.slug_name:
                return redirect("app:app")

        context_dict['hospital'] = hospital

        stories = Story.objects.order_by('-pk').filter(hospital=hospital)
        if len(stories) > 0:
            context_dict["stories"] = stories
        # Get all reviews about this hospital
        reviews = Review.objects.order_by('-pk').filter(hospital=hospital)
        if len(reviews) > 0:
            context_dict["reviews"] = reviews

        return render(request, 'app/hospital.html', context=context_dict)

    except Hospital.DoesNotExist:

        return redirect("app:app")


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
        context_dict[h.name] = [h.hospital_id, h.location, h.slug_name]
    # print()
    # response = render(request, 'app/map.html', context=context_dict)
    return JsonResponse(context_dict)


def cancel_booking(request):

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

    else:
        return redirect("app:app")


def write_review(request):
    context_dict = {}

    if request.method == 'POST':
        print(request.POST)
        donor_id = request.POST["donor"]
        hospital_id = request.POST["hospital"]
        data = {'donor': Donor.objects.get(pk=donor_id),
                'hospital': Hospital.objects.get(pk=hospital_id),
                'date': request.POST["time"],
                'review': request.POST["review_text"]}

        review = Review()
        review.new_review(data)
        try: 
            # review.new_review(data)
            return JsonResponse({'success': True, 'message': "The review has been succesfully published!"})
        except:
            return JsonResponse({'success': False, 'message': "The provided login details are incorrect!"})

    else:
        return redirect("app:app")

def get_new_reviews(request):
    context_dict = {}
    if request.method == 'GET':
        # Check if GET parameter has been used in the url to show hospital sign up form directly
        hospital_id = request.GET.get('hospital_id', '')
        try:
            hospital = Hospital.objects.get(pk=hospital_id)
            reviews = Review.objects.order_by('-pk').filter(hospital=hospital).values()
            data = list(reviews)
            return JsonResponse({'success': True, 'data':data, 'message': "The reviews have been retrieved successfully!"})
        except:
            return JsonResponse({'success': False, 'message': "A hospital with given id does not exist!"})
    else:
        return redirect("app:app")

def notify_donors(request):
    context_dict = {}
    if request.method == 'POST' and request.user.is_hospital:
        # Check if GET parameter has been used in the url to show hospital sign up form directly
        blood_type = request.POST['type']
        try:
            hospital = Hospital.objects.get(pk=request.user.id)
            hospital.notified_types = blood_type
            hospital.save()
            return JsonResponse({'success': True, 'message': "The donors have been successfully notified!"})
        except:
            return JsonResponse({'success': False, 'message': "A hospital with given id does not exist!"})
    else:
        return redirect("app:app")