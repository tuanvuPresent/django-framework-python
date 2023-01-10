"""Example URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from graphene_django.views import GraphQLView
from rest_framework import permissions
from django.conf.urls.static import static
from apps.sample.schema import schema
from django.conf import settings

schema_view = get_schema_view(openapi.Info(
    title="MANAGER_API",
    default_version='v1',
    description="Test",
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="contact@snippets.local"),
    license=openapi.License(name="BSD License"),
),
    url='https://8000-tuanvuprese-djangoframe-mfdrjg9l8lz.ws-us81.gitpod.io',
    public=True,
    permission_classes=(permissions.AllowAny,), )


urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url('admin/', admin.site.urls),
    
    url('api/', include('apps.urls')),

    url(r'^silk/', include('silk.urls', namespace='silk')),
    url('admin/log_viewer/', include('log_viewer.urls')),
    url("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
