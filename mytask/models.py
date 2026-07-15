from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name


class Blog(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    post_body = models.TextField()
    created_date = models.DateField()

    def __str__(self):
        return self.title


class PostData(models.Model):
    title = models.CharField(max_length=30)
    post_body = models.TextField()
    created_date = models.DateField()

    def __str__(self):
        return self.title
     

class Book(models.Model):
    title = models.CharField(max_length=30)
    post_body = models.TextField()
    created_date = models.DateField()

    def __str__(self):
        return self.title 