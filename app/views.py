from app.models import Donor, Hospital, Story, Booking, Review, User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http.response import JsonResponse

from django.urls import reverse
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as usr_login
from django.contrib.auth.decorators import login_required

from django.core.files.storage import FileSystemStorage

from django.db.utils import IntegrityError
from datetime import datetime

import json


# Show Landing page
def index(request):

    context_dict = {}

    response = render(request, 'app/index.html', context=context_dict)
    # Return a rendered response to send to the client.
    return response

# Show Login page
def login(request):
    context_dict = {}

    # If the user is logged in redirect to the app dashboard
    if request.user.is_authenticated:
        return redirect("app:app")

    # Check if the request given is post otherwise just render the page
    if request.method == 'POST':
        # Get the post data from the login form
        username = request.POST["username"]
        password = request.POST["password"]

        # authenticate the user with given data
        user = authenticate(username=username, password=password)
        # If the user exists, continue with the authentication
        if username is not None:
            if user:
                # Is the account active? It could have been disabled.
                if user.is_active:
                    usr_login(request, user)
                    return JsonResponse(
                        {'success': True, 'message': "Logged in successfully!"})
                else:
                    # An inactive account was used - no logging in!
                    return JsonResponse({'success': False, 'message': "Your account is disabled!"})
            else:
                return JsonResponse({'success': False, 'message': "The provided login details are incorrect!"})
        else:
            # return render(request, 'app/login.html')
            return JsonResponse({'success': False, 'message': "The provided login details are incorrect!"})
    else:
        return render(request, 'app/login.html')

# Log out the user
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('app:index'))

# Show sign up view
def signup(request):
    context_dict = {}

    # If the user is logged in redirect to the app dashboard
    if request.user.is_authenticated:
        return redirect("app:app")

    # Check if the request is Post, new user is being registered
    if request.method == 'POST':
        qd = dict(request.POST)

        # Check if it is Donor or Hospital
        if 'username' in qd:
            for k, v in qd.items():
                qd[k] = v[0]

            new_donor = Donor()

            # Create a new donor instance
            r = new_donor.new_donor(data=qd)
            # Handle any errors which may occur
            if r['error'] is None:
                return JsonResponse(
                    {'success': True, 'message': "Account was successfully created. You can now log in!"})
            else:
                return JsonResponse({'success': False, 'message': r['error']})

        elif 'hospital_name' in qd:
            for k, v in qd.items():
                qd[k] = v[0]
            
            # Create a new hospital instance
            new_hosp = Hospital()
            # Handle any errors which may occur
            r = new_hosp.new_hospital(data=qd)
            if r['error'] is None:
                return JsonResponse(
                    {'success': True, 'message': "Account was successfully created. You can now log in!"})
            else:
                return JsonResponse({'success': False, 'message': r['error']})

    # Use this to have a link choosing the Hospital form directly
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

# Show Contact page
def contact(request):

    context_dict = {}

    response = render(request, 'app/contact.html', context=context_dict)
    # Return a rendered response to send to the client.
    return response

# Show Sitemap page
def sitemap(request):

    context_dict = {}

    response = render(request, 'app/site-map.html', context=context_dict)
    # Return a rendered response to send to the client.
    return response

# Show Dashboard page
@login_required
def app(request):
    context_dict = {}

    # Check if the logged in user is Donor or Hospital
    if request.user.is_donor:
        # Get the logged in donor
        donor = Donor.objects.get(pk=request.user.id)
        context_dict["donor"] = donor

        # Get all hospitals
        hospitals = Hospital.objects.all()
        context_dict["hospitals"] = hospitals

        # Get the hospitals which need the donor's blood type
        if donor.notification:
            context_dict["notifications"] = Hospital.objects.filter(notified_types=donor.blood_type)

        # Get 4 most liked stories
        stories = Story.objects.order_by('-likes')[:4]
        context_dict["stories"] = stories

        # get list of stories this donor liked
        context_dict["liked"] = donor.likedStories

        # Get if the donor can donate blood again
        donate = Donor.donate_again(request.user.id)
        if donate:
            context_dict["donate"] = {"donate": "yes"}

        # Get all reviews of by the donor
        reviews = Review.objects.order_by('pk').filter(donor=donor)
        if len(reviews) > 0:
            context_dict["reviews"] = reviews

        # Get bookings of this donor
        bookings = Booking.objects.order_by('appointment').filter(donor=donor)
        if len(bookings) > 0:
            context_dict["bookings"] = bookings

    else:
        # Get the logged in hospital
        hospital = Hospital.objects.get(pk=request.user.id)
        context_dict["hospital"] = hospital
        # Get bookings at this hospital
        bookings = Booking.objects.order_by('appointment').filter(hospital=hospital)
        if len(bookings) > 0:
            context_dict["bookings"] = bookings
        # Get stories written by this hospital
        stories = Story.objects.order_by('-pk').filter(hospital=hospital)
        if len(stories) > 0:
            context_dict["stories"] = stories
        # Get all reviews about this hospital
        reviews = Review.objects.filter(hospital=hospital)
        if len(reviews) > 0:
            context_dict["reviews"] = reviews

    response = render(request, 'app/app.html', context=context_dict)
    # Return a rendered response to send to the client.
    return response


# Show story detail
@login_required
def story(request):
    context_dict = {}

    if request.method == 'GET':
        # Check if valid story id has been provided in the url
        story_id = request.GET.get('id', '')
        story = Story.objects.get(pk=story_id)
        # Check if the user opening the story is donor or hospital
        if request.user.is_donor:
            donor = Donor.objects.get(pk=request.user.id)
            # get ist of storis this donor liked
            context_dict["liked"] = donor.likedStories
        if story:
            context_dict["story"] = story
            return render(request, 'app/story.html', context=context_dict)
        else:
            return redirect("app:app")
    else:
        return redirect("app:app")


# Show review detail
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

# Show the map page
@login_required
def hospital_map(request):
    context_dict = {}

    response = render(request, 'app/map.html', context=context_dict)
    # Return a rendered response to send to the client.
    return response

# Show the profile page
@login_required
def profile(request):
    context_dict = {}

    # Check if the user is donor or hospital
    if request.user.is_donor:
        donor = Donor.objects.get(pk=request.user.id)
        context_dict["donor"] = donor
    else:
        hospital = Hospital.objects.get(pk=request.user.id)
        context_dict["hospital"] = hospital

    response = render(request, 'app/profile.html', context=context_dict)
    # Return a rendered response to send to the client.
    return response


# Show profile editaion and handle the edit of the user details
@login_required
def profile_edit(request):
    context_dict = {}

    # Check if the form has been submitted
    if request.method == 'POST':
        qd = dict(request.POST)
        # check if it s donor or hospital
        if 'username' in qd:
            for k, v in qd.items():
                qd[k] = v[0]
            # get the instance of the donor and update all the data given at the form
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

            for k, v in qd.items():
                qd[k] = v[0]

            # Get the instance of the hospital by its id and update all its fields using the data given by the form
            user = User.objects.get(pk=request.user.id)
            hospital = Hospital.objects.get(pk=request.user.id)

            # Check if this username has been used
            if user.username != qd['hospital_email']:
                user.username = qd['hospital_email']
            try:
                user.save()
            except IntegrityError:
                return JsonResponse({'success': False, 'message': "This email is already used"})

            hospital.name = qd['hospital_name']
            hospital.location = qd['location']
            # Try save the changes
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


# Show the hospital detail page
@login_required
def hospital(request, hospital_slug):
    context_dict = {}
    # Try if there is a hospital with the provided slug
    try:
        hospital = Hospital.objects.get(slug_name=hospital_slug)

        # is the user is a hospital, redirect to the dashboard because hospitals cannot see pages of other hospitals
        if request.user.is_hospital:
            user_hospital = Hospital.objects.get(pk=request.user.id)
            if user_hospital.slug_name == hospital.slug_name:
                return redirect("app:app")

        context_dict['hospital'] = hospital

        donor = Donor.objects.get(pk=request.user.id)
        # Get the stories liked by this donor
        context_dict["liked"] = donor.likedStories

        # Get the stories written by this hospital
        stories = Story.objects.order_by('-pk').filter(hospital=hospital)
        if len(stories) > 0:
            context_dict["stories"] = stories

        # Get all reviews about this hospital
        reviews = Review.objects.order_by('-pk').filter(hospital=hospital)
        if len(reviews) > 0:
            context_dict["reviews"] = reviews

        # Get all the slots provided by this hospital
        booking_slots = Booking.get_slot(hospital.hospital_id)

        if len(booking_slots) > 0:
            context_dict["booking_slots"] = booking_slots

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


# Get information about all the hospitals in giver format of JSON
def all_hospitals(request):
    hospitals = Hospital.objects.all()

    context_dict = {}

    for h in hospitals:
        context_dict[h.name] = [h.hospital_id, h.location, h.slug_name]

    return JsonResponse(context_dict)

# Cancel booking with given id
def cancel_booking(request):
    if request.method == 'GET':
        # Check if GET parameter has been used in the url to show hospital sign up form directly
        booking_id = request.GET.get('id', '')
        # Try if there is a booking with provided id
        try:
            booking = Booking.objects.get(pk=booking_id)
            # If there is such a booking, delete it
            if booking:
                booking.delete()
                return JsonResponse({'success': True, 'message': "The booking has been cancelled successfully!"})
        except:
            return JsonResponse({'success': False, 'message': "Booking with given id does not exist!"})

    else:
        return redirect("app:app")

# Like a story with a given id
def like_story(request):
    # Check if there is get parameter provided
    if request.method == 'GET':
        # Check if GET parameter has been used in the url to show hospital sign up form directly
        story_id = request.GET.get('id', '')
        data = {"story_id": story_id, "donor_id": request.user.id}
        # try to get donor and story of given ids
        try:
            donor = Donor.objects.get(pk=request.user.id)
            story = Story.objects.get(pk=story_id)
            # Decide whether the donor ahs already like this story and perfom like or dislike process accordingly
            if story_id in json.loads(donor.likedStories):
                story.dislike_story(data)
                return JsonResponse({'success': True, 'message': "The story has been successfully disliked!"})
            else:
                story.like_story(data)
                return JsonResponse({'success': True, 'message': "The story has been successfully liked!"})
        except:
            return JsonResponse({'success': False, 'message': "Story with given id does not exist!"})

    else:
        return redirect("app:app")

# Save the review from donor
def write_review(request):
    context_dict = {}

    # Check if the request is of post type
    if request.method == 'POST':
        # Get the informationg from the form in required format
        donor_id = request.POST["donor"]
        hospital_id = request.POST["hospital"]
        data = {'donor': Donor.objects.get(pk=donor_id),
                'hospital': Hospital.objects.get(pk=hospital_id),
                'date': request.POST["time"],
                'review': request.POST["review_text"]}
        # Try to create a new review with given data
        try:
            review = Review()
            review.new_review(data)
            return JsonResponse({'success': True, 'message': "The review has been succesfully published!"})
        except:
            return JsonResponse({'success': False, 'message': "The provided login details are incorrect!"})

    else:
        return redirect("app:app")

# Save the story
def write_story(request):
    context_dict = {}

    # Check if the request is of type post
    if request.method == 'POST':

        # Get the data in required format
        data = {'hospital': Hospital.objects.get(pk=request.user.id),
                    'date': request.POST.get("time"),
                    'story': request.POST.get("story"),
                    'heading': request.POST.get("heading"),
                    'likes': 0}

        # Handle image import
        if request.FILES.get("file") is not None:
            image = request.FILES["file"]
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            uploaded_file_url = filename
            data = {'hospital': Hospital.objects.get(pk=request.user.id),
                    'date': request.POST.get("time"),
                    'story': request.POST.get("story"),
                    'heading': request.POST.get("heading"),
                    'picture': uploaded_file_url,
                    'likes': 0}
        # Try to create a new story
        try:
            story = Story()
            story.new_story(data)
            return JsonResponse({'success': True, 'message': "The review has been succesfully published!"})
        except:
            return JsonResponse({'success': False, 'message': "The provided login details are incorrect!"})

    else:
        return redirect("app:app")

# Get all reviews - used to load new data to the page without 
# a need of refreshing the webpage after new review has been written
def get_new_reviews(request):
    context_dict = {}
    if request.method == 'GET':
        # Check if GET parameter has been used in the url to show hospital sign up form directly
        hospital_id = request.GET.get('hospital_id', '')
        # Get the data in formatted json
        try:
            hospital = Hospital.objects.get(pk=hospital_id)
            reviews = Review.objects.order_by('-pk').filter(hospital=hospital).values()
            data = list(reviews)
            return JsonResponse({'success': True, 'data':data, 'message': "The reviews have been retrieved successfully!"})
        except:
            return JsonResponse({'success': False, 'message': "A hospital with given id does not exist!"})
    else:
        return redirect("app:app")

# Get all stories - used to load new data to the page without 
# a need of refreshing the webpage after new story has been written
def get_new_stories(request):
    context_dict = {}
    if request.method == 'GET':
        # Check if GET parameter has been used in the url to show hospital sign up form directly
        hospital_id = request.GET.get('hospital_id', '')
        try:
            hospital = Hospital.objects.get(pk=hospital_id)
            stories = Story.objects.order_by('-pk').filter(hospital=hospital).values()
            data = list(stories)
            return JsonResponse({'success': True, 'data':data, 'message': "The reviews have been retrieved successfully!"})
        except:
            return JsonResponse({'success': False, 'message': "A hospital with given id does not exist!"})
    else:
        return redirect("app:app")

# Set up a blood type which the hospital needs
def notify_donors(request):
    if request.method == 'POST' and request.user.is_hospital:
        # Check if GET parameter has been used in the url to show hospital sign up form directly
        blood_type = request.POST['type']
        # Try to save the required blood type 
        try:
            hospital = Hospital.objects.get(pk=request.user.id)
            hospital.notified_types = blood_type
            hospital.save()
            return JsonResponse({'success': True, 'message': "The donors have been successfully notified!"})
        except:
            return JsonResponse({'success': False, 'message': "A hospital with given id does not exist!"})
    else:
        return redirect("app:app")

# Create a new appointment
def book_appointment(request):
    # check if the request is of type post and if the user is Donor
    if request.method == 'POST' and request.user.is_donor:
        
        # get the required format of the data
        appointment = request.POST['time']
        donor_id = request.POST['donor']
        hospital_id = request.POST['hospital']
        data = {'hospital': Hospital.objects.get(pk=hospital_id),
                'donor': Donor.objects.get(pk=donor_id),
                'appointment': request.POST.get("time")}
        # Try to create a new Booking with provided data
        try:
            booking = Booking()
            booking.new_appointment(data)
            return JsonResponse({'success': True, 'message': "The appointment has been created successfully"})
        except:
            return JsonResponse({'success': False, 'message': "You might have booking at this time at different hospital. Please, try different slot."})
    else:
        return redirect("app:app")