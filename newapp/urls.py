# from django.urls import path,include
# from .import views
# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register(r'users', views.UserViewSet, basename='user')
# router.register(r'yourmodels', views.newuserviewSet)
# urlpatterns = [
#     path('check/', views.check),
#     path('create_student/', views.create_student),
#     path('create_marks/', views.create_marks),
#     path('data_retrive/', views.data_retrive),
#     path('api/', include(router.urls)),
# ]


from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# Create routers for both UserViewSet and newuserviewSet
user_router = DefaultRouter()
user_router.register(r'users', views.UserViewSet, basename='user')

yourmodels_router = DefaultRouter()
yourmodels_router.register(r'yourmodels', views.newuserviewSet, basename='yourmodel')

urlpatterns = [
    path('check/', views.check),
    path('create_student/', views.create_student),
    path('create_marks/', views.create_marks),
    path('data_retrive/', views.data_retrive),
    
    # Include the URLs for both ViewSets
    path('api/', include(user_router.urls)),
    path('api/', include(yourmodels_router.urls)),
    path('api/newuserviewset/<int:pk>/update-student/', views.newuserviewSet.as_view({'put': 'update_student'}), name='update-student'),
    path('api/yourmodels/<int:pk>/get_student/', views.newuserviewSet.as_view({'get': 'get_student'}), name='get-student'),
]
