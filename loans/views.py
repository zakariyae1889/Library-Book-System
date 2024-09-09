from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework import filters
from .serializers import *
from .models import *
from django.utils import timezone

def handle_exception(e):
    return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

""" Loans list """
class LoansListAPIView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
   

    def get(self, request, *args, **kwargs):
        try:
            queryset = Borrow.objects.all()
            search = request.GET.get("search", None)
            if search:
                queryset = queryset.filter(
                    Q(book__title__icontains=search) |
                    Q(user__username__icontains=search) |
                    Q(borrow_date__icontains=search) |
                    Q(due_date__icontains=search)
                )
            serializer = ListSerializer(queryset, many=True)
            return Response({"books": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return handle_exception(e)

""" Loans details """
class LoansDetails(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request, slug):
        try:
            loans = get_object_or_404(Borrow, book__slug=slug)
            serializer = DetailsSerializer(loans)
            return Response({"book": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return handle_exception(e)

""" Create loans """
class LoansCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        try:
            serializer = createSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Borrow created successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return handle_exception(e)

""" Update loans """
class LoansUpdateAPIView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        try:
            username = request.data.get("username")
            title = request.data.get("title")

            if not username or not title:
                return Response({"error": "Username and book title are required."}, status=status.HTTP_400_BAD_REQUEST)

            user = get_object_or_404(User, username=username)
            book = get_object_or_404(Book, title=title)
            borrow = get_object_or_404(Borrow, user=user, book=book)

            serializer = UpdateSerializer(borrow, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Borrow updated successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return handle_exception(e)

""" Delete loans """
class LoansDeleteAPIView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    permission_classes = [IsAuthenticated]

    def delete(self, request, title):
        try:
            user = request.user
            book = get_object_or_404(Book, title=title)
            borrow = get_object_or_404(Borrow, user=user, book=book)
            borrow.delete()
            return Response({"message": "Your loan was deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return handle_exception(e)

""" Return book loans """
class ReturnBookAPIView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    

    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get("username")
            title = request.data.get("title")

            if not username or not title:
                return Response({"error": "Username and book title are required."}, status=status.HTTP_400_BAD_REQUEST)

            user = get_object_or_404(User, username=username)
            book = get_object_or_404(Book, title=title)
            borrow = get_object_or_404(Borrow, user=user, book=book)

            serializer = ReturnBookSerializer(borrow, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Borrow return date updated successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return handle_exception(e)
            
class LateBooksAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            today=timezone.now().date()
            late_borrows=Borrow.objects.filter(return_date__isnull=True,due_date__lt=today)
            serializer=LateBorrowSerializer(late_borrows,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return handle_exception(e)

