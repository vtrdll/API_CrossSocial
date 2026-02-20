"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from WOD.views import  create_wod, like_wod 
from Social.views import my_profile, HomeAPIView,  PostCreateViewAPI, StoryViewAPIView, PostDeteailViewAPI, PostUpdateDeleteViewAPI, CommentCreateViewAPI, CommentListUserView, CommentListUserDeleteOrUpdateViewAPI, LikePostViewAPI, LikeCommentViewAPI, StoryCreateViewAPI, StoryCreateViewTeamplate, StoryDeleteViewAPI, MyProfileAPI
from Social.views import HomeTemplateView, PostCreateViewAPITemplate, PostDetailViewAPITemplate, PostUpdateDeleteViewAPI
from account.views import PhotoUpdate, PhotoDelete, LoginAPIView, LogoutAPIView
from account.views import  RegisterAPIViewTemplate, RegisterAPIView, UserUpdateAPIView, UserUpdatePasswordAPIView,PrivacyConfigAPIView, CreateTeamAPIView
from Event.views import EventCreate, EventList, EventUpdate, EventDelete,  EventDetail

from account.views import create_time, add_member,detail_time, list_time, delete_time,remove_member,update_time
from account.views import   user_update, UserDelete, PasswordUpdate, ProfileDetail, UserList, register_pr,  update_pr, list_pr 


urlpatterns = [
    path('admin/', admin.site.urls),



    
    path('api/post/<int:pk>/', PostDeteailViewAPI.as_view(), name='post_detail_api' ),
    path('api/post/create/', PostCreateViewAPI.as_view(), name='post_create_api' ),
    path('api/update-delete/<int:pk>/', PostUpdateDeleteViewAPI.as_view(), name='post_update_delete_api' ),
    path('api/like/post/<int:pk>/', LikePostViewAPI.as_view(), name='post_like_api'),
    
    
    path('api/comment/<int:pk>/', CommentCreateViewAPI.as_view(), name='comment_create_api' ),
    path('api/comment/like/<int:pk>/', LikeCommentViewAPI.as_view(), name='comment_like_api' ),
    path('api/comment/user/<int:pk>/', CommentListUserView.as_view(), name='comment_list_user_api' ),
    path('api/comment/<int:pk>/delete/', CommentListUserDeleteOrUpdateViewAPI.as_view(), name='comment_delete_api' ),
    
    path('api/story/create/', StoryCreateViewAPI.as_view(), name='story_create_api' ),
    path('api/story/<int:pk>/view/', StoryViewAPIView.as_view(), name='story_view_api' ),
    path('api/story/<int:pk>/delete/', StoryDeleteViewAPI.as_view(), name='story_delete_api' ),

    path('api/profile/', MyProfileAPI.as_view(), name='my_profile_api' ),

    path('api/register/', RegisterAPIView.as_view(), name='register_api' ),
    path('api/profile/update/', UserUpdateAPIView.as_view(), name='profile_update_api' ),
    path('api/profile/update/password/', UserUpdatePasswordAPIView.as_view(), name='profile_update_password_api' ),
    path('api/login/', LoginAPIView.as_view(), name='login_api' ),
    path('api/logout/', LogoutAPIView.as_view(), name='logout_api' ),
    path('api/privacy/',PrivacyConfigAPIView.as_view(), name='privacy_api'),

    path('api/create_team/', CreateTeamAPIView.as_view(), name='create_team_api'),




    path('/register/', RegisterAPIViewTemplate.as_view(), name='register_template' ),


    path('story/create/', StoryCreateViewTeamplate.as_view(), name='story_create' ),

    path('post/create_wod/', create_wod, name='wod_create' ),
    path('perfil/<int:pk>/', ProfileDetail.as_view(), name='user_public_profile'),
    
    
    #path('story/<int:pk>/', StoryDetailView.as_view(), name='story_detail'),

    path('wod-liked/<int:pk>/like/', like_wod, name = 'like_wod'),

    path("stories/<int:pk>/view/", StoryViewAPIView.as_view(), name="story_view"),



 
    path('user-list/', UserList.as_view(), name='user_list'),
    path('user/editar/', user_update, name='user_update'),
    



    path('profile/<int:pk>/', ProfileDetail.as_view(), name='profile_detail'),


    path('user/<int:pk>/delete/', UserDelete.as_view(), name ='user-delete'),
    path('password/<int:pk>/editar/', PasswordUpdate.as_view(), name='password-change'),

    path('photo/<int:pk>/delete/', PhotoDelete.as_view(), name='photo-delete'),
    path('photo/<int:pk>/update/', PhotoUpdate.as_view(), name='photo-update'),
    
    path('event_create/', EventCreate.as_view(), name= 'event_create'),
    path('event_list/',  EventList.as_view(),  name='event_list'),
    path('event/<int:pk>/detail/', EventDetail.as_view(), name = 'event_detail'),
    path('event/<int:pk>/update/', EventUpdate.as_view(), name='event_update'),
    path('event/<int:pk>/delete/', EventDelete.as_view(), name='event_delete'),

    path('PersonalRecord/',  register_pr, name = 'create_pr'),
    path('PersonalRecord/<int:pk>/update', update_pr, name =  'update_pr'),
    path('PersonalRecord/home', list_pr, name='list_pr'),

    #path('list_wod/', list_wod, name = 'list_wod'),

    path('time/create/', create_time, name='time_create'),
    path('time/<int:time_id>/add/', add_member, name='add_member'),
    path('time/<int:time_id>/', detail_time, name='time_detail'),  
    path('time/<int:time_id>/update/', update_time , name='time_update'),
    path('time/<int:time_id>/delete/', delete_time, name='time_delete'),
    path('time/<int:time_id>/remover/<int:user_id>/', remove_member, name='remove_member'),
    path('times/',list_time, name='list_time'),
   

    path("", HomeTemplateView.as_view(), name="home"),
    path("api/home/", HomeAPIView.as_view(), name="home-api"),
    path('my_perfil/', my_profile, name='my_perfil'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
