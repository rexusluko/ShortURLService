from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/create_link/', CreateLinkAPIView.as_view(), name='create_link'),
    path('api/token/', obtain_auth_token, name='api_token'),
    path('api/get_links/', UserLinksAPIView.as_view(), name='get_links'),
    path('api/decode_link/<str:short_url>', DecodeLinkAPIView.as_view(), name='decode_link'),
    path('<str:short_url>/', redirect_original_url, name='redirect_original_url')
]
