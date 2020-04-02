import os
import string

import random
from datetime import datetime

import django
import pytz
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blood_donation.settings')

django.setup()
from app.models import *

def create_donor(data):
    donor = Donor()
    donor.new_donor(data)
    return donor


def create_hospital(data):
    hospital = Hospital()
    hospital.new_hospital(data)
    return hospital


def create_review(data):
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
    #create hospitals
    create_hospital({
        "hospital_email": "MGHBloodDonorCenter@partners.org",
        "hospital_password": "hospital1",
        "hospital_name": "Massachusetts General Hospital",
        "location": json.dumps({
            "lat": 42.362511,
            "lon": -71.069570
        })
    })
        
    create_hospital({
        "hospital_email": "HRQuestions@Jefferson.edu",
        "hospital_password": "hospital2",
        "hospital_name": "Jefferson University Hospitals",
        "location": json.dumps({
            "lat": 39.949775,
            "lon": -75.158040
        })
    })

    create_hospital({
        "hospital_email": "complaint@jcaho.org",
        "hospital_password": "hospital3",
        "hospital_name": "Maimonides Medical Center",
        "location": json.dumps({
            "lat": 40.639490,
            "lon": -73.998187
        })
    })

    create_hospital({
        "hospital_email": "huntington@hospital.org",
        "hospital_password": "hospital4",
        "hospital_name": "Huntington Hospital",
        "location": json.dumps({
            "lat": 34.134094,
            "lon": -118.152123
        })
    })

    create_hospital({
        "hospital_email": "chla@hospital.org",
        "hospital_password": "hospital5",
        "hospital_name": "Children's Hospital Los Angeles",
        "location": json.dumps({
            "lat": 34.097861,
            "lon": -118.289963
        })
    })

    # create donors
    create_donor({
        "username": "sonnen",
        "first_name": "Chael",
        "last_name": "Sonnen",
        "password": "donor1",
        "email": "chaelsonnen@donor.org",
        "birthday": "1977-4-3",
        "telephone": 4582004585,
        "city": "Portland",
        "height": 185,
        "weight": 103,
        "blood_type": "A+",
        "notification": True
    })

    create_donor({
        "username": "jones",
        "first_name": "Jon",
        "last_name": "Jones",
        "password": "donor2",
        "email": "jonjones@donor.org",
        "birthday": "1987-7-19",
        "telephone": 5855550199,
        "city": "Rochester",
        "height": 193,
        "weight": 93,
        "blood_type": "B-",
        "notification": False
    })

    create_donor({
        "username": "cruz",
        "first_name": "Dominick",
        "last_name": "Cruz",
        "password": "donor3",
        "email": "dominickcruz@donor.org",
        "birthday": "1985-3-9",
        "telephone": 6195550171,
        "city": "San Diego",
        "height": 173,
        "weight": 61,
        "blood_type": "AB+",
        "notification": True
    })

    create_donor({
        "username": "miocic",
        "first_name": "Stepe",
        "last_name": "Miocic",
        "password": "donor4",
        "email": "stepemiocic@donor.org",
        "birthday": "1982-8-19",
        "telephone": 2165550164,
        "city": "Euclid",
        "height": 193,
        "weight": 105,
        "blood_type": "0-",
        "notification": True
    })

    create_donor({
        "username": "gaethje",
        "first_name": "Justin",
        "last_name": "Gaethje",
        "password": "donor5",
        "email": "justingaethje@donor.org",
        "birthday": "1988-11-14",
        "telephone": 9375550194,
        "city": "Safford",
        "height": 180,
        "weight": 70,
        "blood_type": "A-",
        "notification": False
    })

    # get donors and hospital from database
    donors = Donor.objects.all()
    hospitals = Hospital.objects.all()

    # create reviews
    create_review({
        "date": datetime.date(2017, 3, 29),
        "review": "The hospital is one of the best in the United States and the world. It has obtained several awards. The care is very good.",
        "donor": donors[0],
        "hospital": hospitals[0]
    })

    create_review({
        "date": datetime.date(2019, 2, 3),
        "review": "You were all truly amazing. We couldn’t have done it without you all. Thank you so much.",
        "donor": donors[1],
        "hospital": hospitals[1]
    })
    
    create_review({
        "date": datetime.date(2011, 11, 19),
        "review": "All the doctors nurses and staff were wonderful, kind and understanding.",
        "donor": donors[2],
        "hospital": hospitals[2]
    })
    
    create_review({
        "date": datetime.date(2013, 4, 8),
        "review": " I would like to thank the hospital staff for the professional, competent and committed approach they deliver at all times.",
        "donor": donors[3],
        "hospital": hospitals[3]
    })
    
    create_review({
        "date": datetime.date(2017, 9, 7),
        "review": "The building may be a bit old-fashioned, but the care and facilities are just as good as you would receive anywhere else.",
        "donor": donors[4],
        "hospital": hospitals[4]
    })

    # add some stories
    for i in range(len(hospitals)):
        for _ in range(3):
            create_story(hospital=hospitals[i])

    # add bookings
    for d in donors:
        create_booking(d,hospitals[random.randrange(0, len(hospitals))])


# Start execution here!
if __name__ == '__main__':
    print('Starting population script...')
    populate()
