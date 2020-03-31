import os
import string

import random
from datetime import datetime

import django
import pytz

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blood_donation.settings')

django.setup()
from app.models import *

for donor in Donor.objects.all():
    print(Booking.show_all_bookings({ 'donor' : donor }))
for donor in Donor.objects.all():
    print(Review.show_donor_reviews({ 'donor' : donor }))
for hospital in Hospital.objects.all():
    print(Review.show_hospital_reviews({ 'hospital' : hospital }))