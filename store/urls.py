from django.urls import path

from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products',views.ProductViewSet)
router.register('collections',views.CollectionViewSet)

products_routers=routers.NestedDefaultRouter(router,'products',lookup='product')
products_routers.register('reviews',views.ReviewViewSet,basename='product-reviews')

urlpatterns = router.urls + products_routers.urls
