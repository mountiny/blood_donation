import os
import string

import random
from datetime import datetime

import django
import pytz

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blood_donation.settings')

django.setup()
from app.models import *

print(Story.show_all_stories())
print(Review.show_all_reviews())
print(Booking.show_all_bookings())