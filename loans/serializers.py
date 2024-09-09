from rest_framework import serializers
from .models import *
from books.serializers import BookSerializers
from django.contrib.auth.models import User
from datetime import timedelta,date

class ListSerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source="user.username")
    book=serializers.ReadOnlyField(source="book.title")
    class Meta:
        model=Borrow
        fields = ['book', 'user',"due_date"]

class DeatilsSerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source="user.username")
    book=BookSerializers()
    class Meta:
        model=Borrow
        fields = ['title', 'username',"due_date"]

class createSerializer(serializers.ModelSerializer):
    title=serializers.CharField(write_only=True)
    username=serializers.CharField(write_only=True)
    due_date=serializers.DateField(required=False)

    class Meta:
        model = Borrow
        fields = ['title', 'username',"due_date"]

    def create(self,validated_data):

        title=validated_data.pop("title")
        username=validated_data.pop("username")

        try:
            book=Book.objects.get(title=title)
        except Book.DoesNotExist:
            raise serializers.ValidationError({"title":"title of the book does not exist"})
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({"username":"username does not exist"})

        if ('due_date' not in validated_data or not validated_data["due_date"]):
            validated_data["due_date"]=date.today()+timedelta(days=15)

        loans=Borrow.objects.filter(book=book,return_date__isnull=True)

        if loans.exists():
            raise serializers.ValidationError({"book":" This book is borrowed by another client "})

        borrow=Borrow.objects.create(book=book,user=user,**validated_data)

        return borrow
    def validate_due_date(self,value):
        if value < date.today():
            raise serializers.ValidationError("Due date cannot be before the current day")



class UpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    due_date = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = Borrow
        fields = ['title', 'username',"due_date"]

    def update(self, instance, validated_data):
       
        title=validated_data.pop("title")
        username=validated_data.pop("username")
        if title:
            try:
                book = Book.objects.get(title=title)
                instance.book = book
            except Book.DoesNotExist:
                raise serializers.ValidationError({"title": "The title of the book does not exist."})
        if username:
            try:
                user=User.objects.get(username=username)
            except User.DoesNotExist:
                raise serializers.ValidationError({"username":"username does not exist"})
       
        due_date = validated_data.get("due_date")
        if not due_date:
            due_date = date.today() + timedelta(days=16)
        instance.due_date = due_date
        
      
        instance.save()
        return instance

class ReturnBookSerializer(serializers.ModelSerializer):
    title=serializers.CharField(write_only=True)
    username=serializers.CharField(write_only=True)
    
    class Meta:
        model = Borrow
        fields = ['title', 'username',"return_date"]

    def create(self,validated_data):

        title=validated_data.pop("title")
        username=validated_data.pop("username")

        try:
            book=Book.objects.get(title=title)
        except Book.DoesNotExist:
            raise serializers.ValidationError({"title":"title of the book does not exist"})
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({"username":"username does not exist"})

        borrow=Borrow.objects.create(book=book,user=user,**validated_data)

        return borrow
    def validate_due_date(self,value):
        if value < date.today():
            raise serializers.ValidationError("Due date cannot be before the current day")


class LateBorrowSerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source="user.username")
    book=serializers.ReadOnlyField(source="book.title")
   
    class Meta:
        model=Borrow
        fields = '__all__'
