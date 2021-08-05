import os
from population_script import add_book
os.environ.setdefault('DJANGO_SETTINGS_MODULE','tango_with_django_project.settings')

import django
django.setup()

from django.contrib.auth.models import User
from rango.models import Category, Book, Author, UserProfile

userList = []
userProfileList = []
operaterList = []
operaterProfileList = []

def populate():
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

if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()