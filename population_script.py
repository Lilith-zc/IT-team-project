import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','tango_with_django_project.settings')

import django
django.setup()

from django.contrib.auth.models import User
from rango.models import Category, Book, Author, Comment

def populate():
    authors = ['Alice', 'Bob', 'Catelin', 'David']
    users = ['User1', 'User2', 'User3', 'User4']
    
    authorList = []
    userList = []
    categoryList = []
    bookList = []
    commentList = []

    python_books = [
        {'title': 'Official Python Tutorial',
        'url':'http://docs.python.org/3/tutorial/',
        'views': 10,
        'author': authors[0],
        'introduction': 'python book 1 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'},
        {'title':'How to Think like a Computer Scientist',
        'url':'http://www.greenteapress.com/thinkpython/',
        'views': 25,
        'author': authors[1],
        'introduction': 'python book 2 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'},
        {'title':'Learn Python in 10 Minutes',
        'url':'http://www.korokithakis.net/tutorials/python/',
        'views': 60,
        'author': authors[2],
        'introduction': 'python book 3 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}
        ]

    django_books = [
        {'title':'Official Django Tutorial',
        'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
        'views': 24,
        'author': authors[0],
        'introduction': 'django book 1 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'},
        {'title':'Django Rocks',
        'url':'http://www.djangorocks.com/',
        'views': 8,
        'author': authors[2],
        'introduction': 'django book 2 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'},
        {'title':'How to Tango with Django',
        'url':'http://www.tangowithdjango.com/',
        'views': 34,
        'author': authors[3],
        'introduction': 'django book 3 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}
        ]

    other_books = [
        {'title':'Bottle',
        'url':'http://bottlepy.org/docs/dev/',
        'views': 29,
        'author': authors[1],
        'introduction': 'other book 1 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'},
        {'title':'Flask',
        'url':'http://flask.pocoo.org',
        'views': 45,
        'author': authors[3],
        'introduction': 'other book 2 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'} 
        ]

    cats = {
        'Python': {'Books': python_books,'views':128,'likes':64},
        'Django': {'Books': django_books,'views':64,'likes':32},
        'Other Frameworks': {'Books': other_books,'views':32,'likes':16} 
        }

    for author in authors:
        a = add_author(author)
        authorList.append(a)
    
    for user in users:
        u = add_user(user)
        userList.append(u)

    for cat, cat_data in cats.items():
        c = add_cat(cat,cat_data['views'],cat_data['likes'])
        categoryList.append(c)
        for p in cat_data['Books']:
            author = add_author(p['author'])
            b = add_book(c, p['title'], p['url'],p['views'],author,p['introduction'])
            bookList.append(b)

    for c in Category.objects.all():
        for p in Book.objects.filter(category=c):
            print(f'- {c}: {p}')


    for book in bookList:
        for user in userList:
            comment = add_comment(user, book)
            commentList.append(comment)


def add_book(cat, title, url, views, author,introduction):
    p = Book.objects.get_or_create(category=cat, author=author, title=title)[0]
    p.url=url
    p.views=views
    p.introduction=introduction
    p.save()
    return p

def add_cat(name,views,likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

def add_user(username):
    u = User.objects.get_or_create(username=username)[0]
    u.set_password(username)
    u.save()
    return u

def add_author(name):
    a = Author.objects.get_or_create(name=name)[0]
    a.views = 0
    a.save()
    return a

def add_comment(user, book):
    c = Comment.objects.get_or_create(user=user, book=book)[0]
    c.content = user.username + " likes " + book.title + " very much."
    c.score = 5
    c.save()
    return c

if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()