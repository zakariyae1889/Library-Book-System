from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .serializers import *
from .models import *
from django.db.models import Avg, Q
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
#------------------------------#
def handle_exception(e):
    return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#**********************************Book****************************************/
""" book list """
class  BookListAPIView(APIView,PageNumberPagination):
    filter_backends = [filters.SearchFilter]
    search_fields = ['title','author__Firstname','author__Lastname','publisher__name','genre__name']

    try:
        def get(self, request, *args, **kwargs):
            queryset = Book.objects.all()
            for backend in list(self.filter_backends):
                queryset = backend().filter_queryset(self.request, queryset, view=self)

            page = self.paginate_queryset(queryset, request, view=self)
            if page is not None:
                serializer = BookSerializers(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = BookSerializers(queryset, many=True)
            return Response({"books": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        handle_exception(e)
""" book list """

""" book details """
class BookDetailAPIView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request, slug):
        try:
            book = get_object_or_404(Book, slug=slug)
            serializer = BookSerializers(book, many=False)
            return Response({"book": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
             handle_exception(e)
""" book details """

""" last book """
class LastBooksAPIView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request):
        try:
            books = Book.objects.all().order_by("-create")[:5]
            serializers = BookSerializers(books, many=True)
            return Response({"books": serializers.data}, status=status.HTTP_200_OK)
        except Exception as e:
            handle_exception(e)

""" related  book  """

class BookRelatedAPIView(APIView):
    throttle_classes=[UserRateThrottle,AnonRateThrottle]
    def get(self,request,slug):
        try:
            book=get_object_or_404(Book,slug=slug)
            realted_books=Book.objects.filter(genre=book.genre).exclude(slug=book.slug)[:4]
            serializers = BookSerializers(realted_books, many=True)
            return Response({"RealtedBooks": serializers.data}, status=status.HTTP_200_OK)
        except Exception as e:
            handle_exception(e)

""" reviews  book  """
class ReviewsBookAPIView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request):
        try:
            books = Book.objects.filter(Q(ratings__gte=4))
            serializers = BookSerializers(books, many=True)
            return Response({"books": serializers.data}, status=status.HTTP_200_OK)
        except Exception as e:
            handle_exception(e)
#************************************Author**************************************/
"""  author list  """
class  AuthorListAPIView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request):
        try:
            authors = Author.objects.all().order_by("-create")
            if not authors.exists():
                return Response({"message": "No authors found"}, status=status.HTTP_404_NOT_FOUND)

            serializers = AuthorSerializers(authors, many=True)
            return Response({"authors": serializers.data}, status=status.HTTP_200_OK)
        except Exception as e:
            handle_exception(e)
"""  author details  """
class  AuthorDetailAPIView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request, name):
        try:
            author = get_object_or_404(Author, Firstname=name)
            serializer = AuthorSerializers(author, many=False)
            return Response({"author": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            handle_exception(e)
#************************************Genre**************************************/
"""  genre list  """
class GenreListAPIView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request):
        try:
            genres = Genre.objects.all().order_by("-create")
            if not genres.exists():
                return Response({"message": "No genres found"}, status=status.HTTP_404_NOT_FOUND)

            serializers = GenreSerializers(genres, many=True)
            return Response({"genres": serializers.data}, status=status.HTTP_200_OK)
        except Exception as e:
           handle_exception(e)
"""   book by genre   """
class  BooksByGenreAPIView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request, name):
        try:
            genre = get_object_or_404(Genre, name=name)
            books = Book.objects.filter(genre=genre)
            serializers = BookSerializers(books, many=True)
            return Response({"books": serializers.data}, status=status.HTTP_200_OK)
        except Exception as e:
             handle_exception(e)
#************************************Publisher**************************************/
"""  publisher list  """
class PublisherListAPIView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request):
        try:
            publishers = Publisher.objects.all().order_by("-create")
            if not publishers.exists():
                return Response({"message": "No publishers found"}, status=status.HTTP_404_NOT_FOUND)

            serializers = PublisherSerializers(publishers, many=True)
            return Response({"publishers": serializers.data}, status=status.HTTP_200_OK)
        except Exception as e:
            handle_exception(e)
"""  books by publisher  """
class BooksByPublisherAPIView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request, name):
        try:
            publisher = get_object_or_404(Publisher, name=name)
            books = Book.objects.filter(publisher=publisher)
            serializers = BookSerializers(books, many=True)
            return Response({"books": serializers.data}, status=status.HTTP_200_OK)
        except Exception as e:
            handle_exception(e)
#************************************Reviews**************************************/
"""  create review  """
class ReviewCreateAPIView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        try:
            book = get_object_or_404(Book, slug=slug)
            data = request.data
            user = request.user
            review = book.reviews.filter(user=user).first()

            if not 1 <= data["rating"] <= 5:
                return Response({"messageerror": "Please select a rating between 1 to 5 only"},
                                status=status.HTTP_400_BAD_REQUEST)

            if review:
                review.rating = data["rating"]
                review.comment = data["comment"]
                review.save()
                message = "Book review updated"
            else:
                Reviews.objects.create(
                    book=book,
                    user=user,
                    rating=data['rating'],
                    comment=data['comment'],
                )
                message = "Book review created"

            book.ratings = book.reviews.aggregate(avg_ratings=Avg('rating'))['avg_ratings']
            book.save()
            return Response({"message": message}, status=status.HTTP_201_CREATED)

        except Exception as e:
             handle_exception(e)
