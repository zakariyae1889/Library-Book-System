from rest_framework import serializers
from .models import *
class ReviewSerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source="user.username")
   
    books=serializers.ReadOnlyField(source="books.name")
    class Meta:
        model=Reviews
        fields='__all__'
    def validate_rating(self,value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

class GenreSerializers(serializers.ModelSerializer):
    class Meta:
        model=Genre
        fields = '__all__'

class AuthorSerializers(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source="user.username")
    class Meta:
        model=Author
        fields='__all__'

class PublisherSerializers(serializers.ModelSerializer):
    class Meta:
        model=Publisher
        fields="__all__"

class BookSerializers(serializers.ModelSerializer):
    reviews=serializers.SerializerMethodField(method_name="get_reviews",read_only=True)

    user=serializers.ReadOnlyField(source="user.username")
    author=AuthorSerializers()
    publisher=PublisherSerializers()
    genre=GenreSerializers()
 
    class Meta:
        model=Book
        fields='__all__'

    def get_reviews(self,obj):
        reviews=obj.reviews.all()
      
        serializer=ReviewSerializer(reviews,many=True)
        return serializer.data
        
       

