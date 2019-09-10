"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from main import views
urlpatterns = [
    path('summernote/', include('django_summernote.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('transfer1/', views.transferview1),
    path('transfer2/', views.transferview2.as_view()),

    url(r'^$', views.main_logo_pageView.as_view(), name='main_logo_page'),
    url('main/', views.mainView.as_view(), name='main'),
    url('signup_1/', views.signup_1View.as_view(), name='signup_1'),
    url('signup_2/', views.signup_2View.as_view(), name='signup_2'),
    url('login_1/', views.login_1View.as_view(), name='login_1'),
    url('login_2/', views.login_2View.as_view(), name='login_2'),
    url('subscribe_1/', views.subscribe_1View.as_view(), name='subscribe_1'),
    url('subscribe_2/', views.subscribe_2View.as_view(), name='subscribe_2'),
    url('subscribe_3/', views.subscribe_3View.as_view(), name='subscribe_3'),

    url('creator/', views.creatorView.as_view(), name='creator'),
    url('channel/', views.channelView.as_view(), name='channel'),
    url('video/', views.videoView.as_view(), name='video'),
    url('notice/', views.noticeView.as_view(), name='notice'),
    url('help/', views.helpView.as_view(), name='help'),
    url('account/', views.accountView.as_view(), name='account'),
    url('inquiry_new/', views.inquiry_newView, name='inquiry_new'),
    url('inquiry/', views.inquiryView.as_view(), name='inquiry'),
    url('inquiry_detail/', views.inquiry_detailView.as_view(), name='inquiry_detail'),
)