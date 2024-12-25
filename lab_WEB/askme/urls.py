"""
URL configuration for askme project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
import blog.views

urlpatterns = [
    # path("__debug__/", include("debug_toolbar.urls")),

    path('admin/', admin.site.urls),
    path('', blog.views.new, name="main-view"),
    path('hot', blog.views.hot, name="top-questions"),
    path('tag/<slug:tag>', blog.views.tag, name="tag-search"),
    path('question/<int:id>', blog.views.question, name="question-info"),
    # path('question/<int:id>/answer', blog.views.answer, name="new-answer"),
    path('login', blog.views.login, name="login-page"),
    path('signup', blog.views.signup, name="signup-page"),
    path('ask', blog.views.ask, name="ask-question"),
    path('settings', blog.views.settings, name="user-settings"),
    path('logout', blog.views.logout, name="logout"),
    path('like', blog.views.like, name="like"),
    path('dislike', blog.views.dislike, name="dislike"),
    path('status', blog.views.status, name="status"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
