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
        'first': ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randrange(3, 7))),
        'last': ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randrange(5, 10))),
        'pword': "a",
        'email': ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randrange(3, 5))) + "gmail.com",
        'birth': datetime.date(random.randrange(1950, 2000), random.randrange(1, 12), random.randrange(1, 28)),
        'phone': random.randrange(100000000, 999999999),
        'address': ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randrange(10, 20))),
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
        'pword': "a",
        'email': h.lower() + "gmail.com",
        'name': h[:-5] + " " + h[-5:],
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
        'story': ''.join(random.choice(string.ascii_lowercase) for _ in range(100, 150)),
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
        create_booking(i,hospitals[random.randrange(0, len(hospitals))])


# Start execution here!
if __name__ == '__main__':
    print('Starting population script...')
    populate()
