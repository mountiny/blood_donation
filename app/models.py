import datetime

from django.db import models

from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser


# Create your models here.
# class Donor(models.Model):
#     # username, pword, first+last name, email
#     donor = models.OneToOneField(User, on_delete=models.CASCADE)
#
#     # id = models.IntegerField(auto_created=True, unique=True, null=False, primary_key=True)
#     phone = models.CharField(max_length = 10)
#     address = models.CharField(max_length=100)
#     blood_type = models.CharField(max_length=3)
#     weight = models.IntegerField()
#     height = models.IntegerField()
#     birth = models.DateField()
#     age = models.IntegerField()
#     notification = models.BooleanField
#
#     def get_age(self):
#         return int((datetime.date.today() - self.birth).days / 365.25)
#
#     def __str__(self):
#         return self.donor.username
#
#     def new_donor(self, data):
#         # self.donor_id = data['donor_id']
#         self.username = data['username']
#         self.first_name = data['first']
#         self.last_name = data['last']
#         self.password = data['pword']
#
#         self.email = data['email']
#         self.birth = data['birth']
#         self.age = self.get_age()
#
#         self.phone = data['phone']
#         self.address = data['address']
#
#         self.height = data['height']
#         self.weight = data['weight']
#
#         self.blood_type = data['blood_type']
#         self.notification = data['notification']
#         self.save()
#         # return self


class User(AbstractUser):
    is_donor = models.BooleanField(default=False)
    is_hospital = models.BooleanField(default=False)


class Donor(models.Model):
    # username, pword, first+last name, email
    donor = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    # donor_id = models.IntegerField(auto_created=True, unique=True, null=False, primary_key=True)

    nickname = models.CharField(max_length=40, null=True)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    blood_type = models.CharField(max_length=3)
    weight = models.IntegerField()
    height = models.IntegerField()
    birth = models.DateField()
    age = models.IntegerField()
    notification = models.BooleanField

    def get_age(self, b):
        return int((datetime.date.today() - datetime.datetime.strptime(b, "%Y-%m-%d").date()).days / 365.25)

    def __str__(self):
        return self.donor.username

    def new_donor(self, data):
        donor = User.objects.create_user(username = data['email'], password=data['password'])

        donor.first_name = data['first_name']
        donor.last_name = data['last_name']
        donor.nickname = data['nickname']
        donor.is_donor = True

        self.birth = (data['birthday'])
        self.age = self.get_age(self.birth)

        self.phone = data['telephone']
        self.address = data['city']

        self.height = data['height']
        self.weight = data['weight']

        self.blood_type = data['blood_type']
        # self.notification = data['notification']
        donor.save()
        self.save()


class Hospital(models.Model):
    # email, pword
    hospital = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    # hospital_id = models.IntegerField(auto_created=True, unique=True, null=False, primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=300)
    notified_types = models.CharField(max_length=100)
    slug_name = models.SlugField(unique=True)

    # stories = models.ManyToOneRel(Hospital, )

    def save(self, *args, **kwargs):
        self.slug_name = slugify(self.name)
        super(Hospital, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


    def new_hospital(self, data):
        # hospital = User.objects.create_user(data['hospital_name'], data['hospital_email'], data['hospital_password'])
        hospital = User.objects.create_user(username= data['hospital_email'], password=data['hospital_password'])
        hospital.is_hospital = True
        self.name = data['hospital_name']
        # self.location = data['location']
        # self.notified_types = data['notif_types']

        hospital.save()
        self.save()


class Story(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    date = models.DateField()
    story = models.TextField()
    picture = models.ImageField()
    likes = models.IntegerField()

    def new_story(self, data):
        self.hospital = data['hospital']
        self.date = data['date']
        self.story = data['story']
        self.picture = data['picture']
        self.likes = data['likes']
        self.save()


class Booking(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    appointment = models.DateTimeField(unique=True)

    def new_appointment(self, data):
        self.donor = data['donor']
        self.hospital = data['hospital']
        self.appointment = data['appointment']
        self.save()


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
