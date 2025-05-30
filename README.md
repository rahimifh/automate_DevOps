# 🚀 DevOps Hub

A comprehensive Django web application that provides centralized management for DevOps automation tools. DevOps Hub offers seamless integration with Jenkins CI/CD and GitHub Actions, featuring interactive installation, real-time monitoring, and cross-platform support.

## ✨ Features

### 🔧 Jenkins Management
- **Cross-Platform Installation**: Automated setup for Windows, Linux (Ubuntu/Debian), and macOS
- **Multiple Installation Methods**: 
  - Windows: MSI installer, Chocolatey, Docker
  - Linux: APT package manager, Docker
  - macOS: Homebrew, Docker
- **Interactive Installation**: One-click installation with real-time progress tracking
- **System Status Monitoring**: Live status checks for Java, Docker, Jenkins, and Chocolatey
- **Service Management**: Built-in commands for starting, stopping, and managing Jenkins services

### 🐙 GitHub Actions Integration
- **Repository Management**: Create new repositories or connect to existing ones
- **File Upload & Management**: Direct file uploads to GitHub repositories
- **Automatic Workflow Setup**: GitHub Actions workflow configuration
- **Branch Management**: Handle multiple branches and workflows

### 🎨 Modern User Interface
- **Responsive Design**: Bootstrap 5-based UI that works on all devices
- **Real-time Updates**: AJAX-powered status updates and progress tracking
- **OS-Specific Dashboards**: Tailored interfaces for each operating system
- **Interactive Progress Bars**: Visual feedback during installation processes

### 🔐 Security & Authentication
- **User Authentication**: Django's built-in authentication system
- **GitHub Token Integration**: Secure API access with personal access tokens
- **Role-based Access**: User-specific repository and tool access

## 🛠️ Technology Stack

- **Backend**: Django 5.2.1
- **Frontend**: Bootstrap 5.3.0 + Bootstrap Icons
- **Database**: SQLite (development) / PostgreSQL (production-ready)
- **APIs**: GitHub REST API, System Command Execution
- **Styling**: Custom CSS with gradient themes and animations
- **JavaScript**: Vanilla JS with AJAX for real-time updates

## 📋 Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Dependencies**: Listed in `requirements.txt`
- **Optional**: Git, Docker, Java 17+ (for Jenkins)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/devops-hub.git
cd devops-hub
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# On Windows:
env\Scripts\activate
# On macOS/Linux:
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
# Apply migrations
python manage.py migrate

# Create superuser account
python manage.py createsuperuser
```

### 5. Run the Application
```bash
python manage.py runserver
```

### 6. Access the Application
Open your browser and navigate to: `http://127.0.0.1:8000`

## 📖 Usage Guide

### Getting Started
1. **Sign Up/Login**: Create an account or log in with existing credentials
2. **Choose Your Tool**: Select between Jenkins or GitHub Actions from the homepage
3. **Configure Settings**: Set up your GitHub tokens and preferences

### Jenkins Installation
1. **Navigate**: Go to Jenkins Dashboard → Select your OS (Windows/Linux/macOS)
2. **Choose Method**: Pick your preferred installation method
3. **Install**: Click the installation button and monitor progress
4. **Manage**: Use built-in commands to start, stop, and configure Jenkins

### GitHub Actions Setup
1. **Configure GitHub**: Add your personal access token
2. **Repository Management**: Create new repos or connect existing ones
3. **Upload Files**: Drag and drop files or use the upload interface
4. **Workflow Creation**: Set up automated GitHub Actions workflows

## 🗂️ Project Structure

```
devops-hub/
├── 📁 core/                    # Core app (home page, auth)
│   ├── views.py               # Main views and authentication
│   ├── urls.py                # Core URL patterns
│   └── models.py              # User models
├── 📁 jenkins/                 # Jenkins management app
│   ├── views.py               # Jenkins installation & config
│   ├── urls.py                # Jenkins URL patterns
│   └── models.py              # Jenkins-related models
├── 📁 githubaction/           # GitHub Actions app
│   ├── views.py               # Repository & workflow management
│   ├── urls.py                # GitHub Actions URL patterns
│   └── models.py              # Repository models
├── 📁 templates/              # HTML templates
│   ├── 📁 core/               # Core app templates
│   ├── 📁 jenkins/            # Jenkins-specific templates
│   ├── 📁 githubaction/       # GitHub Actions templates
│   └── 📁 repository/         # Base templates
├── 📁 static/                 # Static files (CSS, JS, images)
├── 📁 media/                  # User uploads
├── 📁 devops_tools/           # Django project settings
├── requirements.txt           # Python dependencies
├── manage.py                  # Django management script
└── README.md                  # This file
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
GITHUB_TOKEN=your-github-token
```

### GitHub Token Setup
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with repo permissions
3. Add the token to your environment variables or configure it in the app

## 🌟 Key Features Walkthrough

### Cross-Platform Jenkins Installation
- **Windows**: MSI installer with automatic Java detection
- **Linux**: APT package manager with dependency resolution
- **macOS**: Homebrew integration with service management
- **Docker**: Universal containerized installation for all platforms

### Real-time Status Monitoring
- Live system checks for installed components
- Color-coded status indicators (green/red badges)
- Automatic refresh capabilities
- Detailed system information display

### Interactive Installation Process
- Progress bars with percentage completion
- Step-by-step installation messages
- Error handling and troubleshooting guidance
- Automatic page refresh upon completion

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature-name`
3. **Commit** your changes: `git commit -am 'Add feature'`
4. **Push** to the branch: `git push origin feature-name`
5. **Submit** a pull request

### Development Guidelines
- Follow Django best practices
- Write clean, commented code
- Test cross-platform compatibility
- Update documentation for new features

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Kill existing Django processes
pkill -f "python manage.py runserver"
# Or use a different port
python manage.py runserver 8001
```

**Template Errors**
- Ensure all templates extend the correct base template
- Check URL namespace configuration
- Verify static files are loading correctly

**Installation Failures**
- Check system permissions (admin/sudo access required)
- Verify internet connectivity
- Review installation logs in the progress section

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Django Community** for the excellent web framework
- **Bootstrap Team** for the responsive UI components
- **Jenkins Project** for the open-source automation server
- **GitHub** for Actions and API integration

## 📧 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Search existing issues on GitHub
3. Create a new issue with detailed information
4. Contact the maintainers

---

**DevOps Hub** - Streamlining development workflows with powerful automation tools and seamless integration.

*Built with ❤️ using Django & Bootstrap* 