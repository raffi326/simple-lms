from functools import wraps
from ninja.errors import HttpError
from courses.models import Profile, Course

def has_role(user, role):
    if not user.is_authenticated:
        return False
    try:
        return user.profile.role == role
    except Profile.DoesNotExist:
        return False

def is_admin(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not has_role(request.user, 'admin'):
            raise HttpError(403, "Akses ditolak: Memerlukan peran Admin")
        return func(request, *args, **kwargs)
    return wrapper

def is_instructor(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not (has_role(request.user, 'instructor') or has_role(request.user, 'admin')):
            raise HttpError(403, "Akses ditolak: Memerlukan peran Instructor")
        return func(request, *args, **kwargs)
    return wrapper

def is_student(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not (has_role(request.user, 'student') or has_role(request.user, 'admin')):
            raise HttpError(403, "Akses ditolak: Memerlukan peran Student")
        return func(request, *args, **kwargs)
    return wrapper

def is_course_owner(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        course_id = kwargs.get('id')
        if not course_id:
            raise HttpError(400, "ID Course diperlukan untuk validasi kepemilikan")
        
        try:
            course = Course.objects.get(pk=course_id)
            if course.teacher != request.user and not has_role(request.user, 'admin'):
                raise HttpError(403, "Akses ditolak: Anda bukan pengajar course ini")
        except Course.DoesNotExist:
            raise HttpError(404, "Course tidak ditemukan")
            
        return func(request, *args, **kwargs)
    return wrapper
