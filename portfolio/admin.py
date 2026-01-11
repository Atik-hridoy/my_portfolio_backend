import logging
from django.shortcuts import render, redirect
from django.contrib import admin
from django.contrib import messages
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.urls import path
from datetime import datetime
from .db import projects_collection, contacts_collection

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
            path('profile/', self.admin_view(self.profile_view), name='profile'),
            path('profile/update/', self.admin_view(self.update_profile), name='update_profile'),
        ]
        return custom_urls + urls
    
    @method_decorator(cache_page(300), name='index_view')  # Cache for 5 minutes
    @method_decorator(vary_on_headers('User-Agent'), name='index_view')
    def index_view(self, request):
        # Try to get from cache first
        cache_key = 'admin_dashboard_stats'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.info(f"📊 Dashboard stats loaded from cache")
            projects_count, contacts_count = cached_data
        else:
            # Get fresh data
            projects_count = projects_collection.count_documents({})
            contacts_count = contacts_collection.count_documents({})
            
            # Cache for 5 minutes
            cache.set(cache_key, (projects_count, contacts_count), 300)
            logger.info(f"🎯 Admin dashboard accessed - Projects: {projects_count}, Contacts: {contacts_count}")
        
        return render(request, 'admin/index.html', {
            'projects_count': projects_count,
            'contacts_count': contacts_count,
            'site_header': self.site_header,
            'site_title': self.site_title,
            'has_permission': True
        })
    
    @method_decorator(cache_page(600), name='projects_view')  # Cache for 10 minutes
    def projects_view(self, request):
        # Try to get from cache first
        cache_key = 'admin_projects_list'
        cached_projects = cache.get(cache_key)
        
        if cached_projects:
            projects = cached_projects
            logger.info(f"📋 Projects list loaded from cache")
        else:
            # Get fresh data with projection for performance
            projects = list(projects_collection.find(
                {"_id": 0}, 
                {"title": 1, "category": 1, "year": 1, "featured": 1, "created_at": 1, "technologies": 1, "live_url": 1, "github_url": 1, "image_url": 1, "description": 1}
            ))
            
            # Sort by creation date (newest first)
            projects.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            
            # Cache for 10 minutes
            cache.set(cache_key, projects, 600)
            logger.info(f"📋 Projects list viewed - Total projects: {len(projects)}")
            for i, project in enumerate(projects):
                logger.info(f"  📁 {i+1}. {project.get('title', 'Unknown')}")
                logger.info(f"     📱 Category: {project.get('category', 'Unknown')}")
                logger.info(f"     📅 Year: {project.get('year', 'Unknown')}")
                logger.info(f"     ⭐ Featured: {project.get('featured', False)}")
                logger.info(f"     🛠️ Techs: {len(project.get('technologies', []))} technologies")
                logger.info(f"     🔗 Live URL: {'Yes' if project.get('live_url') else 'No'}")
                logger.info(f"     💻 GitHub: {'Yes' if project.get('github_url') else 'No'}")
                logger.info(f"     📝 Description: {'Yes' if project.get('description') else 'No'}")
        
        # Debug: Check if projects are being passed to template
        logger.info(f"🔍 DEBUG: Passing {len(projects)} projects to template")
        for i, project in enumerate(projects[:3]):  # Log first 3 projects
            logger.info(f"🔍 DEBUG: Project {i+1}: {project.get('title', 'No title')} - Fields: {list(project.keys())}")
        
        return render(request, 'admin/projects.html', {
            'projects': projects,
            'site_header': self.site_header,
            'has_permission': True
        })
    
    def add_project(self, request):
        if request.method == 'POST':
            # Clear cache when new project is added
            cache.delete('admin_projects_list')
            cache.delete('admin_dashboard_stats')
            
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
        # Clear cache when project is deleted
        cache.delete('admin_projects_list')
        cache.delete('admin_dashboard_stats')
        
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
    
    @method_decorator(cache_page(900), name='profile_view')  # Cache for 15 minutes
    def profile_view(self, request):
        # Try to get from cache first
        cache_key = 'admin_profile_data'
        cached_profile = cache.get(cache_key)
        
        if cached_profile:
            profile = cached_profile
            logger.info(f"👤 Profile data loaded from cache")
        else:
            # Get or create profile data
            profile = contacts_collection.find_one({'type': 'profile'})
            
            if not profile:
                profile = {
                    'name': 'Atik Hridoy',
                    'title': 'Full Stack Developer',
                    'bio': 'Passionate developer with expertise in modern web technologies.',
                    'email': 'atik.hridoy.00@gmail.com',
                    'phone': '+8801234567890',
                    'location': 'Dhaka, Bangladesh',
                    'github': 'https://github.com/Atik-hridoy',
                    'linkedin': 'https://linkedin.com/in/atik-hridoy',
                    'website': 'https://atik-hridoy.com',
                    'skills': ['Python', 'Django', 'JavaScript', 'React', 'MongoDB'],
                    'experience_years': '3+',
                    'available_for_hire': True,
                    'profile_image': 'https://via.placeholder.com/150x150/417690/ffffff?text=AH'
                }
                contacts_collection.insert_one(profile)
            
            # Cache for 15 minutes
            cache.set(cache_key, profile, 900)
            logger.info(f"\033[94m👤\033[0m Profile viewed - Name: \033[93m{profile.get('name', 'Unknown')}\033[0m")
        
        return render(request, 'admin/profile.html', {
            'profile': profile,
            'site_header': self.site_header,
            'has_permission': True
        })
    
    def update_profile(self, request):
        if request.method == 'POST':
            # Clear cache when profile is updated
            cache.delete('admin_profile_data')
            
            profile_data = {
                'name': request.POST.get('name', ''),
                'title': request.POST.get('title', ''),
                'bio': request.POST.get('bio', ''),
                'email': request.POST.get('email', ''),
                'phone': request.POST.get('phone', ''),
                'location': request.POST.get('location', ''),
                'github': request.POST.get('github', ''),
                'linkedin': request.POST.get('linkedin', ''),
                'website': request.POST.get('website', ''),
                'skills': request.POST.getlist('skills', []),
                'experience_years': request.POST.get('experience_years', ''),
                'available_for_hire': request.POST.get('available_for_hire') == 'on',
                'profile_image': request.POST.get('profile_image', ''),
                'type': 'profile',
                'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Handle CV file upload
            if 'cv_file' in request.FILES:
                cv_file = request.FILES['cv_file']
                
                # Create CV upload directory if it doesn't exist
                import os
                cv_upload_dir = os.path.join('media', 'cv')
                os.makedirs(cv_upload_dir, exist_ok=True)
                
                # Save CV file
                cv_filename = f"cv_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{cv_file.name}"
                cv_file_path = os.path.join(cv_upload_dir, cv_filename)
                
                # Write file to disk
                with open(cv_file_path, 'wb+') as destination:
                    for chunk in cv_file.chunks():
                        destination.write(chunk)
                
                # Store file path in database
                profile_data['cv_file'] = f"/media/cv/{cv_filename}"
                profile_data['cv_filename'] = cv_file.name
                profile_data['cv_file_size'] = f"{cv_file.size / 1024 / 1024:.2f} MB"
                profile_data['cv_file_type'] = cv_file.content_type
                
                logger.info(f"\033[94m📄\033[0m CV uploaded: \033[93m{cv_file.name}\033[0m ({cv_file.size / 1024 / 1024:.2f} MB)")
                logger.info(f"\033[94m💾\033[0m CV saved to: \033[93m{cv_file_path}\033[0m")
            
            logger.info(f"\033[92m🚀\033[0m Updating profile: \033[94m{profile_data['name']}\033[0m")
            logger.info(f"\033[94m📧\033[0m Email: \033[93m{profile_data['email']}\033[0m")
            logger.info(f"\033[94m💼\033[0m Title: \033[93m{profile_data['title']}\033[0m")
            logger.info(f"\033[94m🛠️\033[0m Skills: \033[93m{', '.join(profile_data['skills'])}\033[0m")
            logger.info(f"\033[94m📍\033[0m Location: \033[93m{profile_data['location']}\033[0m")
            logger.info(f"\033[94m🕐\033[0m Updated at: \033[93m{profile_data['updated_at']}\033[0m")
            
            try:
                contacts_collection.update_one(
                    {'type': 'profile'},
                    {'$set': profile_data},
                    upsert=True
                )
                logger.info(f"\033[92m✅\033[0m Profile updated successfully!")
                messages.success(request, f'\033[92m🎉\033[0m Profile "{profile_data["name"]}" updated successfully!')
                return redirect('/portfolio-admin/profile/')
            except Exception as e:
                logger.error(f"\033[91m❌\033[0m Error updating profile: \033[31m{str(e)}\033[0m")
                messages.error(request, f'\033[91m❌\033[0m Error updating profile: {str(e)}')
        
        # Get current profile for form
        profile = contacts_collection.find_one({'type': 'profile'})
        
        return render(request, 'admin/update_profile.html', {
            'profile': profile,
            'site_header': self.site_header,
            'has_permission': True
        })

# Create custom admin instance
portfolio_admin = CustomAdminSite(name='portfolio_admin')
