from rest_framework import routers
from .auth_viewset import AuthenticationViewSet
from .category_viewset import CategoryViewSet
from .blogs_viewset import BlogsViewset
from . contact_viewset import ContactViewset

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'auth', AuthenticationViewSet, basename='auth')
router.register(r'category',CategoryViewSet,basename='category')
router.register(r'blogs',BlogsViewset,basename='blogs')
router.register(r'contact',ContactViewset,basename='contact')

urlpatterns = router.urls
