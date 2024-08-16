from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

urlpatterns =[
    
    path('api/admin/', admin.site.urls),
    path("api/users/",include("users.urls")),
    path('api/token/', TokenObtainPairView.as_view()),

    path("api/books/",include("books.urls")),


    path('api/token/refresh/', TokenRefreshView.as_view()),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404='utils.error.handler_404'
handler500='utils.error.handler_500'