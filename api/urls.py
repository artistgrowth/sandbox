from django.urls import include, path
from rest_framework import routers
from . import custome_router
from . import views

router = custome_router.PatchRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"questions", views.QuestionViewSet)
router.register(r"choices", views.ChoiceViewSet)

# app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
    #path("questions/", views.QuestionViewSet.as_view(actions={'get': 'list', 'post': 'create'}), name="api-question"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework"))
]
