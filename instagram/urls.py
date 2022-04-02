from django.urls import path
from . import views

urlpatterns=[
    path('',views.welcome,name = 'welcome'),
    path('search/', views.search_results, name='search_results'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update.profile'),
    path('upload/add/', views.new_post, name='save.image'),
    path('like/<int:id>/', views.like_image, name='like.image'),
    path('post/<int:id>/', views.view_post, name='single.image'),
    path('comment/add', views.add_comment, name='comment.add'),
    path('user/<int:id>/', views.user_profile, name='user.profile'),
]