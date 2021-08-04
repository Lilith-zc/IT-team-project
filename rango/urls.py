from django.urls import path
from rango import views

app_name = 'rango'
urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('category/<slug:category_name_slug>/',views.show_category, name='show_category'),
   
    path('category/<slug:category_name_slug>/add_book/', views.add_book, name='add_book'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('book/<slug:book_name_slug>/', views.show_book, name='show_book'),
    path('add_comment/<slug:book_name_slug>/', views.add_comment, name='add_comment'),
    path('favorite/<slug:username>/', views.my_favorite, name='my_favorite'),
    path('add_favorite/<slug:book_name_slug>/', views.add_favorite, name='add_favorite'),
    path('operator/',views.operator_index,name='operator_index'),
    path('operator/add_category/', views.add_category, name='add_category'),
    path('operator/category/<slug:category_name_slug>/',views.operator_show_category, name='operator_show_category'),
    path('operator/delete_category/<slug:category_name_slug>/',views.operator_delete_category, name ='operator_delete_category'),
    path('operator/delete_book/<slug:book_name_slug>/',views.operator_delete_book, name ='operator_delete_book'),
    path('admin/',views.admin_index,name='admin_index'),
    path('admin/admin_delete_operator/<slug:operator_name>/',views.admin_delete_operator,name='admin_delete_operator')

]