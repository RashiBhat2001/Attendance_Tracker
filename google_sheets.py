import os
import requests
import logging

connection_settings = None

def get_access_token():
    global connection_settings
    
    hostname = os.environ.get('REPLIT_CONNECTORS_HOSTNAME')
    
    repl_identity = os.environ.get('REPL_IDENTITY')
    web_repl_renewal = os.environ.get('WEB_REPL_RENEWAL')
    
    if repl_identity:
        x_replit_token = f'repl {repl_identity}'
    elif web_repl_renewal:
        x_replit_token = f'depl {web_repl_renewal}'
    else:
        raise Exception('X_REPLIT_TOKEN not found for repl/depl')
    
    response = requests.get(
        f'https://{hostname}/api/v2/connection?include_secrets=true&connector_names=google-sheet',
        headers={
            'Accept': 'application/json',
            'X_REPLIT_TOKEN': x_replit_token
        }
    )
    
    data = response.json()
    connection_settings = data.get('items', [{}])[0] if data.get('items') else None
    
    if not connection_settings:
        raise Exception('Google Sheet not connected')
    
    settings = connection_settings.get('settings', {})
    access_token = settings.get('access_token') or settings.get('oauth', {}).get('credentials', {}).get('access_token')
    
    if not access_token:
        raise Exception('Google Sheet access token not found')
    
    return access_token


def get_sheet_data(spreadsheet_id, range_name):
    access_token = get_access_token()
    
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_name}'
    
    response = requests.get(
        url,
        headers={
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }
    )
    
    if response.status_code != 200:
        logging.error(f"Google Sheets API error: {response.status_code} - {response.text}")
        raise Exception(f'Failed to fetch sheet data: {response.status_code}')
    
    return response.json()


def get_student_credentials(spreadsheet_id):
    try:
        data = get_sheet_data(spreadsheet_id, 'Credentials!A:C')
        values = data.get('values', [])
        
        if len(values) <= 1:
            return {}
        
        credentials = {}
        for row in values[1:]:
            if len(row) >= 3:
                student_id = str(row[0]).strip()
                password = str(row[1]).strip()
                name = str(row[2]).strip()
                credentials[student_id] = {'password': password, 'name': name}
        
        return credentials
    except Exception as e:
        logging.error(f"Error fetching credentials: {e}")
        return {}


def get_student_attendance(spreadsheet_id, student_id):
    try:
        data = get_sheet_data(spreadsheet_id, 'Attendance!A:Z')
        values = data.get('values', [])
        
        if len(values) <= 1:
            return {'subjects': [], 'overall': 0, 'alerts': []}
        
        headers = values[0]
        
        student_row = None
        for row in values[1:]:
            if len(row) > 0 and str(row[0]).strip() == student_id:
                student_row = row
                break
        
        if not student_row:
            return {'subjects': [], 'overall': 0, 'alerts': []}
        
        subjects = []
        alerts = []
        total_attended = 0
        total_classes = 0
        
        i = 1
        while i < len(headers) - 1:
            subject_name = headers[i]
            
            if subject_name and not subject_name.lower().endswith('_total'):
                attended = 0
                total = 0
                
                if i < len(student_row):
                    try:
                        attended = int(student_row[i])
                    except (ValueError, TypeError):
                        attended = 0
                
                if i + 1 < len(headers) and i + 1 < len(student_row):
                    try:
                        total = int(student_row[i + 1])
                    except (ValueError, TypeError):
                        total = 0
                
                if total > 0:
                    percentage = round((attended / total) * 100, 1)
                else:
                    percentage = 0
                
                subject_data = {
                    'name': subject_name,
                    'attended': attended,
                    'total': total,
                    'percentage': percentage
                }
                subjects.append(subject_data)
                
                if percentage < 75:
                    classes_needed = 0
                    if total > 0:
                        classes_needed = max(0, int((0.75 * total - attended) / 0.25) + 1)
                    alerts.append({
                        'subject': subject_name,
                        'percentage': percentage,
                        'classes_needed': classes_needed,
                        'severity': 'critical' if percentage < 60 else 'warning'
                    })
                
                total_attended += attended
                total_classes += total
                
                i += 2
            else:
                i += 1
        
        overall = round((total_attended / total_classes) * 100, 1) if total_classes > 0 else 0
        
        return {
            'subjects': sorted(subjects, key=lambda x: x['name']),
            'overall': overall,
            'alerts': sorted(alerts, key=lambda x: x['percentage'])
        }
    except Exception as e:
        logging.error(f"Error fetching attendance: {e}")
        return {'subjects': [], 'overall': 0, 'alerts': []}


def get_attendance_history(spreadsheet_id, student_id, start_date=None, end_date=None):
    try:
        data = get_sheet_data(spreadsheet_id, 'History!A:Z')
        values = data.get('values', [])
        
        if len(values) <= 1:
            return []
        
        headers = values[0]
        
        history = []
        for row in values[1:]:
            if len(row) >= 4 and str(row[0]).strip() == student_id:
                date_str = str(row[1]).strip()
                subject = str(row[2]).strip()
                status = str(row[3]).strip().lower()
                
                from datetime import datetime
                try:
                    record_date = datetime.strptime(date_str, '%Y-%m-%d')
                    
                    if start_date and record_date < start_date:
                        continue
                    if end_date and record_date > end_date:
                        continue
                    
                    history.append({
                        'date': date_str,
                        'subject': subject,
                        'status': 'present' if status in ['present', 'p', '1', 'yes'] else 'absent'
                    })
                except ValueError:
                    history.append({
                        'date': date_str,
                        'subject': subject,
                        'status': 'present' if status in ['present', 'p', '1', 'yes'] else 'absent'
                    })
        
        return sorted(history, key=lambda x: x['date'], reverse=True)
    except Exception as e:
        logging.error(f"Error fetching history: {e}")
        return []


def update_student_password(spreadsheet_id, student_id, new_password):
    try:
        access_token = get_access_token()
        
        data = get_sheet_data(spreadsheet_id, 'Credentials!A:C')
        values = data.get('values', [])
        
        row_index = None
        for i, row in enumerate(values):
            if len(row) > 0 and str(row[0]).strip() == student_id:
                row_index = i + 1
                break
        
        if row_index is None:
            return False
        
        url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/Credentials!B{row_index}?valueInputOption=RAW'
        
        response = requests.put(
            url,
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            },
            json={
                'values': [[new_password]]
            }
        )
        
        return response.status_code == 200
    except Exception as e:
        logging.error(f"Error updating password: {e}")
        return False
