from django.urls import path
from .views import *
urlpatterns = [
    path("",LoansListAPIView.as_view(),name="loans-list"),
    path("<slug:slug>/",LoansDetails.as_view(),name="loans-details"),
    path('create-loans', LoansCreateAPIView.as_view(), name='create-loans'),
    path('update-loans',LoansUpdateAPIView.as_view(), name='update-loans'),
    path('delete-loans/<str:title>',LoansDeleteAPIView.as_view(), name='delete-loans'),
    path('create-return-book',ReturnBookAPIView.as_view(), name='create-return-book'),
    path('late-return-book',LateBooksAPIView.as_view(), name='late-return-book'),

]
