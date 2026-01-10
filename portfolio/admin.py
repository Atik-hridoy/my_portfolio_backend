from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages
from .db import projects_collection, contacts_collection
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger('portfolio.admin')

# Custom Admin Views
class CustomAdminSite(admin.AdminSite):
    site_header = " Portfolio Admin"
    site_title = "Portfolio Admin Portal"
    index_title = "Welcome to Portfolio Admin Portal"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_view(self.index_view), name='index'),
            path('portfolio-projects/', self.admin_view(self.projects_view), name='projects'),
            path('portfolio-projects/add/', self.admin_view(self.add_project), name='add_project'),
            path('portfolio-projects/delete/<str:project_title>/', self.admin_view(self.delete_project), name='delete_project'),
            path('portfolio-contacts/', self.admin_view(self.contacts_view), name='contacts'),
        ]
        return custom_urls + urls
    
    def index_view(self, request):
        projects_count = projects_collection.count_documents({})
        contacts_count = contacts_collection.count_documents({})
        
        logger.info(f"🎯 Admin dashboard accessed - Projects: {projects_count}, Contacts: {contacts_count}")
        
        return render(request, 'admin/index.html', {
            'projects_count': projects_count,
            'contacts_count': contacts_count,
            'site_header': self.site_header,
            'site_title': self.site_title,
            'has_permission': True
        })
    
    def projects_view(self, request):
        projects = list(projects_collection.find({}, {"_id": 0}))
        
        logger.info(f"📋 Projects list viewed - Total projects: {len(projects)}")
        for project in projects:
            logger.info(f"  📁 {project.get('title', 'Unknown')}")
            logger.info(f"  📱 Category: {project.get('category', 'Unknown')}")
            logger.info(f"  📅 Year: {project.get('year', 'Unknown')}")
            logger.info(f"  ⭐ Featured: {project.get('featured', False)}")
        
        return render(request, 'admin/projects.html', {
            'projects': projects,
            'site_header': self.site_header,
            'has_permission': True
        })
    
    def add_project(self, request):
        if request.method == 'POST':
            technologies = request.POST.get('technologies', '').split(',')
            technologies = [tech.strip() for tech in technologies if tech.strip()]
            
            project_data = {
                'title': request.POST.get('title'),
                'description': request.POST.get('description'),
                'year': int(request.POST.get('year', 2024)),
                'technologies': technologies,
                'live_url': request.POST.get('live_url'),
                'github_url': request.POST.get('github_url'),
                'image_url': request.POST.get('image_url'),
                'featured': request.POST.get('featured') == 'on',
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'category': request.POST.get('category', 'web')
            }
            
            # Log project creation with colors
            logger.info(f"\033[92m🚀\033[0m Creating new project: \033[94m{project_data['title']}\033[0m")
            logger.info(f"\033[94m📁\033[0m Technologies: \033[93m{', '.join(technologies)}\033[0m")
            logger.info(f"\033[94m🔗\033[0m Live URL: \033[93m{project_data['live_url']}\033[0m")
            logger.info(f"\033[94m📱\033[0m Category: \033[93m{project_data['category']}\033[0m")
            logger.info(f"\033[94m⭐\033[0m Featured: \033[93m{project_data['featured']}\033[0m")
            logger.info(f"\033[94m🕐\033[0m Created at: \033[93m{project_data['created_at']}\033[0m")
            
            try:
                result = projects_collection.insert_one(project_data)
                logger.info(f"\033[92m✅\033[0m Project '\033[94m{project_data['title']}\033[0m' added successfully with ID: \033[93m{result.inserted_id}\033[0m")
                messages.success(request, f'\033[92m🎉\033[0m Project "{project_data["title"]}" added successfully at {project_data["created_at"]}!')
                return redirect('/portfolio-admin/portfolio-projects/')
            except Exception as e:
                logger.error(f"\033[91m❌\033[0m Error adding project: \033[31m{str(e)}\033[0m")
                messages.error(request, f'\033[91m❌\033[0m Error adding project: {str(e)}')
        
        logger.info(f"\033[94m📝\033[0m Add project form accessed")
        return render(request, 'admin/add_project.html', {
            'site_header': self.site_header,
            'has_permission': True
        })
    
    def delete_project(self, request, project_title):
        logger.info(f"\033[91m🗑️\033[0m Attempting to delete project: \033[94m{project_title}\033[0m")
        
        try:
            result = projects_collection.delete_one({'title': project_title})
            if result.deleted_count > 0:
                logger.info(f"\033[92m✅\033[0m Project '\033[94m{project_title}\033[0m' deleted successfully")
                messages.success(request, f'Project "{project_title}" deleted successfully!')
            else:
                logger.warning(f"\033[93m⚠️\033[0m Project '\033[94m{project_title}\033[0m' not found for deletion")
                messages.warning(request, f'Project "{project_title}" not found!')
        except Exception as e:
            logger.error(f"\033[91m❌\033[0m Error deleting project: \033[31m{str(e)}\033[0m")
            messages.error(request, f'Error deleting project: {str(e)}')
        
        return redirect('/portfolio-admin/portfolio-projects/')
    
    def contacts_view(self, request):
        contacts = list(contacts_collection.find({}, {"_id": 0}))
        
        logger.info(f"\033[94m📧\033[0m Contacts list viewed - Total contacts: \033[93m{len(contacts)}\033[0m")
        for contact in contacts:
            logger.info(f"  👤 {contact.get('name', 'Unknown')} (\033[93m{contact.get('email', 'Unknown')}\033[0m)")
        
        return render(request, 'admin/contacts.html', {
            'contacts': contacts,
            'site_header': self.site_header,
            'has_permission': True
        })

# Create custom admin instance
portfolio_admin = CustomAdminSite(name='portfolio_admin')
