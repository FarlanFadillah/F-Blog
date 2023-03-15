from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name='login'), 
    path('home/<str:unique>', views.home, name='home'),
    path('home/<str:unique>/post', views.post, name='post'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('profile/<str:username>', views.profile, name="profile"),
    path('uploadimg', views.uploadimg, name='uploadimg'),
    path('content/<str:username>/<str:id>', views.content, name='content'),
    path('comment/<str:username>/<str:id>', views.comment, name='comment'),
    path('search/<str:keyword>', views.search, name='search'),
    path('follow/<str:followed_id>', views.follow, name='follow'),

]