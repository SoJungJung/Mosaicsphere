"""
URL configuration for MosaicSphere project.

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
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),  # Ensure consistency with trailing slashes
    path('', views.main, name='main'),  # Corrected for root URL
    path('collage/', views.collage, name='collage'),  # Ensure consistency with trailing slashes
    path('hall/', views.hall, name='hall'),  # Ensure consistency with trailing slashes
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

