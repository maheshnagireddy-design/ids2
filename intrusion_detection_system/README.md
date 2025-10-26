
# Professional Intrusion Detection System

A comprehensive web-based Intrusion Detection System (IDS) built with Flask, featuring Random Forest machine learning for real-time network threat detection.

## 🚀 Features

### Core Functionality
- **Real-time Network Monitoring**: Live detection of network intrusions
- **AI-Powered Analysis**: Random Forest machine learning algorithm with 99%+ accuracy
- **NSL-KDD Dataset**: Trained on the industry-standard NSL-KDD benchmark dataset
- **Multi-Attack Detection**: Supports DoS, Probe, R2L, and U2R attack categories

### User Management
- **Role-Based Access Control**: SuperAdmin, Admin, and User roles with hierarchical permissions
- **Session-Based Authentication**: Secure login/logout system
- **User CRUD Operations**: Complete user management capabilities
- **Access Control**: Middleware decorators for endpoint protection

### Professional UI/UX
- **Bootstrap 5**: Modern, responsive design with professional aesthetics
- **Real-time Dashboard**: Live monitoring interface with animated status indicators
- **Interactive Visualizations**: Charts and graphs for security metrics
- **Mobile Responsive**: Optimized for all device sizes

### Technical Architecture
- **Flask Framework**: Scalable Python web application
- **SQLite Database**: Lightweight, embedded database solution
- **Model Persistence**: Pre-trained ML models with joblib serialization
- **RESTful API**: Clean API endpoints for detection services

## 📋 Requirements

```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.3
Flask-WTF==1.1.1
WTForms==3.0.1
Werkzeug==2.3.7
pandas==2.1.0
scikit-learn==1.3.0
numpy==1.24.3
joblib==1.3.2
python-socketio==5.8.0
flask-socketio==5.3.6
```

## 🔧 Installation & Setup

1. **Extract the project**
   ```bash
   unzip intrusion_detection_system.zip
   cd intrusion_detection_system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python run.py
   ```

5. **Access the application**
   - Open your browser and navigate to `http://localhost:5000`

## 👥 Default Credentials

### SuperAdmin (Full Access)
- **Username**: `admin`
- **Password**: `admin123`
- **Capabilities**: 
  - Create/Edit/Delete all users (including Admins)
  - Access all system features
  - View system-wide statistics

### Creating Additional Users
- **Admins**: Only SuperAdmin can create Admin users
- **Users**: Can register themselves or be created by Admins/SuperAdmin

## 🏗️ Project Structure

```
intrusion_detection_system/
├── app/
│   ├── __init__.py              # Application factory
│   ├── models/
│   │   ├── user.py             # User model with RBAC
│   │   └── detection.py        # Detection results model
│   ├── routes/
│   │   ├── auth.py             # Authentication routes
│   │   ├── main.py             # Main application routes
│   │   ├── admin.py            # Admin panel routes
│   │   └── detection.py        # ML detection routes
│   ├── templates/              # Jinja2 HTML templates
│   │   ├── base.html           # Base template with Bootstrap 5
│   │   ├── auth/               # Authentication templates
│   │   ├── main/               # Main application templates
│   │   ├── admin/              # Admin panel templates
│   │   └── detection/          # Detection interface templates
│   └── static/
│       ├── css/                # Custom stylesheets
│       ├── js/                 # JavaScript files
│       └── models/             # ML model storage
├── config.py                   # Configuration settings
├── run.py                      # Application entry point
├── requirements.txt            # Python dependencies
└── database.db                 # SQLite database (created on first run)
```

## 🤖 Machine Learning Details

### NSL-KDD Dataset
- **Features**: 41 network traffic features
- **Attack Types**: DoS, Probe, R2L, U2R, Normal
- **Training Samples**: 10,000+ network connections
- **Preprocessing**: Categorical encoding, feature scaling

### Random Forest Model
- **Algorithm**: Ensemble of 100 decision trees
- **Accuracy**: ~99% on test dataset
- **Features**: Automatic feature importance ranking
- **Prediction**: Multi-class classification with confidence scores

## 🔐 Security Features

### Authentication & Authorization
- **Password Hashing**: Werkzeug secure password hashing
- **Session Management**: Flask-Login session handling
- **RBAC Implementation**: Role-based access control with decorators
- **CSRF Protection**: Flask-WTF CSRF token validation

### Access Control Matrix
| Feature | User | Admin | SuperAdmin |
|---------|------|-------|------------|
| Live Detection | ✅ | ✅ | ✅ |
| View Own Results | ✅ | ✅ | ✅ |
| User Dashboard | ✅ | ✅ | ✅ |
| Create Users | ❌ | ✅ | ✅ |
| Delete Users | ❌ | ✅ | ✅ |
| Create Admins | ❌ | ❌ | ✅ |
| System Dashboard | ❌ | ✅ | ✅ |

## 🌐 API Endpoints

### Detection API
- `POST /detection/api/predict` - Analyze network traffic
- `POST /detection/api/simulate` - Generate simulated traffic

### Authentication
- `GET/POST /login` - User authentication
- `GET/POST /register` - User registration
- `GET /logout` - User logout

### Admin Routes
- `GET /admin/dashboard` - System overview
- `GET /admin/users` - User management
- `POST /admin/create_user` - Create new user
- `GET /admin/delete_user/<id>` - Delete user

## 🎨 UI/UX Features

### Modern Design
- **Bootstrap 5**: Latest UI framework
- **Gradient Backgrounds**: Professional visual appeal
- **Glass Morphism**: Modern translucent card effects
- **Responsive Layout**: Mobile-first design approach

### Interactive Elements
- **Real-time Updates**: Live detection status
- **Animated Indicators**: Pulse effects for active monitoring
- **Progress Bars**: Visual confidence metrics
- **Status Badges**: Color-coded attack classifications

## 📊 Monitoring & Analytics

### Real-time Dashboard
- Live network traffic analysis
- Attack detection counters
- Confidence score visualization
- Historical detection log

### System Metrics
- Total users and detections
- Attack type distribution
- User activity tracking
- System performance indicators

## 🔧 Customization

### Adding New Features
1. Create new routes in appropriate blueprint
2. Add corresponding templates
3. Update navigation and permissions
4. Test with different user roles

### Model Updates
1. Retrain with new dataset
2. Save model to `app/static/models/`
3. Update prediction endpoint
4. Validate accuracy metrics

## 🚀 Deployment

### Production Considerations
- Change `SECRET_KEY` in config.py
- Use production WSGI server (Gunicorn, uWSGI)
- Configure reverse proxy (Nginx)
- Set up proper logging
- Use production database (PostgreSQL, MySQL)

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "run.py"]
```

## 📈 Performance

### Optimization Features
- Lazy loading of ML models
- Database query optimization
- Static file caching
- Minimal JavaScript footprint

### Scalability
- Modular blueprint architecture
- Database relationship optimization
- Efficient session management
- RESTful API design

## 🛠️ Troubleshooting

### Common Issues
1. **Model not found**: Ensure `intrusion_detection_model.pkl` is in the correct directory
2. **Permission denied**: Check user roles and RBAC decorators
3. **Database errors**: Delete `database.db` and restart the application
4. **Import errors**: Verify all dependencies are installed

### Development Mode
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python run.py
```

## 📝 License

This project is developed for educational and professional demonstration purposes.

## 👨‍💻 Author

Professional Intrusion Detection System - A comprehensive cybersecurity solution combining machine learning, web development, and modern UI design principles.

---

**Note**: This system uses simulated network traffic for demonstration. In production, integrate with actual network monitoring tools for real-time threat detection.
