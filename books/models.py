from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Genre(models.Model):

    name=models.CharField(max_length=255)
    descriptions=models.TextField(blank=True,null=True)

    create=models.DateTimeField(auto_now=True)
    update=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Genre")
        verbose_name_plural = ("Genres")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Genre_detail", kwargs={"pk": self.pk})
class Author(models.Model):

    Firstname=models.CharField(max_length=255)
    Lastname=models.CharField(max_length=255)
    biography=models.TextField(blank=True,null=True)
    photo=models.ImageField(upload_to="authorphoto/",blank=True,null=True)
    Datebirth=models.DateField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    create=models.DateTimeField(auto_now=True)
    update=models.DateTimeField(auto_now_add=True)


    

    class Meta:
        verbose_name = ("Author")
        verbose_name_plural = ("Authors")

    def __str__(self):
        return f'{self.Firstname}'

    def get_absolute_url(self):
        return reverse("Author_detail", kwargs={"pk": self.pk})

class Publisher(models.Model):
    name=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    website=models.URLField(null=True ,blank=True)


    create=models.DateTimeField(auto_now=True)
    update=models.DateTimeField(auto_now_add=True)
    

    class Meta:
        verbose_name = ("Publisher")
        verbose_name_plural = ("Publishers")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Publisher_detail", kwargs={"pk": self.pk})

class Book(models.Model):

    title=models.CharField(max_length=255)
    description=models.TextField(null=True,blank=True)
    author=models.ForeignKey(Author,on_delete=models.SET_NULL,null=True)
    publisher=models.ForeignKey(Publisher,on_delete=models.SET_NULL,null=True)
    genre=models.ForeignKey(Genre,on_delete=models.SET_NULL,null=True)
    ratings=models.DecimalField(max_digits=3,decimal_places=2,default=0.00)
    
    photo=models.ImageField(upload_to="authorphoto/",blank=True,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    slug=models.SlugField(blank=True,null=True)

    create=models.DateTimeField(auto_now=True)
    update=models.DateTimeField(auto_now_add=True)




    class Meta:
        verbose_name = ("Book")
        verbose_name_plural = ("Books")

    def __str__(self):
        return self.title


    def save(self, *args , **kwargs):
        self.slug=slugify(self.title)
        return super(Book,self).save( *args , **kwargs)


    def get_absolute_url(self):
        return reverse("Book_detail", kwargs={"pk": self.pk})


class Reviews(models.Model):
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name="reviews")
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.PositiveIntegerField()
    comment=models.TextField()
    create=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)


    




    def __str__(self) -> str:
        return self.books.title
