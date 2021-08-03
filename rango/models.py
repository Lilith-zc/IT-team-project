from datetime import datetime
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    NAME_MAX_LENGTH = 128
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(blank=True,unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Author(models.Model):
    NAME_MAX_LENGTH = 128
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField(blank=True,unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Author, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Book(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='book_images', blank=True)
    slug = models.SlugField(blank=True,unique=True)
    introduction = models.TextField(blank=True)
    views = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Book, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    GENDER_MAX_LENGTH = 128
    AGE_MAX_LENGTH = 128
    ROLE_MAX_LENGTH = 128
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    gender = models.CharField(max_length=GENDER_MAX_LENGTH)
    age = models.IntegerField(max_length=AGE_MAX_LENGTH)
    role = models.CharField(max_length=ROLE_MAX_LENGTH, default="USER")
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

class LikeList(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favoriteBook = models.ManyToManyField(Book)

    def __str__(self):
        return self.user.username + "'s favorite books."

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    content = models.TextField()
    score = models.IntegerField(default=5)
    date = models.DateTimeField(default = datetime.now())

    def __str__(self):
        return self.content

class History(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    browsedBook = models.ManyToManyField(Book)
    date = models.DateTimeField(default = datetime.now())

    def __str__(self):
        return self.user + " browsed " + self.browsedBook

