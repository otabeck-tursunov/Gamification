from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from main import views

schema_view = get_schema_view(
    openapi.Info(
        title="Codial Gamification App's API",
        default_version='v1',
        description="Codial Gamification App's API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="otabekpm@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += [
    # Course URLs
    path('courses/', views.CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', views.CourseRetrieveUpdateDestroyView.as_view(), name='course-retrieve-update-destroy'),

    # CustomUser URLs
    # path('users/', views.CustomUserListCreateView.as_view(), name='user-list-create'),
    # path('users/<int:pk>/', views.CustomUserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),

    # Mentor URLs
    path('mentors/', views.MentorListCreateView.as_view(), name='mentor-list-create'),
    path('mentors/<int:pk>/', views.MentorRetrieveUpdateDestroyView.as_view(), name='mentor-retrieve-update-destroy'),

    # Group URLs
    path('groups/', views.GroupListCreateView.as_view(), name='group-list-create'),
    path('groups/<int:pk>/', views.GroupRetrieveUpdateDestroyView.as_view(), name='group-retrieve-update-destroy'),

    # Student URLs
    path('students/', views.StudentListCreateView.as_view(), name='student-list-create'),
    path('students/<int:pk>/', views.StudentRetrieveUpdateDestroyView.as_view(),
         name='student-retrieve-update-destroy'),

    # PointType URLs
    path('point-types/', views.PointTypeListCreateView.as_view(), name='point-type-list-create'),
    path('point-types/<int:pk>/', views.PointTypeRetrieveUpdateDestroyView.as_view(),
         name='point-type-retrieve-update-destroy'),

    # GivePoint URLs
    path('give-points/', views.GivePointListCreateView.as_view(), name='give-point-list-create'),
    path('give-points/<int:pk>/', views.GivePointRetrieveUpdateDestroyView.as_view(),
         name='give-point-retrieve-update-destroy'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
