from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from fridges.views import FridgeViewSet
from products.views import ProductViewSet
from wishes.views import WishesViewSet

schema_view = get_schema_view(
   openapi.Info(
      title="Т-ХОЛОД",
      default_version='v1',
      description="Т-ХОЛОД",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = SimpleRouter()
router.register(r'fridges', FridgeViewSet, basename="fridge")

product_router = SimpleRouter()
product_router.register(r'product', ProductViewSet, basename="products")

wishes_router = SimpleRouter()
wishes_router.register(r'wishes', WishesViewSet, basename='wishes')

urlpatterns = [
    path('admin/', admin.site.urls),

    path(r'auth/', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path('', include(wishes_router.urls)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
