# #!/usr/bin/env python
# """
# Simple script to load sample projects into MongoDB
# """

# from portfolio.db import projects_collection
# from datetime import datetime

# def load_sample_projects():
#     """Load sample projects into MongoDB"""
    
#     sample_projects = [
#         {
#             'title': 'E-Commerce Platform',
#             'description': 'A full-featured e-commerce platform with user authentication, product management, and payment integration.',
#             'year': 2024,
#             'technologies': ['Python', 'Django', 'JavaScript', 'React', 'PostgreSQL', 'Stripe'],
#             'live_url': 'https://example-ecommerce.com',
#             'github_url': 'https://github.com/Atik-hridoy/ecommerce-platform',
#             'image_url': 'https://via.placeholder.com/400x250/417690/ffffff?text=E-Commerce',
#             'featured': True,
#             'category': 'web',
#             'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         },
#         {
#             'title': 'Task Management App',
#             'description': 'A mobile-first task management application with real-time collaboration features.',
#             'year': 2023,
#             'technologies': ['React Native', 'Node.js', 'Express', 'MongoDB', 'Socket.io'],
#             'live_url': 'https://taskapp.example.com',
#             'github_url': 'https://github.com/Atik-hridoy/task-management',
#             'image_url': 'https://via.placeholder.com/400x250/28a745/ffffff?text=Task+App',
#             'featured': True,
#             'category': 'mobile',
#             'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         },
#         {
#             'title': 'Weather Dashboard',
#             'description': 'Real-time weather dashboard with location-based forecasts and interactive maps.',
#             'year': 2023,
#             'technologies': ['HTML', 'CSS', 'JavaScript', 'React', 'OpenWeather API', 'Chart.js'],
#             'live_url': 'https://weather-dashboard.example.com',
#             'github_url': 'https://github.com/Atik-hridoy/weather-dashboard',
#             'image_url': 'https://via.placeholder.com/400x250/17a2b8/ffffff?text=Weather',
#             'featured': False,
#             'category': 'web',
#             'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         },
#         {
#             'title': 'Blog Platform',
#             'description': 'A modern blogging platform with markdown support, tags, and user comments.',
#             'year': 2024,
#             'technologies': ['Python', 'Django', 'PostgreSQL', 'Bootstrap', 'JavaScript'],
#             'live_url': 'https://blog.example.com',
#             'github_url': 'https://github.com/Atik-hridoy/blog-platform',
#             'image_url': 'https://via.placeholder.com/400x250/dc3545/ffffff?text=Blog',
#             'featured': False,
#             'category': 'web',
#             'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         },
#         {
#             'title': 'Portfolio Website',
#             'description': 'Personal portfolio website showcasing projects and skills with modern design.',
#             'year': 2024,
#             'technologies': ['HTML', 'CSS', 'JavaScript', 'React', 'Tailwind CSS'],
#             'live_url': 'https://hello-atik.vercel.app',
#             'github_url': 'https://github.com/Atik-hridoy/my_portfolio_backend',
#             'image_url': 'https://via.placeholder.com/400x250/6f42c1/ffffff?text=Portfolio',
#             'featured': True,
#             'category': 'web',
#             'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         }
#     ]
    
#     print("🚀 Loading sample projects into MongoDB...")
    
#     projects_loaded = 0
#     for project in sample_projects:
#         existing = projects_collection.find_one({'title': project['title']})
#         if not existing:
#             projects_collection.insert_one(project)
#             projects_loaded += 1
#             print(f"  ✅ Loaded: {project['title']}")
#         else:
#             print(f"  ⏭️  Skipped (already exists): {project['title']}")
    
#     # Show summary
#     total_projects = projects_collection.count_documents({})
#     print(f"\n📊 Summary:")
#     print(f"  📁 Total projects in database: {total_projects}")
#     print(f"  🆕 New projects loaded: {projects_loaded}")
#     print(f"  ✅ Process completed successfully!")
    
#     return projects_loaded

# if __name__ == "__main__":
#     load_sample_projects()
