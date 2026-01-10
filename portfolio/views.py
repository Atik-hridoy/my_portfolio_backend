from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .db import projects_collection, contacts_collection

def home(request):
    """Render the portfolio UI"""
    return render(request, 'index.html')

# MongoDB API Views
def get_projects_api(request):
    """API endpoint to get all portfolio projects"""
    projects = list(projects_collection.find({}, {"_id": 0}))
    return JsonResponse({"projects": projects})

@csrf_exempt
@require_http_methods(["POST"])
def add_project_api(request):
    """API endpoint to add new portfolio project"""
    try:
        data = json.loads(request.body)
        
        project = {
            "title": data.get("title", ""),
            "description": data.get("description", ""),
            "year": data.get("year", 2024),
            "technologies": data.get("technologies", []),
            "live_url": data.get("live_url", ""),
            "github_url": data.get("github_url", ""),
            "image_url": data.get("image_url", ""),
            "featured": data.get("featured", False),
            "created_at": data.get("created_at", ""),
            "category": data.get("category", "web")
        }
        
        result = projects_collection.insert_one(project)
        return JsonResponse({
            "message": "Project added successfully",
            "project_id": str(result.inserted_id)
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def contact_api(request):
    """API endpoint to handle contact form submissions"""
    try:
        data = json.loads(request.body)
        
        contact_data = {
            "name": data.get("name", ""),
            "email": data.get("email", ""),
            "message": data.get("message", ""),
            "timestamp": data.get("timestamp", "")
        }
        
        contacts_collection.insert_one(contact_data)
        return JsonResponse({"status": "success", "message": "Contact form submitted"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
