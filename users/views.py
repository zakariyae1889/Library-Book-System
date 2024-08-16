from rest_framework.decorators import api_view,permission_classes,throttle_classes
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from  .serializers import RegisterSerializers,CustomerSerializers,UserUpdateSerializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import logout
#------------------------------#
def handle_exception(e):
    return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#-----------------------ManageUsers------------------------------#
""""" Register user """""
class RegisterUserAPIViews(APIView):
    throttle_classes=[UserRateThrottle,AnonRateThrottle]
    def post(self,request):
        try:
            data=request.data
            user=RegisterSerializers(data=data)
            if user.is_valid():
                if not User.objects.filter(username=data["username"]).exists(): 
                    user=User.objects.create(
                        username=data["username"],
                        first_name=data["first_name"],
                        last_name=data["last_name"],
                        email=data["email"],
                        password=make_password(data['password'])
                    )
                    return Response(
                        {
                        "message":"your account register susccessfuly"
                        },
                        status=status.HTTP_201_CREATED
                    )
                else:
                    return Response(
                        {
                        "message":"This User Already Exists"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(user.errors)
        except Exception as e:
            handle_exception(e)

""""" current user """""
class  CurrentUserAPIView(APIView):
    throttle_classes=[UserRateThrottle,AnonRateThrottle]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            user=CustomerSerializers(request.user)
            return Response(user.data)
        except Exception as e:
            handle_exception(e)

""""" Edit user """""
class EditUserAPIView(APIView):
    throttle_classes=[UserRateThrottle,AnonRateThrottle]
    permission_classes=[IsAuthenticated]
    def put(self,reuqset):
        try:
            user=request.user
            data=request.data
            serializer=UserUpdateSerializers(user,data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                       "message" : "your account update susccessfuly"
                    }, 
                    status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            handle_exception(e)

""""" DELETE user """""
class DeleteUserAPIView(APIView):
    throttle_classes=[UserRateThrottle,AnonRateThrottle]
    permission_classes=[IsAuthenticated]
    def delete(self,request):
        try:
            user=request.user
            user.delete()
            
            return Response(
                    
                {
                    "message" : "your account delete susccessfuly"
                }, 
                status=status.HTTP_200_OK
            )
            logout(request)
        except Exception as e:
           handle_exception(e)

#------------------------------ManagePassowrd----------------------#
""""" change password """""
class ChangePasswordAPIViews(APIView):
    throttle_classes=[UserRateThrottle,AnonRateThrottle]
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            user=request.user
            current_password=request.data.get('current_password')
            new_password=request.data.get('new_password')
            if not user.check_password(current_password):
               return  Response({"message":"Current Password is incoorrect"},status=status.HTTP_400_BAD_REQUEST)
            else:
                user.set_password(new_password)
                user.save()
                return  Response({"message":"Password changed successfully"},status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            handle_exception(e)

#------------------------------Logout----------------------#
""""" logout """""
class LogoutAPIViews(APIView):
    def post(self,request):
        try:
            logout(request)
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
           handle_exception(e)

