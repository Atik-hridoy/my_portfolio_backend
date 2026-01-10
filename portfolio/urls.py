from django.urls import path
from .views import home, get_projects_api, add_project_api, contact_api

urlpatterns = [
    path("", home),
    path("projects/", get_projects_api),
    path("projects/add/", add_project_api),
    path("contact/", contact_api),
]
