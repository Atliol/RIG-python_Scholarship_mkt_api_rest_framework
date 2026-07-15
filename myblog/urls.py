from django.contrib import admin
from django.urls import path, include
from mytask import views
from rest_framework import routers

# ViewSet တွေအတွက် Router ချိတ်ဆက်ခြင်း
router = routers.DefaultRouter()
# Book အတွက် ViewSet (အိမ်စာအရ အသုံးပြုရန်)
router.register('books', views.BookViewSet, basename='book')
# PostData အတွက် ViewSet (Day 8 မှာ စမ်းသပ်ရန် ချန်ထားပေးပါသည်)
router.register('posts', views.PostDataViewSet, basename='post')

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),
    
    # HTML Views (Day 1 to 6)
    path('', views.homepage, name='home'),
    path('about/', views.about, name='about'),
    path('creat/', views.createblog, name='createblog'),
    path('save_blog/', views.save_blog, name='save_blog'),
    path('filterblog/', views.filter_blog, name='filterblog'),
    path('detail/<int:blogid>/', views.detail_blog, name='detail'),
    path('createblog/', views.createblog, name='createblog_form'),
    path('blogtemplate/', views.MyBlogTemplateView.as_view(), name='blogtemplate'),
    path('blogdetail/<int:pk>/', views.MyBlogDetailView.as_view(), name='blogdetail'),
    path('createblogview/', views.CreateBlogView.as_view(), name='createblogview'),
    
    # User Authentication
    path('register/', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path("api-auth/", include("rest_framework.urls")),

    # ==================== REST API SECTION ====================
    
    # ၁။ Blog API (@api_view သုံးထားသော Function-based Views)
    path('api/blogs/', views.blog_list, name='blog-list'),
    path('api/blogs/<int:pk>/', views.blog_detail, name='blog-detail'),

    # ၂။ PostData API (@api_view သုံးထားသော Function-based Views)
    path('api/postdata/', views.postdata_list, name='postdata_list'),
    path('api/postdata/<int:pk>/', views.postdata_detail, name='postdata_detail'),
    
    # ၃။ Book API (ViewSet သုံးထားသော Class-based Views)
    path('api/', include(router.urls)), # ဤလမ်းကြောင်းအောက်တွင် api/books/ ရရှိပါမည်
    
    # Extra: Class-based API View အဟောင်းများ စမ်းသပ်လိုပါက
    path('api/postdata-cbv/', views.PostDataListCreateView.as_view(), name='PostDataListCreateView'),
    path('api/myblog-view/', views.MyBlogView.as_view()),
    
    # App-level urls.py ကို စနစ်တကျ ချိတ်ဆက်ထားခြင်း
    path('blog/', include('mytask.urls')),
]