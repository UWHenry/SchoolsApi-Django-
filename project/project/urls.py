"""
URL configuration for project project.

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
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework import routers, permissions
from api import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

swagger_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1',
      description="API description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

api_router = routers.DefaultRouter(trailing_slash=False)
api_router.register("schools", views.SchoolViewSet)
api_router.register("administrators", views.AdministratorViewSet)
api_router.register("teachers", views.TeacherViewSet)
api_router.register("students", views.StudentViewSet)
api_router.register("courses", views.CourseViewSet)

urlpatterns =  [
    path('', RedirectView.as_view(url='api/')),
    path('admin/', admin.site.urls),
    path('api/', include(api_router.urls)),
    path('api/transfer', views.transfer, name="transfer"),
    path('swagger<format>/', swagger_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', swagger_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', swagger_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)