import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','tango_with_django_project.settings')

import django
django.setup()

from django.contrib.auth.models import User
from rango.models import Category, Book, Author, Comment, UserProfile, LikeList

def populate():
    authors = ['Alice', 'Bob', 'Catelin', 'David']
    userList = []
    userProfileList = []
    operaterList = []
    operaterProfileList = []
    
    authorList = []
    categoryList = []
    bookList = []
    commentList = []
    likelistList = []

    users = [
        {'username': 'user1',
        'password':'user1',
        'email': 'user1@user.com',
        'picture': 'profile_images/user1.jpg',
        'gender': 'male',
        'age': 18},
        {'username': 'user2',
        'password':'user2',
        'email': 'user2@user.com',
        'picture': 'profile_images/user2.jpg',
        'gender': 'female',
        'age': 20},
        {'username': 'user3',
        'password':'user3',
        'email': 'user3@user.com',
        'picture': 'profile_images/user3.jpg',
        'gender': 'male',
        'age': 22},
    ]

    operators = [
        {'username': 'operator1',
        'password':'operator1',
        'email': 'operator1@operator.com',
        'picture': 'profile_images/user4.jpg',
        'gender': 'male',
        'age': 24},
        {'username': 'operator2',
        'password':'operator2',
        'email': 'operator2@operator.com',
        'picture': 'profile_images/user5.jpg',
        'gender': 'female',
        'age': 26},
    ]

    admin = {'username': 'admin',
            'password':'admin',
            'email': 'admin@admin.com',
            'picture': 'profile_images/user6.jpg',
            'gender': 'male',
            'age': 28}

    python_books = [
        {'title': 'Official Python Tutorial',
        'url':'http://docs.python.org/3/tutorial/',
        'views': 0,
        'author': authors[0],
        'introduction': 'python book 1 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'image': 'book_images/book1.jpg'},
        {'title':'How to Think like a Computer Scientist',
        'url':'http://www.greenteapress.com/thinkpython/',
        'views': 0,
        'author': authors[1],
        'introduction': 'python book 2 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'image': 'book_images/book2.jpg'},
        {'title':'Learn Python in 10 Minutes',
        'url':'http://www.korokithakis.net/tutorials/python/',
        'views': 0,
        'author': authors[2],
        'introduction': 'python book 3 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'image': 'book_images/book3.jpg'}
        ]

    django_books = [
        {'title':'Official Django Tutorial',
        'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
        'views': 0,
        'author': authors[0],
        'introduction': 'django book 1 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'image': 'book_images/book4.jpg'},
        {'title':'Django Rocks',
        'url':'http://www.djangorocks.com/',
        'views': 0,
        'author': authors[2],
        'introduction': 'django book 2 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'image': 'book_images/book5.jpg'},
        {'title':'How to Tango with Django',
        'url':'http://www.tangowithdjango.com/',
        'views': 0,
        'author': authors[3],
        'introduction': 'django book 3 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'image': 'book_images/book6.jpg'}
        ]

    other_books = [
        {'title':'Bottle',
        'url':'http://bottlepy.org/docs/dev/',
        'views': 0,
        'author': authors[1],
        'introduction': 'other book 1 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'image': 'book_images/book7.jpg'},
        {'title':'Flask',
        'url':'http://flask.pocoo.org',
        'views': 0,
        'author': authors[3],
        'introduction': 'other book 2 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'image': 'book_images/book8.jpg'} 
        ]

    cats = {
        'Python': {'Books': python_books,'views':0,'likes':0},
        'Django': {'Books': django_books,'views':0,'likes':0},
        'Other Frameworks': {'Books': other_books,'views':0,'likes':0} 
        }

    for user in users:
        u, u_p = add_user(user['username'], user['password'], user['email'], 
                        user['picture'], user['gender'], user['age'])
        userList.append(u)
        userProfileList.append(u_p)

    for operator in operators:
        o, o_p = add_user(operator['username'], operator['password'], operator['email'], 
                        operator['picture'], operator['gender'], operator['age'])
        o_p.role = 'OPERATOR'
        o_p.save()
        operaterList.append(o)
        operaterProfileList.append(o_p)

    administrator, adminProfile =  add_user(admin['username'], admin['password'], admin['email'], 
                        admin['picture'], admin['gender'], admin['age'])
    adminProfile.role = 'ADMIN'
    adminProfile.save()

    for author in authors:
        a = add_author(author)
        authorList.append(a)

    for cat, cat_data in cats.items():
        c = add_cat(cat,cat_data['views'],cat_data['likes'])
        categoryList.append(c)
        for p in cat_data['Books']:
            author = add_author(p['author'])
            b = add_book(c, p['title'], p['url'],p['views'],author,p['introduction'],p['image'])
            bookList.append(b)

    for c in Category.objects.all():
        for p in Book.objects.filter(category=c):
            print(f'- {c}: {p}')

    for book in bookList:
        for user in userList:
            comment = add_comment(user, book)
            commentList.append(comment)

    for user in userList:
        for book in bookList[:3]:
            likelist = add_favorite(user, book)
            likelistList.append(likelist)


def add_user(username, password, email, picture, gender, age):
    user = User.objects.get_or_create(username=username)[0]
    user.set_password(password)
    user.email = email
    user.save()
    userprofile = UserProfile.objects.get_or_create(user=user, age=age)[0]
    userprofile.picture = picture
    userprofile.gender = gender
    userprofile.save()
    return user, userprofile

def add_book(cat, title, url, views, author,introduction, image):
    p = Book.objects.get_or_create(category=cat, author=author, title=title)[0]
    p.url=url
    p.views=views
    p.introduction=introduction
    p.image=image
    p.save()
    return p

def add_cat(name,views,likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

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

def add_favorite(user, book):
    likelist = LikeList.objects.get_or_create(user=user)[0]
    likelist.save()
    likelist.favoriteBook.add(book)
    return likelist

if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
