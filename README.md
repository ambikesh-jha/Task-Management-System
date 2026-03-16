# Training Dashboard

A Flask-based web application for managing training tasks between trainers and trainees.

## Overview

Training Dashboard provides a simple yet effective platform for trainers to assign tasks to students and for students to track their progress. The application features role-based access control, secure authentication, and a clean, intuitive interface.

## Features

- **User Authentication**: Secure signup/login with password hashing
- **Role-Based Access**: Separate interfaces for trainers and students
- **Task Management**:
  - Trainers can assign tasks to multiple students
  - Students can view and update task statuses
  - Real-time task status tracking (To-Do, In Progress, Done)
- **Session Management**: Persistent login sessions with configurable timeout
- **Responsive Design**: Clean, user-friendly interface for all devices

## Tech Stack

- **Backend**: Python Flask
- **Database**: MongoDB (Atlas cloud)
- **Authentication**: JWT tokens + Session management
- **Frontend**: HTML5, CSS3, Jinja2 templating

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure MongoDB connection in the database files
4. Run the application: `python app.py`

## Usage

1. **Sign up** as either a trainer or student
2. **Login** with your credentials
3. **Trainers**: Add tasks for students
4. **Students**: View and update task statuses
5. **Logout** when done

## Project Structure

- `app.py` - Main application entry point
- `login_signup_render.py` - Authentication blueprint
- `trainee_render.py` - Student operations
- `trainer_render.py` - Trainer operations
- `database.py` - MongoDB connection and operations
- `validate.py` - Input validation utilities
- `templates/` - HTML templates

## API Endpoints

- `/signup` - User registration
- `/login` - User authentication
- `/logout` - Session termination
- `/add_tasks` - Trainer task assignment
- `/tasks` - Student task viewing
- `/update_user_task_status` - Task status updates
- `/view_all_tasks` - View all tasks (trainer only)

## Security Features

- Password hashing with pbkdf2:sha256
- JWT token authentication
- Session-based authorization
- Input validation for all forms
- Role-based access control

## Future Enhancements

- Email notifications for task assignments
- Task deadlines and reminders
- Progress analytics dashboard
- File attachments for tasks
- Mobile-responsive enhancements