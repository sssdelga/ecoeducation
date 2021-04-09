from django.db import models
import re


class BookManager(models.Manager):
    def book_validate(self, post_data):
        errors = {}
        if len(post_data['title'])<1:
            errors['title']="A title must be provided"
        if len(post_data['desc'])<1:
            errors['desc']="A description must be provided"
        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    img_url = models.CharField(max_length=150)
    desc = models.TextField()
    month = models.DateTimeField()
    purchase_link = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()


class UserManager(models.Manager):
    def reg_validate(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email']="Invalid email address entered"
        if len(post_data['password'])<8:
            errors['password']="Password must be at least 8 characters"
        if post_data['password']!=post_data['pw_confirm']:
            errors['password']="Passwords did not match"
        return errors
    def login_validate(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email']="Invalid email address entered"
        return errors

# later addition - specify admin user
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    bday = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Subscriber(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    # improvement: if user exists, do not create a new log

class Carbon(models.Model):
    flights = models.PositiveIntegerField()
    drives = models.PositiveIntegerField()
    trains = models.PositiveIntegerField()
    fp_user = models.ForeignKey(User, related_name='carbon_footprint', on_delete=models.CASCADE)