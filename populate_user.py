import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','tango_with_django_project.settings')

import django
django.setup()

from django.contrib.auth.models import User
from rango.models import Category, Book, Author

userList = []
def populate():
    users = ['User1', 'User2', 'User3', 'User4']
    for user in users:
        u = User.objects.get_or_create(username=user)[0]
        u.set_password(user)
        userList.append(u)
        u.save()
    
    for user in userList:
        print(user)
        
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()