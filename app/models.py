import datetime
import json

from django.db import models
from django.db.utils import IntegrityError
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_donor = models.BooleanField(default=False)
    is_hospital = models.BooleanField(default=False)


class Donor(models.Model):
    # username, pword, first+last name, email
    donor = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    # donor_id = models.IntegerField(auto_created=True, unique=True, null=False, primary_key=True)

    nickname = models.CharField(max_length=40, unique=True)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    blood_type = models.CharField(max_length=3)
    weight = models.IntegerField()
    height = models.IntegerField()
    birth = models.DateField()
    age = models.IntegerField()
    notification = models.BooleanField(default=False)
    likedStories = models.TextField(default=json.dumps([]))

    def get_age(self, b):
        return int((datetime.date.today() - datetime.datetime.strptime(b, "%Y-%m-%d").date()).days / 365.25)

    def __str__(self):
        return self.nickname

    def new_donor(self, data):

        try:
            self.donor = User.objects.create_user(username=data['email'], password=data['password'])
        except IntegrityError:
            return {'error': "email already exists"}
        except:
            return {'error': "something went wrong please try again"}

        self.donor.first_name = data['first_name']
        self.donor.last_name = data['last_name']
        self.donor.is_donor = True

        self.nickname = data['username']
        self.birth = (data['birthday'])
        self.age = self.get_age(self.birth)

        self.address = data['city']

        self.height = data['height']
        if int (data['weight']) < 50:
            return {'error': "You must weight over 50kg to be able to sign up"}
        self.weight = data['weight']

        self.blood_type = data['blood_type']
        if data['notification'] == "true":
            self.notification = True
        else:
            self.notification = False
    
        try:
            self.donor.save()
            self.save()
        except IntegrityError:
            self.donor.delete()
            return {'error': "nickname already exists"}
        except:
            self.donor.delete()
            return {'error': "something went wrong please try again"}
        return {'error': None}


class Hospital(models.Model):
    # email, pword
    hospital = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    # hospital_id = models.IntegerField(auto_created=True, unique=True, null=False, primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=300)
    notified_types = models.CharField(max_length=100,default="NO")
    slug_name = models.SlugField(unique=True)
    # stories = models.ManyToOneRel(Hospital, )

    def save(self, *args, **kwargs):
        self.slug_name = slugify(self.name)
        super(Hospital, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def new_hospital(self, data):
        try:
            self.hospital = User.objects.create_user(username=data['hospital_email'], password=data['hospital_password'])
        except IntegrityError:
            return {'error': "email already exists"}
        except:
            return {'error': "something went wrong with email please try again"}

        self.hospital.is_hospital = True
        self.name = data['hospital_name']
        self.location = data['location']

        try:
            self.hospital.save()
            self.save()
        except:
            self.hospital.delete()
            return {'error': "something went wrong please try again"}
        return {'error': None}


class Story(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    date = models.DateField()
    story = models.TextField()
    heading = models.TextField()
    picture = models.ImageField()
    likes = models.IntegerField()

    def new_story(self, data):
        self.hospital = data['hospital']
        self.date = data['date']
        self.story = data['story']
        self.heading = data['heading']
        if data.get("picture") is not None:
            self.picture = data['picture']
        if data.get("likes") is not None:
            self.likes = data['likes']
        self.save()

    @staticmethod
    def show_story(data):
        id = data['story_id']
        story = Story.objects.get(id=id)
        return {'hospital': story.hospital.name,
                'date': story.date,
                'story': story.story,
                'heading': story.heading,
                'picture': story.picture,
                'likes': story.likes}

    @staticmethod
    def like_story(data):
        id = data['story_id']
        donor_id = data['donor_id']
        donor = Donor.objects.get(donor_id=donor_id)
        liked_stories = json.loads(donor.likedStories)
        # add like only if donor had not given like before
        if id not in liked_stories:
            story = Story.objects.get(id=id)
            story.likes += 1
            story.save()
            liked_stories.append(id)
            donor.likedStories = json.dumps(liked_stories)
            donor.save()

    @staticmethod
    def dislike_story(data):
        id = data['story_id']
        donor_id = data['donor_id']
        donor = Donor.objects.get(donor_id=donor_id)
        liked_stories = json.loads(donor.likedStories)
        if id in liked_stories:
            story = Story.objects.get(id=id)
            story.likes -= 1
            story.save()
            liked_stories.remove(id)
            donor.likedStories = json.dumps(liked_stories)
            donor.save()

    @staticmethod
    def show_all_stories():
        d = dict()
        for story in Story.objects.all():
            if story.hospital not in d:
                d[story.hospital] = []
            d[story.hospital].append(story.id)
        return d


class Booking(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    appointment = models.DateTimeField(unique=True)

    def new_appointment(self, data):
        self.donor = data['donor']
        self.hospital = data['hospital']
        self.appointment = data['appointment']
        self.save()

    @staticmethod
    def show_all_bookings(data):
        l = []
        for booking in Booking.objects.all():
            if booking.donor == data['donor']:
                l.append(booking.id)
        return l

    @staticmethod
    def get_slot(data):
        hosp_id = data['hospital_id']
        from_date = (datetime.datetime.now(tz=pytz.utc) + datetime.timedelta(days=1)).replace(hour=8, minute=0)
        to_date = (from_date + datetime.timedelta(days=6)).replace(hour=12, minute=0)

        def half_hour(h):
            return 0 if h % 2 == 0 else 30

        # initialize slots dictionary with all slots free
        slots = dict()
        for d in range(5):
            slots[(from_date + datetime.timedelta(days=d)).date()] = {}
            for t in range(0, 6):
                slots[(from_date + datetime.timedelta(days=d)).date()][datetime.time(9 + (t // 2), half_hour(t))] = True

        # booked slots for given hospital for the next 5 days
        booked_slots = Booking.objects.filter(hospital_id=hosp_id, appointment__range=[from_date, to_date])

        # enter booked slots to the dictionary
        for bs in booked_slots:
            slots[bs.appointment.date()][bs.appointment.time()] = False

        # pprint.pprint(slots)
        return slots


class Review(models.Model):
    # review_id = models.IntegerField(unique=True, primary_key=True)

    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    date = models.DateField()
    review = models.TextField()

    def new_review(self, data):
        self.donor = data['donor']
        self.hospital = data['hospital']
        self.date = data['date']
        self.review = data['review']

        self.save()

    @staticmethod
    def show_review(data):
        id = data['review_id']
        review = Review.objects.get(id=id)
        return {'donor': review.donor.nickname,
                'hospital': review.hospital.name,
                'date': review.date,
                'review': review.review}

    @staticmethod
    def show_all_reviews():
        d = dict()
        for review in Review.objects.all():
            if review.donor not in d:
                d[review.donor] = []
            d[review.donor].append(review.id)
        return d

    @staticmethod
    def show_hospital_reviews(data):
        l = []
        for review in Review.objects.all():
            if review.hospital == data['hospital']:
                l.append(review.id)
        return l

    @staticmethod
    def show_donor_reviews(data):
        l = []
        for review in Review.objects.all():
            if review.donor == data['donor']:
                l.append(review.id)
        return l
