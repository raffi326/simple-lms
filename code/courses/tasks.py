from celery import shared_task
from django.core.mail import send_mail
from .models import Course, CourseMember, UserProgress, CourseContent
from django.contrib.auth.models import User
import csv
import os
from django.conf import settings
from datetime import datetime

@shared_task
def send_enrollment_email(user_id, course_id):
    try:
        user = User.objects.get(id=user_id)
        course = Course.objects.get(id=course_id)
        subject = f"Selamat Datang di {course.name}"
        message = f"Halo {user.first_name}, Anda telah berhasil mendaftar di course {course.name}."
        # In a real app, use send_mail. For now we just log it.
        print(f"EMAIL SENT: {subject} to {user.email}")
        return f"Email sent to {user.email}"
    except Exception as e:
        return str(e)

@shared_task
def generate_certificate(user_id, course_id):
    try:
        user = User.objects.get(id=user_id)
        course = Course.objects.get(id=course_id)
        # Mock certificate generation
        print(f"CERTIFICATE GENERATED: {user.username} - {course.name}")
        return f"Certificate generated for {user.username}"
    except Exception as e:
        return str(e)

@shared_task
def update_course_statistics():
    courses = Course.objects.all()
    stats = []
    for course in courses:
        enrollment_count = CourseMember.objects.filter(course_id=course).count()
        stats.append(f"{course.name}: {enrollment_count}")
    print(f"STATISTICS UPDATED: {', '.join(stats)}")
    return "Statistics updated"

@shared_task
def export_course_report(course_id):
    try:
        course = Course.objects.get(id=course_id)
        members = CourseMember.objects.filter(course_id=course).select_related('user_id')
        
        # Define path relative to project root (since worker runs in /app/code)
        report_dir = os.path.join(settings.BASE_DIR, 'media', 'reports')
        os.makedirs(report_dir, exist_ok=True)
        filename = f"course_{course_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        file_path = os.path.join(report_dir, filename)
        
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['username', 'email', 'role']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for member in members:
                writer.writerow({
                    'username': member.user_id.username,
                    'email': member.user_id.email,
                    'role': member.roles
                })
        return f"Report exported to {file_path}"
    except Exception as e:
        return str(e)
