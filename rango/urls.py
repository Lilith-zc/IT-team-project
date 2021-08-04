from django.urls import path
from rango import views

app_name = 'rango'
urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('category/<slug:category_name_slug>/',views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('book/<slug:book_name_slug>/<slug:username>', views.show_book, name='show_book'),
    path('add_comment/<slug:book_name_slug>/', views.add_comment, name='add_comment'),
    path('favorite/<slug:username>/', views.my_favorite, name='my_favorite'),
    path('add_favorite/<slug:book_name_slug>/', views.add_favorite, name='add_favorite'),
]