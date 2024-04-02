"""
URL configuration for CampusSync project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include, re_path
from event import urls as event_urls
from user import urls as user_urls
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls.static import static
from django.conf import settings




schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('event/', include(event_urls)), 
    path('user/', include(user_urls)), 
    re_path(r'^$', schema_view, name='swagger'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
