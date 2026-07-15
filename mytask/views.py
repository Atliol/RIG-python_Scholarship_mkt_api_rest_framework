from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView

# ဘယ်တော့မှ မေ့မရတဲ့ အမှားလိုင်းဟောင်းကို ဖျက်လိုက်ပြီး .models ကနေ အကုန်ယူထားပါတယ်
from .models import *
from .tests import sumnumber

from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .serializers import BlogSerializer, BookSerializer, PostDataSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

# Create your views here.

@login_required
def about(request):
    ans = sumnumber(40, 20)
    print(ans)
    return render(request, 'about.html')

@login_required
def homepage(request):
    title = "My Blog Title"
    cat_data = Category.objects.all()
    blogs = Blog.objects.all()
    contex = {
        'abc': title,
        'name': 'Mg Myo Kyaw',
        'datas': cat_data,
        'blogs': blogs
    }
    return render(request, 'home.html', contex)

def save_blog(request):
    cate = request.POST.get('category')
    cat = Category(category_name=cate)  
    cat.save()
    return redirect("url:home")

def filter_blog(request):
    cid = request.GET.get('cid')
    cat_obj = Category.objects.get(id=cid)
    filter_data = Blog.objects.filter(category=cat_obj)
    context = {
        'blogs': filter_data
    }
    return render(request, 'home.html', context)
    
def detail_blog(request, blogid):
    blog = Blog.objects.get(id=blogid)
    if request.method == 'POST':
        title = request.POST.get('title')
        pbody = request.POST.get('post_body')
        blogs = Blog.objects.filter(id=blogid)
        blogs.update(title=title, post_body=pbody)
        return redirect('/')
     
    context = {
        'blog': blog
    }
    return render(request, 'blogdetail.html', context)

def createblog(request):
    form = MyblogModelForm()
    if request.method == 'POST':
        fm = MyblogModelForm(request.POST)
        if fm.is_valid():
            fm.save()
            return redirect('/')
    context = {"fm": form}
    return render(request, 'createblog.html', context)


class MyBlogView(View):
    def get(self, request):
        blogs = Blog.objects.all()
        context = {
            'blogs': blogs
        }
        return render(request, 'home.html', context)
    def post(self, request):
        fm = MyblogModelForm(request.POST)
        if fm.is_valid():
            fm.save()        
        return redirect('/')  
    
    def put(self, request):
        return HttpResponse("This is put method")
    
    def delete(self, request):
        return HttpResponse("This is delete method")


class LoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class MangaerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class MyBlogTemplateView(MangaerRequiredMixin, ListView):
    template_name = 'home.html'
    model = Blog
    context_object_name = 'blogs'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.all()
        context['datas'] = category
        return context

class MyBlogDetailView(DetailView):
    template_name = 'blogdetail.html'
    model = Blog
    context_object_name = 'blog'
    def context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CreateBlogView(CreateView):
    template_name = 'createblog.html'
    model = Blog
    form_class = MyblogModelForm
    success_url = '/'
    def form_valid(self, form):
        phone = form.cleaned_data['title']
        if len(phone) < 5:
            form.add_error('title', 'Title must be at least 5 characters long')
            return self.form_invalid(form)
        elif len(phone) > 20:
            form.add_error('title', 'Title must be less than 20 characters long')
            return self.form_invalid(form)
        return super().form_valid(form)
    
class UpdateBlogView(CreateView):
    template_name = 'createblog.html'
    model = Blog
    form_class = MyblogModelForm
    success_url = '/'
    def form_valid(self, form):
        phone = form.cleaned_data['title']
        if len(phone) < 5:
            form.add_error('title', 'Title must be at least 5 characters long')
            return self.form_invalid(form)
        elif len(phone) > 20:
            form.add_error('title', 'Title must be less than 20 characters long')
            return self.form_invalid(form)
        return super().form_valid(form)

class DeleteBlogView(DeleteView):
    template_name = 'deleteblog.html'
    model = Blog
    success_url = '/'

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        fm = RegisterForm(request.POST)
        if fm.is_valid():
            fm.save()
            return redirect('/')
        else:
            print(fm.errors)
            return render(request, 'register.html', {'form': fm})
    context = {"form": form}
    return render(request, 'register.html', context)

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/register')
    return render(request, 'login.html')


# ==================== REST API SECTION ====================

# --- 1. Blog API (@api_view သုံးထားသည်) ---
@api_view(['GET', 'POST'])
def blog_list(request):
    if request.method == 'GET':
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def blog_detail(request, pk):
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BlogSerializer(blog)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- 2. PostData API (@api_view သုံးထားသည်) ---
@api_view(["GET", 'POST'])
def postdata_list(request):
    if request.method == 'GET':
        postdata = PostData.objects.all()
        serializer = PostDataSerializer(postdata, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PostDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def postdata_detail(request, pk):
    try:
        postdata = PostData.objects.get(pk=pk)
    except PostData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostDataSerializer(postdata)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = PostDataSerializer(postdata, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        postdata.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Class-based API Views (Extra သင်ယူထားမှုများ)
class PostDataListCreateView(APIView):
    def get(self, request):
        postdata = PostData.objects.all()
        serializer = PostDataSerializer(postdata, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDataDetailView(APIView):
    def get_object(self, pk):
        try:
            return PostData.objects.get(pk=pk)
        except PostData.DoesNotExist:
            return None

    def get(self, request, pk):
        postdata = self.get_object(pk)
        if postdata is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostDataSerializer(postdata)
        return Response(serializer.data)

    def put(self, request, pk):
        postdata = self.get_object(pk)
        if postdata is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostDataSerializer(postdata, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        postdata = self.get_object(pk)
        if postdata is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        postdata.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostDataViewSet(viewsets.ModelViewSet):
    queryset = PostData.objects.all()
    serializer_class = PostDataSerializer


# --- 3. Book API (ViewSet သုံးထားသည်) ---
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer