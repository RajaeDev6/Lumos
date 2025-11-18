Lesson Plan App - Adaptive Curriculum Engine


A modern, AI-powered educational platform that helps teachers create adaptive lesson plans using Gemini AI, Firebase, and Cloudinary integration.
🚀 Features
📚 Core Functionality

    Syllabus Management - Upload and manage course syllabi (PDF, DOCX, XLSX)

    Test Paper Analysis - Upload student test papers for AI-powered analysis

    AI-Powered Lesson Plans - Generate adaptive lesson plans using Gemini AI

    Performance Analytics - Track student performance and identify weak areas

    Real-time Dashboard - Comprehensive overview of teaching materials and progress

🎯 Smart Features

    Adaptive Curriculum - AI suggests personalized teaching strategies

    Weak Area Identification - Automatically detects student learning gaps

    Progress Tracking - Monitor syllabus coverage and teaching effectiveness

    Recommendation Engine - AI-generated teaching recommendations

💼 Teacher Tools

    Profile Management - Personal teacher profiles and preferences

    File Management - Cloud storage for all teaching materials

    Export Capabilities - Download lesson plans in multiple formats

    Collaboration Ready - Share and collaborate on curriculum planning

🛠️ Technology Stack
Frontend

    HTML5 - Semantic markup and structure

    TailwindCSS - Utility-first CSS framework

    Vanilla JavaScript - Modern ES6+ features

    Modular Architecture - Clean, maintainable code structure

Backend Integration

    FastAPI - High-performance Python web framework

    Firebase Firestore - Real-time database

    Cloudinary - Cloud file storage and management

    Google Gemini AI - Advanced AI analysis and recommendations

📦 Installation & Setup
Prerequisites

    Node.js (for frontend development)

    Python 3.7+

    Modern web browser

Quick Start

    Clone the repository
    bash

git clone <your-repo-url>
cd lessonplanapp-frontend

Set up the frontend
bash

# No build process required - it's pure HTML/CSS/JS!
# Simply open index.html in your browser

Start the backend (separate repository)
bash

# Navigate to backend directory
cd ../lessonplanapp-backend

# Install Python dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn fastapi:app --reload --host 0.0.0.0 --port 5000

    Launch the application

        Open frontend/index.html in your web browser

        Or use a local server: python -m http.server 3000

🏗️ Project Structure
text

frontend/
├── index.html                 # Main application entry point
├── js/
│   ├── api-service.js        # Backend API communication layer
│   ├── state-manager.js      # Application state management
│   └── config.js            # Configuration and constants
├── css/                      # Additional styles (if needed)
└── assets/                   # Images and static resources

🔌 API Integration

The frontend communicates with the backend through these main endpoints:
Authentication

    POST /auth/login - User authentication

    POST /submit_teacher/ - Teacher registration

File Management

    POST /syllabus_uploader/ - Upload syllabus files

    POST /test_paper_uploader/ - Upload test papers

    POST /list_uploads/ - Retrieve upload history

Curriculum Management

    POST /add_lesson/ - Create new lesson plans

    POST /list_lessons/ - Retrieve lesson plans

    POST /generate/ - AI-powered lesson plan generation

Data Retrieval

    POST /get_teacher/ - Get teacher profile

    POST /list_syllabus_uploads/ - Get syllabus list

    POST /list_testpaper_uploads/ - Get test papers list

🎨 UI/UX Features
Responsive Design

    Mobile-first approach

    Cross-browser compatible

    Accessible components (ARIA labels, keyboard navigation)

User Experience

    Drag & Drop file uploads

    Real-time progress indicators

    Toast notifications for user feedback

    Modal dialogs for detailed interactions

    Loading states for better UX during API calls

Navigation

    Sticky header with quick access navigation

    Mobile-optimized dropdown menu

    Active state indicators for current page

🔧 Configuration
Environment Setup

Create a config.js file with your backend configuration:
javascript

const CONFIG = {
    API_BASE_URL: 'http://localhost:5000',
    MAX_FILE_SIZE: 50 * 1024 * 1024, // 50MB
    ALLOWED_FILE_TYPES: ['.pdf', '.docx', '.xlsx'],
    REQUEST_TIMEOUT: 30000
};

Browser Support

    Chrome 90+

    Firefox 88+

    Safari 14+

    Edge 90+

🚀 Deployment
Development
bash

# Simple static file serving
python -m http.server 3000
# or
npx serve -s . -l 3000

Production

The frontend is static and can be deployed to any web server:

    Netlify - Drag and drop deployment

    Vercel - Git-based deployment

    AWS S3 - Static website hosting

    GitHub Pages - Free hosting for open source

📱 Usage Guide
For Teachers

    Register/Login - Create your teacher profile

    Upload Syllabus - Add your course syllabus

    Upload Test Papers - Add student assessment data

    Generate Plans - Let AI create adaptive lesson plans

    Review & Edit - Customize generated plans

    Track Progress - Monitor student performance

File Requirements

    Syllabus: PDF, DOCX, XLSX (max 50MB)

    Test Papers: PDF, DOCX, XLSX (max 50MB)

    Images: JPEG, PNG, GIF (for future features)

🤝 Contributing

We welcome contributions! Please see our Contributing Guidelines for details.
Development Setup

    Fork the repository

    Create a feature branch: git checkout -b feature/amazing-feature

    Commit changes: git commit -m 'Add amazing feature'

    Push to branch: git push origin feature/amazing-feature

    Open a Pull Request

🐛 Troubleshooting
Common Issues

Frontend not connecting to backend:

    Check if backend is running on port 5000

    Verify CORS configuration in backend

    Check browser console for errors

File upload issues:

    Verify file size (< 50MB)

    Check file format (PDF, DOCX, XLSX)

    Ensure stable internet connection

Authentication problems:

    Clear browser cookies and local storage

    Check backend authentication service

    Verify teacher credentials in database

Getting Help

    Check the Issues page

    Create a detailed bug report

    Include browser console errors

📄 License

This project is licensed under the MIT License - see the LICENSE.md file for details.
