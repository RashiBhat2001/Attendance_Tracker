import os
import logging
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user

from app import app, Student, students_cache
from google_sheets import (
    get_student_credentials, 
    get_student_attendance, 
    get_attendance_history,
    update_student_password
)

SPREADSHEET_ID = os.environ.get('GOOGLE_SHEET_ID', '')


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        student_id = request.form.get('student_id', '').strip()
        password = request.form.get('password', '').strip()
        
        if not student_id or not password:
            flash('Please enter both Student ID and Password', 'error')
            return render_template('login.html')
        
        if not SPREADSHEET_ID:
            flash('System configuration error. Please contact administrator.', 'error')
            return render_template('login.html')
        
        try:
            credentials = get_student_credentials(SPREADSHEET_ID)
            
            if student_id in credentials and credentials[student_id]['password'] == password:
                student = Student(student_id, credentials[student_id]['name'])
                students_cache[student_id] = student
                login_user(student)
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid Student ID or Password', 'error')
        except Exception as e:
            logging.error(f"Login error: {e}")
            flash('Unable to connect to the system. Please try again later.', 'error')
    
    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    if not SPREADSHEET_ID:
        flash('System configuration error. Please contact administrator.', 'error')
        return redirect(url_for('login'))
    
    try:
        attendance_data = get_student_attendance(SPREADSHEET_ID, current_user.student_id)
        return render_template('dashboard.html', 
                               student=current_user, 
                               attendance=attendance_data)
    except Exception as e:
        logging.error(f"Dashboard error: {e}")
        flash('Unable to load attendance data. Please try again later.', 'error')
        return render_template('dashboard.html', 
                               student=current_user, 
                               attendance={'subjects': [], 'overall': 0, 'alerts': []})


@app.route('/history')
@login_required
def history():
    if not SPREADSHEET_ID:
        flash('System configuration error. Please contact administrator.', 'error')
        return redirect(url_for('login'))
    
    start_date = None
    end_date = None
    start_date_str = request.args.get('start_date', '')
    end_date_str = request.args.get('end_date', '')
    
    try:
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        pass
    
    try:
        history_data = get_attendance_history(SPREADSHEET_ID, current_user.student_id, start_date, end_date)
        return render_template('history.html', 
                               student=current_user, 
                               history=history_data,
                               start_date=start_date_str,
                               end_date=end_date_str)
    except Exception as e:
        logging.error(f"History error: {e}")
        flash('Unable to load attendance history. Please try again later.', 'error')
        return render_template('history.html', 
                               student=current_user, 
                               history=[],
                               start_date='',
                               end_date='')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if not SPREADSHEET_ID:
        flash('System configuration error. Please contact administrator.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        current_password = request.form.get('current_password', '').strip()
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        if not current_password or not new_password or not confirm_password:
            flash('Please fill in all password fields', 'error')
            return render_template('profile.html', student=current_user)
        
        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
            return render_template('profile.html', student=current_user)
        
        if len(new_password) < 4:
            flash('New password must be at least 4 characters long', 'error')
            return render_template('profile.html', student=current_user)
        
        try:
            credentials = get_student_credentials(SPREADSHEET_ID)
            
            if current_user.student_id not in credentials:
                flash('Unable to verify current password', 'error')
                return render_template('profile.html', student=current_user)
            
            if credentials[current_user.student_id]['password'] != current_password:
                flash('Current password is incorrect', 'error')
                return render_template('profile.html', student=current_user)
            
            if update_student_password(SPREADSHEET_ID, current_user.student_id, new_password):
                flash('Password updated successfully', 'success')
            else:
                flash('Unable to update password. Please try again.', 'error')
        except Exception as e:
            logging.error(f"Profile error: {e}")
            flash('An error occurred. Please try again later.', 'error')
    
    return render_template('profile.html', student=current_user)


@app.route('/logout')
@login_required
def logout():
    if current_user.student_id in students_cache:
        del students_cache[current_user.student_id]
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))
