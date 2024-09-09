from django.urls import path
from .views import *
urlpatterns = [
    path("",AllFinesAPIView.as_view()),
    path("overdueFines/", OverdueFinesAPIView.as_view()),
    path("payment/", PayFineAPIView.as_view())
]
