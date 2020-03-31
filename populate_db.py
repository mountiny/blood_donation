import os
import string

import random
from datetime import datetime

import django
import pytz

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blood_donation.settings')

django.setup()
from app.models import *

def create_donor():
    data = {
        'username': ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randrange(3, 7))),
        'first_name': ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randrange(3, 7))),
        'last_name': ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randrange(5, 10))),
        'password': "a",
        'email': ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randrange(3, 5))) + "gmail.com",
        'birthday': str(random.randrange(1950, 2000)) + "-" + str(random.randrange(1, 12)) +"-" +str(random.randrange(1, 28)),
        'telephone': random.randrange(100000000, 999999999),
        'city': ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randrange(10, 20))),
        'height': random.randrange(150, 200),
        'weight': random.randrange(60, 90),
        'blood_type': random.choice(["A+", "A-", "B+", "B-", "AB+", "AB-", "0+", "0-"]),
        'notification': random.choice([True, False])
    }
    donor = Donor()
    donor.new_donor(data)
    return donor


def create_hospital():
    h = "Hospital" + ''.join(random.choice(string.ascii_uppercase) for _ in range(5))
    data = {
        'username': h.lower(),
        'hospital_password': "a",
        'hospital_email': h.lower() + "gmail.com",
        'hospital_name': h[:-5] + " " + h[-5:],
        'location': "Location" + ''.join(random.choice(string.ascii_uppercase) for _ in range(3)),
        'notif_types': random.choice(["A+", "A-", "B+", "B-", "AB+", "AB-", "0+", "0-"])
    }
    hospital = Hospital()
    hospital.new_hospital(data)

    return hospital


def create_review(donor, hospital):
    data = {
        "date": datetime.date(random.randrange(2005, 2019), random.randrange(1, 12), random.randrange(1, 28)),
        "review": ''.join(random.choice(string.ascii_lowercase) for _ in range(100, 150)),
        "donor": donor,
        "hospital": hospital
    }
    review = Review()
    review.new_review(data)
    return review


def create_story(hospital=None):
    data = {
        'hospital': hospital,
        'date': datetime.date(random.randrange(2005, 2019), random.randrange(1, 12), random.randrange(1, 28)),
        'heading': 'This is heading',
        'story': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Vivamus ac leo pretium faucibus. Maecenas sollicitudin. Pellentesque arcu. Maecenas aliquet accumsan leo. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Praesent id justo in neque elementum ultrices. Integer in sapien. Mauris dolor felis, sagittis at, luctus sed, aliquam non, tellus. Phasellus rhoncus. Nulla non lectus sed nisl molestie malesuada. Morbi leo mi, nonummy eget tristique non, rhoncus non leo. Etiam quis quam. Nunc auctor. Fusce dui leo, imperdiet in, aliquam sit amet, feugiat eu, orci. Pellentesque ipsum. Etiam posuere lacus quis dolor. Integer rutrum, orci vestibulum ullamcorper ultricies, lacus quam ultricies odio, vitae placerat pede sem sit amet enim. Pellentesque pretium lectus id turpis.',#''.join(random.choice(string.ascii_lowercase) for _ in range(100, 150)),
        'likes': random.randrange(0, 20),
        'picture': None
    }
    story = Story()
    story.new_story(data)
    return data


def create_booking(donor, hospital):
    random_date = datetime.datetime(2020,
                           random.randrange(4, 12),  # month
                           random.randrange(1, 28),  # day
                           random.randrange(9, 16),  # hour
                           random.choice([00, 15, 30, 45]),  # min
                           tzinfo=pytz.UTC)  # sec
    data = {
        "donor" : donor,
        "hospital": hospital,
        "appointment": random_date
    }
    book = Booking()
    book.new_appointment(data)
    return book


def populate():
    for _ in range(5):
        create_donor()
    for _ in range(3):
        create_hospital()

    # get donors and hospital from database
    donors = Donor.objects.all()
    hospitals = Hospital.objects.all()

    # add some stories
    for i in range(len(hospitals)):
        for _ in range(3):
            create_story(hospital=hospitals[i])

    # add reviews
    for i in donors:
        create_review(i, hospitals[random.randrange(0, len(hospitals))])

    # add bookings
    for d in donors:
        create_booking(d,hospitals[random.randrange(0, len(hospitals))])


# Start execution here!
if __name__ == '__main__':
    print('Starting population script...')
    populate()
