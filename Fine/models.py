# models.py
from django.db import models
from django.contrib.auth.models import User
from loans.models import Borrow
from datetime import timedelta, date
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField


class Fine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrow = models.ForeignKey(Borrow, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    issued_date = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Fine for {self.borrow.book.title} by {self.user.username}'

    def save(self, *args, **kwargs):
        if not self.paid:
            self.amount = self.borrow.fine_amount
        else : self.amount=0.00
        super().save(*args, **kwargs)


class Payment(models.Model):
    fine = models.OneToOneField('Fine', on_delete=models.CASCADE)
    cc_number = CardNumberField(verbose_name='card number')
    cc_expiry = CardExpiryField(verbose_name=('expiration date'))
    cc_code = SecurityCodeField(verbose_name=('security code'))
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Payment for Fine ID {self.fine.id}'

