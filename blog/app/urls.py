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
from WOD.views import CreateWodAPIVIEW, ListWodAPIView
from Social.views import my_profile, HomeAPIView,  PostCreateViewAPI, StoryViewAPIView, PostDeteailViewAPI, PostUpdateDeleteViewAPI, CommentCreateViewAPI, CommentListUserView, CommentListUserDeleteOrUpdateViewAPI, LikePostViewAPI, LikeCommentViewAPI, StoryCreateViewAPI, StoryCreateViewTeamplate, StoryDeleteViewAPI, MyProfileAPI
from Social.views import HomeTemplateView, PostCreateViewAPITemplate,  PostUpdateDeleteViewAPI, PostListViewAPI, StoryListViewAPI
from account.views import LoginAPIView, LogoutAPIView, UserUpdatePhotoAPIView, RegisterPersonalRecordAPIView, MeView
from account.views import  RegisterAPIViewTemplate, RegisterAPIView, UserUpdateAPIView, UserUpdatePasswordAPIView,PrivacyConfigAPIView,  UserDeleteAPIView, UserListAPIView, UserPhotoDeleteAPIView, UpdatePergonalRecordAPIView,  PersonalRecordListAPIView
from Event.views import EventCreate, EventList, EventUpdate, EventDelete,  EventDetail
from Team.views import CreateTeamAPIView, TeamListAPIView, DetailTeamAPIView, TeamUpdateDeleteAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/users/me/", MeView.as_view(), name="me"),

    path('api/posts/', PostListViewAPI.as_view(), name='post_list_api'),
    path('api/post/<int:pk>/', PostDeteailViewAPI.as_view(), name='post_detail_api' ),
    path('api/post/create/', PostCreateViewAPI.as_view(), name='post_create_api' ),
    path('api/update-delete/<int:pk>/', PostUpdateDeleteViewAPI.as_view(), name='post_update_delete_api' ),
    path('api/like/post/<int:pk>/', LikePostViewAPI.as_view(), name='post_like_api'),
    
    
    path('api/comment/<int:pk>/', CommentCreateViewAPI.as_view(), name='comment_create_api' ),
    path('api/comment/like/<int:pk>/', LikeCommentViewAPI.as_view(), name='comment_like_api' ),
    path('api/comment/user/<int:pk>/', CommentListUserView.as_view(), name='comment_list_user_api' ),
    path('api/comment/<int:pk>/delete/', CommentListUserDeleteOrUpdateViewAPI.as_view(), name='comment_delete_api' ),
    
    path('api/story/create/', StoryCreateViewAPI.as_view(), name='story_create_api' ),
    path('api/story_list/', StoryListViewAPI.as_view(), name='story_list_api'),
    path('api/story/<int:pk>/view/', StoryViewAPIView.as_view(), name='story_view_api' ),
    path('api/story/<int:pk>/delete/', StoryDeleteViewAPI.as_view(), name='story_delete_api' ),

    path('api/profile/', MyProfileAPI.as_view(), name='my_profile_api' ),

    path('api/register/', RegisterAPIView.as_view(), name='register_api' ),
    path('api/profile/update/', UserUpdateAPIView.as_view(), name='profile_update_api' ),
    path('api/profile_photo/update/', UserUpdatePhotoAPIView.as_view(), name = 'profile_photo_update_api'),
    path('api/profile_photo/delete/', UserPhotoDeleteAPIView.as_view, name= 'profile_photo_delete_api'),
    path('api/profile/update/password/', UserUpdatePasswordAPIView.as_view(), name='profile_update_password_api' ),
    path('api/delete-account/', UserDeleteAPIView.as_view(), name = 'profile_delete_api'),
    path('api/users/', UserListAPIView.as_view(),  name='users_list_api'),
    path('api/login/', LoginAPIView.as_view(), name='login_api' ),
    path('api/logout/', LogoutAPIView.as_view(), name='logout_api' ),
    path('api/privacy/',PrivacyConfigAPIView.as_view(), name='privacy_api'),

   

    path('api/create_pr/',RegisterPersonalRecordAPIView.as_view(), name='create_pr_api'),
    path('api/list_pr/',  PersonalRecordListAPIView.as_view(), name='list_Pr_api'),
    path('api/update_pr/<int:pk>/',UpdatePergonalRecordAPIView.as_view(),name='update_pr'),
    
    path('api/create_team/', CreateTeamAPIView.as_view(), name='create_team_api'),
    path('api/detail_team/<int:pk>/', DetailTeamAPIView.as_view(), name='detail_team'),
    path('api/list_team/', TeamListAPIView.as_view(), name='list_team_api'),
    path('api/update_team/<int:pk>/', TeamUpdateDeleteAPIView.as_view(),  name='update_team'),
    path('/register/', RegisterAPIViewTemplate.as_view(), name='register_template' ),


    path('story/create/', StoryCreateViewTeamplate.as_view(), name='story_create' ),

   

    
    
    #path('story/<int:pk>/', StoryDetailView.as_view(), name='story_detail'),

    path('api/create_wod/',CreateWodAPIVIEW.as_view(), name='create_wod_api'),
    path('api/wod_list/', ListWodAPIView.as_view(), name='wod_list_api'),
  
    path("stories/<int:pk>/view/", StoryViewAPIView.as_view(), name="story_view"),



    path('event_create/', EventCreate.as_view(), name= 'event_create'),
    path('event_list/',  EventList.as_view(),  name='event_list'),
    path('event/<int:pk>/detail/', EventDetail.as_view(), name = 'event_detail'),
    path('event/<int:pk>/update/', EventUpdate.as_view(), name='event_update'),
    path('event/<int:pk>/delete/', EventDelete.as_view(), name='event_delete'),

    path('api/personal_record/',  RegisterPersonalRecordAPIView.as_view(), name = 'pr_create_api'),



    #path('list_wod/', list_wod, name = 'list_wod'),

    path("", HomeTemplateView.as_view(), name="home"),
    path("api/home/", HomeAPIView.as_view(), name="home-api"),
    path('my_perfil/', my_profile, name='my_perfil'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
