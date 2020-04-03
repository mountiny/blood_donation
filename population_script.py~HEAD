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


def create_story(data):
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

    create_story({
        "hospital": hospitals[0],
        "date": datetime.date(2019, 12, 12),
        "heading": "Alicia's car accident",
        "story": "42 minutes trapped in a car after a head-on collision, 8 units of donated blood, 12 surgeries, 17 days in a coma, 18 months in a wheelchair, and 5 years of physical therapy and recovery that involved re-learning how to read, write, and talk. Alicia Northenscold has been through more than most.\n\nOne snowy morning in 2009, 27-year-old Alicia was driving to work when her car was struck by an oncoming vehicle. The impact compacted the dash of Alicia’s car, pinning her legs under the dash; she was trapped until help was able to get to the scene.\n\nWhen first responders arrived from the Boston Fire Department, they pulled back the dash of Alicia’s car and freed her. “As a responder, you’re taught to never to use tools together – they’re very expensive and can be dangerous when combined,” said Alicia. “But they said, ‘let’s do it’ and they got my legs out of there.” To this day, Alicia and her family have stayed in touch with the Boston Fire Department.\n\nAlicia was transported to Massachusetts General Hospital in Boston, where she received 8 units of blood and had 12 surgeries over the next few months. The accident broke both of her femurs and her hip. Formerly a kickboxer and a runner, Alicia had to re-learn how to use her legs. She also broke her neck and sustained a traumatic brain injury, putting her in a coma for 17 days. It took her 5 years to learn to read again, and once she could, she went back to school to pursue a degree in neuropsychology. Alicia was told she would be unable to have children, but today she is a mother of two daughters. All thanks to generous blood donors, fast-acting first responders, and excellent care teams – not to mention Alicia’s positivity and bravery.\n\nAlicia knows how vital donated blood was to her survival and recovery. “Donated blood saved my life, so I can help save more people’s lives and pay it forward.” She donates blood with the Massachusetts General Hospital regularly, adding that it’s “completely selfless giving – it doesn’t come out of our pockets, we can give and get it back.”\n\nIn spring 2019, Alicia held her first-ever blood drive to commemorate the 10-year anniversary of her accident and rescue. The drive was held at the Boston Fire Department, and several of Alicia’s firefighters and paramedics that helped during her accident attended and donated. It was a huge success, and Alicia plans to make it an annual tradition in honor of the first responders at the Boston Fire Department. “To be able to give back and get other people to give blood is huge. My goal is that giving blood will become a routine thing for others as well.”",
        "likes": 20,
        "picture": "alicia.png"
    })

    create_story({
        "hospital": hospitals[4],
        "date": datetime.date(2019, 1, 17),
        "heading": "Ike's fight with cancer",
        "story": "Fever and ear pain. A stubborn rash that wouldn’t go away. Then tests indicating low hemoglobin levels and a declining white blood cell count. For parents Chelsea and Chad, they knew going into the ER with their young son, Ike, that something wasn’t right. What they didn’t expect was to hear the words, “your child has cancer.”\n\nJust three days shy of his fifth birthday, Ike was diagnosed with B-ALL leukemia, a fast-growing cancer of lymphocyte-forming cells typically found in the blood stream and bone marrow. At that moment, Ike and his parents sprang into action. Ike received his first blood transfusion while still in the hospital, and regular transfusions helped sustain him as he endured months of chemotherapy treatments. Despite the rigor of his maintenance routine—a spinal tap every three months, a monthly trip to the clinic for lab tests, a weekly dose of eight chemotherapy pills, plus another nightly dose of pills as well—Ike was back to playing hockey and baseball even during his treatments.\n\n“Ike’s diagnosis was life-changing for all of us,” said Ike's mom Chelsea. “Through it all, he was incredibly strong and resilient—and tough. That’s why we came together almost immediately as a community of friends and family and began blogging, fundraising, and hosting events.\"\n\nIke’s last cancer treatment was in July of 2016—three years after his diagnosis. Today, like clockwork, his family holds an annual “Tough Like Ike” golf and silent auction event to raise funds for children going through similar treatment. Additionally, Ike’s elementary school coordinates a “Tough Like Ike” blood drive each year in his honor to give back to hospitals like Children’s Hospital Los Angeles, where Ike received his numerous blood transfusions.\n\n\"We want to honor Ike’s toughness, to raise awareness of the need for more research into childhood cancers, and to give back in gratitude for all the generous blood donors who were there with the blood Ike needed to survive,” said Chelsea.",
        "likes": 25,
        "picture": "ike.jpg"
    })

    # add bookings
    for d in donors:
        create_booking(d,hospitals[random.randrange(0, len(hospitals))])


# Start execution here!
if __name__ == '__main__':
    print('Starting population script...')
    populate()
