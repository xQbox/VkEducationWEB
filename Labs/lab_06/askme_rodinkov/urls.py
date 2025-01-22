"""
URL configuration for askme_rodinkov project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from app import views
from django.conf.urls.static import static
from askme_rodinkov import settings 

urlpatterns = [
    path('', views.index, name='index'),
    path('hot-questions/', views.hot_questions, name='hot_questions'),
    path('question/<int:question_id>', views.question, name='question'),
    path('tag/', views.tag, name='tag'),
    path('add-question/', views.add_question, name='add_question'),
    path('register/', views.register, name='register'),
    path('settings/', views.settings, name='settings'),
    path('log-in/', views.log_in, name='log_in'),
    path('log-out/', views.logout, name='log_out'),
    path('admin/', admin.site.urls),
    path('like', views.like, name="like"),
    path('dislike', views.dislike, name="dislike"),
    path('tag/<slug:nameTag>/', views.tag, name='tag'),  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)