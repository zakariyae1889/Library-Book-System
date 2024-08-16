from django.urls import path
from .views import *
    


urlpatterns = [
    # Books URLs
    path('', BookListAPIView.as_view(), name='books-list'),
    path('<slug:slug>/', BookDetailAPIView.as_view(), name='book-detail'),
    path('latest', LastBooksAPIView.as_view(), name='books-latest'),
    path('trendy', ReviewsBookAPIView.as_view(), name='books-reviews'),
    path('<slug:slug>/realated-books',BookRelatedAPIView.as_view(), name='books-realeted'),
    
    # Authors URLs
    path('authors', AuthorListAPIView.as_view(), name='authors-list'),
    path('authors/<str:name>/', AuthorDetailAPIView.as_view(), name='author-detail'),
    
    # Genres URLs
    path('genres', GenreListAPIView.as_view(), name='genres-list'),
    path('genres/<str:name>', BooksByGenreAPIView.as_view(), name='books-by-genre'),
    
    # Publishers URLs
    path('publishers', PublisherListAPIView.as_view(), name='publishers-list'),
    path('publishers/<str:name>', BooksByPublisherAPIView.as_view(), name='books-by-publisher'),
    
    # Reviews URLs
    path('<slug:slug>/reviews/', ReviewCreateAPIView.as_view(), name='create-review'),
]
