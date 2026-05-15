# Task Scheduler

A complete, modern, full-stack task management application built with Python Flask, SQLAlchemy, and Bootstrap 5.

## Features
- **User Authentication**: Secure signup, login, password reset, and email verification.
- **Dynamic Dashboard**: Visual progress charts and task summaries.
- **Task Management**: Create, edit, delete, and filter tasks.
- **Productivity Tools**: Built-in Pomodoro timer.
- **Calendar Integration**: Full Calendar view of upcoming tasks.
- **Customization**: Dark Mode support.
- **File Handling**: Upload attachments to tasks.
- **Data Export**: Export your tasks to CSV.

## Setup Instructions

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```
   
2. **Activate the environment:**
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration:**
   Rename `.env.example` to `.env` and fill in your specific configurations (SMTP details are required for the email functionalities).

5. **Initialize Database:**
   Run the initialization script to construct the DB tables and add sample data.
   ```bash
   python init_db.py
   ```

6. **Run the Application:**
   ```bash
   python run.py
   ```

7. **Access the App:**
   Open your browser to `http://127.0.0.1:5000`. 
   
   *Dummy Account Login:*
   - Email: `john@example.com`
   - Password: `Password123!`
