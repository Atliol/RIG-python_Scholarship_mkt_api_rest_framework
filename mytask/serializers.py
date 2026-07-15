from rest_framework import serializers
from .models import Blog, PostData, Book

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        # category ကိုပါ fields ထဲ ထည့်ပေးထားပါတယ်
        fields = ['id', 'category', 'title', 'post_body', 'created_date']

class PostDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostData
        fields = ['id', 'title', 'post_body', 'created_date']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'post_body', 'created_date']