from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'books', views.BookViewSet, basename='book')
router.register(r'postsets', views.PostDataViewSet, basename='postset') # ViewSet စမ်းချင်ရင်သုံးရန်

urlpatterns = [
    # 1. Blog API endpoints (@api_view)
    path('api/blogs/', views.blog_list, name='blog-list'),
    path('api/blogs/<int:pk>/', views.blog_detail, name='blog-detail'),

    # 2. PostData API endpoints (@api_view)
    path('api/postdata/', views.postdata_list, name='postdata-list'),
    path('api/postdata/<int:pk>/', views.postdata_detail, name='postdata-detail'),

    # 3. Book ViewSet & Router endpoints
    path('api/', include(router.urls)),
]