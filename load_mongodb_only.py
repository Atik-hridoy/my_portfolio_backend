#!/usr/bin/env python
"""
Load projects only from MongoDB - no external URLs
"""

from portfolio.db import projects_collection
from datetime import datetime

def load_mongodb_projects():
    """Load projects with only MongoDB data - no external URLs"""
    
    # Clear existing projects first
    projects_collection.delete_many({})
    print("🗑️ Cleared existing projects from MongoDB")
    
    mongodb_projects = [
        {
            'title': 'E-Commerce Platform',
            'description': 'A full-featured e-commerce platform with user authentication, product management, and payment integration using MongoDB for data storage.',
            'year': 2024,
            'technologies': ['Python', 'Django', 'JavaScript', 'React', 'MongoDB', 'Stripe'],
            'live_url': '',  # No external URL
            'github_url': '',  # No external URL
            'image_url': '/static/images/ecommerce-platform.jpg',  # Local image
            'featured': True,
            'category': 'web',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            'title': 'Task Management App',
            'description': 'A mobile-first task management application with real-time collaboration features using MongoDB as the primary database.',
            'year': 2023,
            'technologies': ['React Native', 'Node.js', 'Express', 'MongoDB', 'Socket.io'],
            'live_url': '',  # No external URL
            'github_url': '',  # No external URL
            'image_url': '/static/images/task-management.jpg',  # Local image
            'featured': True,
            'category': 'mobile',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            'title': 'Weather Dashboard',
            'description': 'Real-time weather dashboard with location-based forecasts and interactive maps. Data stored and managed in MongoDB.',
            'year': 2023,
            'technologies': ['HTML', 'CSS', 'JavaScript', 'React', 'MongoDB', 'Chart.js'],
            'live_url': '',  # No external URL
            'github_url': '',  # No external URL
            'image_url': '/static/images/weather-dashboard.jpg',  # Local image
            'featured': False,
            'category': 'web',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            'title': 'Blog Platform',
            'description': 'A modern blogging platform with markdown support, tags, and user comments. All content managed through MongoDB.',
            'year': 2024,
            'technologies': ['Python', 'Django', 'MongoDB', 'Bootstrap', 'JavaScript'],
            'live_url': '',  # No external URL
            'github_url': '',  # No external URL
            'image_url': '/static/images/blog-platform.jpg',  # Local image
            'featured': False,
            'category': 'web',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            'title': 'Portfolio Admin System',
            'description': 'Professional admin panel for portfolio management with MongoDB backend, caching, and performance optimizations.',
            'year': 2024,
            'technologies': ['Python', 'Django', 'MongoDB', 'JavaScript', 'CSS', 'HTML'],
            'live_url': '',  # No external URL
            'github_url': '',  # No external URL
            'image_url': '/static/images/portfolio-admin.jpg',  # Local image
            'featured': True,
            'category': 'web',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            'title': 'MongoDB Data Analytics',
            'description': 'Data analytics dashboard with MongoDB aggregation pipelines and real-time data visualization.',
            'year': 2024,
            'technologies': ['Python', 'Django', 'MongoDB', 'Chart.js', 'JavaScript'],
            'live_url': '',  # No external URL
            'github_url': '',  # No external URL
            'image_url': '/static/images/analytics-dashboard.jpg',  # Local image
            'featured': False,
            'category': 'web',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            'title': 'API Gateway Service',
            'description': 'RESTful API gateway with MongoDB for request logging, rate limiting, and service management.',
            'year': 2023,
            'technologies': ['Node.js', 'Express', 'MongoDB', 'Redis', 'Docker'],
            'live_url': '',  # No external URL
            'github_url': '',  # No external URL
            'image_url': '/static/images/api-gateway.jpg',  # Local image
            'featured': True,
            'category': 'web',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    ]
    
    print("🚀 Loading MongoDB-only projects...")
    
    projects_loaded = 0
    for project in mongodb_projects:
        projects_collection.insert_one(project)
        projects_loaded += 1
        print(f"  ✅ Loaded: {project['title']}")
        print(f"     📝 Description: {project['description'][:50]}...")
        print(f"     🛠️ Technologies: {', '.join(project['technologies'])}")
        print(f"     ⭐ Featured: {project['featured']}")
        print("")
    
    # Show summary
    total_projects = projects_collection.count_documents({})
    print(f"📊 Summary:")
    print(f"  📁 Total projects in MongoDB: {total_projects}")
    print(f"  🆕 New projects loaded: {projects_loaded}")
    print(f"  🔗 External URLs: None (MongoDB only)")
    print(f"  ✅ Process completed successfully!")
    
    return projects_loaded

if __name__ == "__main__":
    load_mongodb_projects()
