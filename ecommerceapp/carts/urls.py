from rest_framework import routers

from . import viewset

router = routers.DefaultRouter()
router.register("", viewset.CartsViewset, basename="carts")

urlpatterns = router.urls
