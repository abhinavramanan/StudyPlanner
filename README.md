# 📚 StudyPlanner

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**StudyPlanner** is an intelligent study planning application that leverages Google's Gemini AI to create personalized study schedules. Transform your learning goals into structured, time-managed study plans with AI-powered recommendations.

## ✨ Features

- **🤖 AI-Powered Planning**: Generate intelligent study schedules using Google Gemini AI
- **📋 Task Management**: Add, organize, and track your study tasks with different priority levels
- **📅 Calendar View**: Visualize your study plan in an easy-to-read timeline format
- **🏷️ Task Types**: Support for different task types (Normal, Priority, Weekly, Daily)
- **📊 Status Tracking**: Monitor progress with Pending, In Progress, and Completed statuses
- **📱 Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **🎨 Modern UI**: Clean, intuitive interface built with Bootstrap 5

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/abhinavramanan/StudyPlanner.git
   cd StudyPlanner
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file and add your configuration:
   ```env
   SECRET_KEY=your-django-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   GEMINI_API_KEY=your-gemini-api-key-here
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Open your browser** and navigate to `http://localhost:8000`

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Django secret key for security | Yes | - |
| `DEBUG` | Enable/disable debug mode | No | `True` |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | No | `localhost,127.0.0.1` |
| `GEMINI_API_KEY` | Google Gemini AI API key | Yes | - |

### Getting a Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key and add it to your `.env` file

## 📖 Usage

### Adding Tasks

1. **Navigate to the home page** at `http://localhost:8000`
2. **Fill in the task form**:
   - Task Description: What you need to study
   - Due Date: When the task should be completed
3. **Choose task type**:
   - **Add Task**: Regular study task
   - **Priority Task**: High-priority task that needs immediate attention
   - **Weekly Task**: Recurring weekly task
   - **Daily Task**: Daily study routine

### Generating Study Plans

1. **Add your tasks** using the task form
2. **Set task statuses** (Pending, In Progress, Completed)
3. **Click "Generate Study Plan"** to create an AI-powered schedule
4. **View your calendar** by clicking "View Calendar" or navigating to `/calendar/`

### Managing Tasks

- **Status Updates**: Change task status using the dropdown in each row
- **Visual Indicators**: Tasks are color-coded based on their status
- **Task Removal**: Use the trash icon to remove tasks you no longer need

## 🏗️ Project Structure

```
StudyPlanner/
├── StudyPlanner/           # Main Django project
│   ├── __init__.py
│   ├── settings.py         # Django settings
│   ├── urls.py            # URL routing
│   ├── views.py           # View functions
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── templates/             # HTML templates
│   ├── header.html        # Common header
│   ├── footer.html        # Common footer
│   ├── index.html         # Main task management page
│   └── calendar.html      # Study plan calendar view
├── static/               # Static files (created by collectstatic)
├── db.sqlite3           # SQLite database
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🎨 Customization

### Styling

The application uses Bootstrap 5 for styling with custom CSS for:
- Task type color coding
- Status indicators
- Timeline visualization
- Responsive design elements

### Task Types

You can customize task types by modifying the CSS classes in `templates/header.html`:
- `.badge-normal` - Regular tasks
- `.badge-priority` - High-priority tasks
- `.badge-weekly` - Weekly recurring tasks
- `.badge-daily` - Daily recurring tasks

## 🔍 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main task management interface |
| `/calendar/` | GET | Study plan calendar view |
| `/generate-study-plan/` | POST | Generate AI study plan |

### Generate Study Plan API

**Endpoint**: `POST /generate-study-plan/`

**Request Body**:
```json
{
  "tasks": [
    {
      "name": "Study Mathematics",
      "date": "2024-01-15",
      "type": "normal",
      "status": "pending"
    }
  ]
}
```

**Response**:
```json
{
  "study_plan": {
    "title": "Personalized Study Plan",
    "tasks": [
      {
        "date": "2024-01-15",
        "time_start": "09:00",
        "time_end": "10:30",
        "activity": "Study Mathematics",
        "type": "normal",
        "notes": "Focus on algebra and geometry"
      }
    ]
  }
}
```

## 🐛 Troubleshooting

### Common Issues

1. **"AI service not configured" error**
   - Ensure your `GEMINI_API_KEY` is set correctly in the `.env` file
   - Verify the API key is valid and has proper permissions

2. **Static files not loading**
   - Run `python manage.py collectstatic`
   - Ensure the `static/` directory exists

3. **Database errors**
   - Run `python manage.py migrate` to apply database migrations
   - Delete `db.sqlite3` and run migrations again if needed

4. **Import errors**
   - Verify all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility (3.8+)

### Development Mode

For development, ensure `DEBUG=True` in your `.env` file. This enables:
- Detailed error pages
- Debug toolbar (if installed)
- Static file serving
- Automatic code reloading

## 🚀 Deployment

### Production Considerations

1. **Security**:
   - Set `DEBUG=False`
   - Use a strong, unique `SECRET_KEY`
   - Configure `ALLOWED_HOSTS` appropriately
   - Use HTTPS in production

2. **Database**:
   - Consider using PostgreSQL for production
   - Set up regular database backups

3. **Static Files**:
   - Use a CDN or dedicated static file server
   - Run `python manage.py collectstatic` during deployment

4. **Environment Variables**:
   - Use environment-specific configuration
   - Keep sensitive data out of version control

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Django](https://djangoproject.com) - The web framework used
- [Bootstrap](https://getbootstrap.com) - UI framework
- [Google Gemini AI](https://deepmind.google/technologies/gemini/) - AI-powered study plan generation
- [Bootstrap Icons](https://icons.getbootstrap.com) - Icon library

## 📞 Support

If you have any questions or run into issues, please:

1. Check the [troubleshooting section](#🐛-troubleshooting)
2. Search existing [GitHub issues](https://github.com/abhinavramanan/StudyPlanner/issues)
3. Create a new issue if your problem isn't covered

---

**Happy Studying! 📚✨**