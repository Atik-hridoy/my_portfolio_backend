# My Portfolio

A modern Django-based portfolio website with MongoDB backend and responsive UI.

## Features

- 🎨 **Modern UI** - Responsive design with Tailwind CSS
- 📱 **Mobile Friendly** - Works on all devices
- 🚀 **Dynamic Projects** - Projects loaded from MongoDB
- 📧 **Contact Form** - Working contact form with email integration
- 🔄 **RESTful API** - Clean API endpoints for data management
- 🎯 **No Authentication** - Public portfolio website

## Tech Stack

- **Backend**: Django 6.0.1
- **Database**: MongoDB with PyMongo
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **API**: Custom Django REST API
- **Deployment**: Ready for production

## Installation

1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env` file and update with your settings
   - Configure MongoDB connection string

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Visit your portfolio: **http://127.0.0.1:8000/**

## API Endpoints

### Public Endpoints (No Authentication Required)

- `GET /` - Portfolio homepage (UI)
- `GET /api/projects/` - Get all portfolio projects
- `POST /api/projects/add/` - Add new project (for admin use)
- `POST /api/contact/` - Submit contact form

### Project Data Structure
```json
{
  "title": "Project Title",
  "description": "Project description",
  "tech_stack": ["Django", "React", "MongoDB"],
  "live_url": "https://example.com",
  "github_url": "https://github.com/user/project",
  "image_url": "https://example.com/image.jpg",
  "featured": true,
  "created_at": "2024-01-10",
  "category": "web"
}
```

## Adding Projects

### Method 1: Using API
```bash
curl -X POST http://127.0.0.1:8000/api/projects/add/ \
-H "Content-Type: application/json" \
-d '{
  "title": "My Project",
  "description": "Project description",
  "tech_stack": ["Django", "React"],
  "live_url": "https://example.com",
  "github_url": "https://github.com/user/project"
}'
```

### Method 2: Using MongoDB Directly
```python
from portfolio.db import projects_collection

project = {
    "title": "My Project",
    "description": "Project description",
    "tech_stack": ["Django", "React"],
    "live_url": "https://example.com",
    "github_url": "https://github.com/user/project"
}

projects_collection.insert_one(project)
```

## Project Structure

```
my_portfolio/
├── .env                    # Environment variables
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── my_portfolio/          # Main Django project
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── portfolio/             # Portfolio app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── urls.py
│   ├── views.py
│   ├── db.py              # MongoDB connection
│   ├── models.py
│   ├── serializers.py
│   ├── utils.py
│   └── tests.py
├── templates/             # HTML templates
│   └── index.html         # Main portfolio UI
└── static/               # Static assets (CSS, JS, images)
```

## MongoDB Collections

- **projects** - Portfolio projects data
- **contacts** - Contact form submissions

## Customization

### Update Personal Information
Edit `templates/index.html` to update:
- Your name in hero section
- About section content
- Skills and technologies
- Social media links

### Add Custom Styling
- Modify CSS classes in `templates/index.html`
- Add custom CSS in `static/css/`
- Update color scheme (currently blue/gray theme)

## Deployment

### Production Setup
1. Set `DEBUG=False` in settings
2. Configure `ALLOWED_HOSTS`
3. Set up production MongoDB
4. Configure static files serving
5. Use Gunicorn/Uvicorn for WSGI

### Environment Variables
```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com
MONGODB_URI=mongodb://your-production-db
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Create an issue on GitHub
- Use the contact form on the website
- Email: your-email@example.com
