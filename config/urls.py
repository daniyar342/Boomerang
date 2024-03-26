
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.contrib import admin
from django.urls import path,include
import debug_toolbar
urlpatterns = [
    path("admin/", admin.site.urls),
    path("product/",include('product.urls')),
    path("application/",include('applications.urls')),
    path("user/",include('user_profiles.urls')),
    
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",),
    path('__debug__/', include(debug_toolbar.urls)),
]
