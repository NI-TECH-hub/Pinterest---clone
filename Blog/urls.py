from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('img/<int:id>',views.viewimage,name='viewimg'),

    path('login',views.userlogin,name='login'),
    path('logout',views.userlogout,name='logout'),
    path('signup',views.usersignup,name='signup'),
    path('changepassword',views.changepassword,name='changepassword'),


    
    path('profile',views.userprofile,name='profile'),
    path('editprofile',views.editprofile,name='editprofile'),
    # path('createprofile',views.createprofile,name='createprofile'),


    path('likepost/<int:id>',views.like,name='likepost'),
    path('addpost',views.addpost,name='addpost'),
    path('search',views.search,name='search'),
    path('sort_today',views.sortby,name='sortby'),
    path('contact/',views.contact,name='contact'),
    path('delete/<int:id>',views.deletepost,name='delete'),
]
