from django.urls import path
from .views import *
    

urlpatterns = [
    path("account/create",RegisterUserAPIViews.as_view()),
    #--------------------manageUser----------------#
    path("account",CurrentUserAPIView.as_view()),
    
    path("account/update",EditUserAPIView.as_view()),
    path("account/delete",DeleteUserAPIView.as_view()),
    #--------------------managePassword----------------#
    path("passord/change",ChangePasswordAPIViews.as_view()),
    #--------------------manageLogut----------------#
    path("logout",LogoutAPIViews.as_view()),

]
