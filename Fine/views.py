from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *
from datetime import date
from loans.models import Borrow

class AllFinesAPIView(APIView):
  
    def get(self, request, *args, **kwargs):
        fines = Fine.objects.all() 
        serializer = FineSerializer(fines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class OverdueFinesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request, *args, **kwargs):
        today = date.today()

       
        late_borrows = Borrow.objects.filter(due_date__lt=today)
        overdue_fines = Fine.objects.filter(borrow__in=late_borrows, paid=False)
        if not overdue_fines.exists():
            return Response({"message": "No overdue fines found."}, status=status.HTTP_200_OK)

        serializer = FineSerializer(overdue_fines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    

class PayFineAPIView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    def post(self, request, *args, **kwargs):
        fine_id = request.data.get('fine_id')
        card_number = request.data.get('card_number')
        card_expiry = request.data.get('card_expiry')
        card_cvv = request.data.get('card_cvv')

        if not fine_id or not card_number or not card_expiry or not card_cvv:
            return Response({"message": "Fine ID and card details are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            fine = Fine.objects.get(id=fine_id)
        except Fine.DoesNotExist:
            return Response({"message": "No Fine record found for the given ID."}, status=status.HTTP_404_NOT_FOUND)

        if fine.paid:
           
            return Response({"message": "Fine has already been paid"}, status=status.HTTP_400_BAD_REQUEST)

        # تحقق من تفاصيل البطاقة (يمكن تحسينها)
        if len(card_number) < 13 or len(card_number) > 19:
            return Response({"message": "Invalid card number length."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Mock payment processing
            payment = Payment.objects.create(
                fine=fine,
                cc_number=card_number,
                cc_expiry=card_expiry,
                cc_code=card_cvv,
                paid=True
            )
            fine.paid = True
            fine.save()
            serializer = PaymentSerializer(payment)
            return Response({"message": "Payment processed successfully "}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        