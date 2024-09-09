from django.db import models
from books.models import Book
from django.contrib.auth.models import User



class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
   
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(blank=True,null=True)
    fine_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "Borrow"
        verbose_name_plural = "Borrows"

    def __str__(self):
        return self.book.title

    def get_absolute_url(self):
        return reverse("Borrow_detail", kwargs={"pk": self.pk})

    
    def is_late(self):
        """
        تحقق مما إذا كانت الاستعارة متأخرة أم لا.
        """
        if self.return_date:
            return self.return_date > self.due_date
        return date.today() > self.due_date

  
    def save(self, *args, **kwargs):
        # تأكد من حساب الغرامة عند الحفظ
        self.calculate_fine()
        super().save(*args, **kwargs)

    def calculate_fine(self):
        if self.is_late():
            delay_days = (self.return_date - self.due_date).days if self.return_date else (date.today() - self.due_date).days
            daily_fine_amount = 5.00
            self.fine_amount = delay_days * daily_fine_amount
            print(f"Fine calculated: {self.fine_amount}")  # إضافة طباعة هنا
        else:
            self.fine_amount = 0.00
