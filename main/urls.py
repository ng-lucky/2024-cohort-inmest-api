from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'queries', QueryModelViewSet, basename='queries')
router.register(r'classes', ClassModelViewset, basename='classes')

urlpatterns = [
    path("say_hello/", say_hello),
    path("profile/", user_profile),
    path("filter_queries/<int:query_id>/", filter_queries),
    path('', include(router.urls)),
    path("queries/", QueryView.as_view(), name="query-view"),
    path("schedules/fetch/", fetch_class_schedules),
    path("schedules/create/", create_class_schedule)
]
