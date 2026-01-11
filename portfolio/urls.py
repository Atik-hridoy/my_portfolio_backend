from django.urls import path
from .views import home, get_projects_api, add_project_api, contact_api
from .admin import portfolio_admin

urlpatterns = [
    path("", home),
    path("projects/", get_projects_api),
    path("projects/add/", add_project_api),
    path("contact/", contact_api),
]

# Admin URLs
admin_urls = [
    path('', portfolio_admin.index_view, name='index'),
    path('portfolio-projects/', portfolio_admin.projects_view, name='projects'),
    path('portfolio-projects/add/', portfolio_admin.add_project, name='add_project'),
    path('portfolio-projects/delete/<str:project_title>/', portfolio_admin.delete_project, name='delete_project'),
    path('portfolio-contacts/', portfolio_admin.contacts_view, name='contacts'),
    path('profile/', portfolio_admin.profile_view, name='profile'),
    path('profile/update/', portfolio_admin.update_profile, name='update_profile'),
]
