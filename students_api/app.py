from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import csv
import io
import ssl

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    'postgresql://airflow:airflow@postgres:5432/students_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Student model
class Student(db.Model):
    __tablename__ = 'students'
    
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    grade = db.Column(db.String(2))
    subject = db.Column(db.String(50))
    score = db.Column(db.Integer)
    enrollment_date = db.Column(db.Date)
    
    def to_dict(self):
        return {
            'student_id': self.student_id,
            'name': self.name,
            'age': self.age,
            'grade': self.grade,
            'subject': self.subject,
            'score': self.score,
            'enrollment_date': self.enrollment_date.isoformat() if self.enrollment_date else None
        }

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'students-api'}), 200

@app.route('/students', methods=['GET'])
def get_all_students():
    """Get all students"""
    try:
        students = Student.query.all()
        return jsonify({
            'students': [student.to_dict() for student in students],
            'count': len(students)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """Get a specific student by ID"""
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        return jsonify(student.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/students', methods=['POST'])
def create_student():
    """Create a new student"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'name' not in data:
            return jsonify({'error': 'Name is required'}), 400
        
        # Parse enrollment_date if provided
        enrollment_date = None
        if 'enrollment_date' in data and data['enrollment_date']:
            try:
                enrollment_date = datetime.strptime(data['enrollment_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Create new student
        student = Student(
            student_id=data.get('student_id'),
            name=data['name'],
            age=data.get('age'),
            grade=data.get('grade'),
            subject=data.get('subject'),
            score=data.get('score'),
            enrollment_date=enrollment_date
        )
        
        db.session.add(student)
        db.session.commit()
        
        return jsonify({
            'message': 'Student created successfully',
            'student': student.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """Update an existing student"""
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update fields if provided
        if 'name' in data:
            student.name = data['name']
        if 'age' in data:
            student.age = data['age']
        if 'grade' in data:
            student.grade = data['grade']
        if 'subject' in data:
            student.subject = data['subject']
        if 'score' in data:
            student.score = data['score']
        if 'enrollment_date' in data and data['enrollment_date']:
            try:
                student.enrollment_date = datetime.strptime(data['enrollment_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        db.session.commit()
        
        return jsonify({
            'message': 'Student updated successfully',
            'student': student.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete a student"""
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        db.session.delete(student)
        db.session.commit()
        
        return jsonify({'message': 'Student deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/students/upload', methods=['POST'])
def upload_students_file():
    """Upload and process a CSV file containing student data"""
    try:
        print("Uploading students file ", request.files, request.form)
        # Check if file is present in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file extension
        if not file.filename.lower().endswith('.csv'):
            return jsonify({'error': 'File must be a CSV file'}), 400
        
        # Read file content
        file_content = file.read().decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(file_content))
        
        # Process each row
        success_count = 0
        error_count = 0
        duplicate_count = 0
        errors = []
        skipped_duplicates = []
        
        for row_num, row in enumerate(csv_reader, start=2):  # Start at 2 because header is row 1
            try:
                # Validate required fields
                if not row.get('name'):
                    errors.append(f"Row {row_num}: Name is required")
                    error_count += 1
                    continue
                
                # Parse enrollment_date if provided
                enrollment_date = None
                if row.get('enrollment_date'):
                    try:
                        enrollment_date = datetime.strptime(row['enrollment_date'], '%Y-%m-%d').date()
                    except ValueError:
                        errors.append(f"Row {row_num}: Invalid date format for enrollment_date. Use YYYY-MM-DD")
                        error_count += 1
                        continue
                
                # Check for duplicate student_id if provided
                student_id = int(row['student_id']) if row.get('student_id') and row['student_id'].strip() else None
                if student_id:
                    existing_student = Student.query.filter_by(student_id=student_id).first()
                    if existing_student:
                        skipped_duplicates.append(f"Row {row_num}: Student ID {student_id} already exists")
                        duplicate_count += 1
                        continue
                
                # Create student record
                student = Student(
                    student_id=student_id,
                    name=row['name'],
                    age=int(row['age']) if row.get('age') and row['age'].strip() else None,
                    grade=row['grade'] if row.get('grade') and row['grade'].strip() else None,
                    subject=row['subject'] if row.get('subject') and row['subject'].strip() else None,
                    score=int(row['score']) if row.get('score') and row['score'].strip() else None,
                    enrollment_date=enrollment_date
                )
                
                db.session.add(student)
                success_count += 1
                
            except Exception as e:
                errors.append(f"Row {row_num}: {str(e)}")
                error_count += 1
        
        # Commit all successful inserts
        db.session.commit()
        
        response_data = {
            'message': 'File processing completed',
            'success_count': success_count,
            'error_count': error_count,
            'duplicate_count': duplicate_count,
            'total_processed': success_count + error_count + duplicate_count
        }
        
        if errors:
            response_data['errors'] = errors[:10]  # Limit to first 10 errors for readability
        
        if skipped_duplicates:
            response_data['skipped_duplicates'] = skipped_duplicates[:10]  # Limit to first 10 for readability
        
        # Return 207 (Multi-Status) if there were any errors or duplicates, 200 if all successful
        if error_count > 0 or duplicate_count > 0:
            return jsonify(response_data), 207  # 207 Multi-Status for partial success
        else:
            return jsonify(response_data), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'File processing failed: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
    
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context='adhoc')
