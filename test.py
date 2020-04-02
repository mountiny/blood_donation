import os
import string

import random
from datetime import datetime

import django
import pytz

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blood_donation.settings')

django.setup()
from app.models import *

print ("pepa")
print(Donor.objects.get(donor_id=1))
c = type(Donor.objects.get(donor_id=1))
print (f"type of query {c}")

d = Donor.objects.get(donor_id=1)
print ("nickname: ", d.nickname)
print ("only donors")
print(User.objects.filter(is_donor=1))

print ("donor 1")
print(Donor.objects.filter(donor_id=1))

print ("all donors")
print (Donor.objects.all())

print (Hospital.objects.filter(hospital_id=4))
print (Hospital.objects.all())

print ("hospital 1")
h=Hospital.objects.get(hospital_id=3)
print (h.hospital)