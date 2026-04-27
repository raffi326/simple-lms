# core/apiv1.py
from ninja import NinjaAPI, Router
from ninja.errors import HttpError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from courses.models import Course, Profile, CourseMember, UserProgress, CourseContent
from core.schemas import (
    CourseIn, CourseOut, DetailCourseOut, 
    RegisterIn, UserOut, ProfileUpdateIn,
    EnrollmentOut, ProgressIn, ProgressOut,
    LoginIn, TokenOut
)
from core.auth import is_admin, is_instructor, is_student, is_course_owner
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
from typing import List

apiv1 = NinjaExtraAPI(
    title="Simple LMS API",
    version="1.0.0",
    description="API untuk Simple Learning Management System"
)

# Register JWT Controller
apiv1.register_controllers(NinjaJWTDefaultController)
auth_router = Router(tags=["Authentication"])
course_router = Router(tags=["Courses"])
enroll_router = Router(tags=["Enrollments"])

from ninja_jwt.tokens import RefreshToken
from django.contrib.auth import authenticate

# ==================== Auth Endpoints ====================

@auth_router.post("/login", response=TokenOut)
def login(request, data: LoginIn):
    user = authenticate(username=data.username, password=data.password)
    if not user:
        raise HttpError(401, "Kredensial tidak valid")
    
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }

@auth_router.post("/refresh", response=TokenOut)
def refresh_token(request, refresh: str):
    try:
        token = RefreshToken(refresh)
        return {
            'access': str(token.access_token),
            'refresh': str(token)
        }
    except Exception:
        raise HttpError(401, "Token refresh tidak valid")

@auth_router.post("/register", response={201: UserOut})
def register(request, data: RegisterIn):
    if User.objects.filter(username=data.username).exists():
        raise HttpError(400, "Username sudah digunakan")
    
    user = User.objects.create(
        username=data.username,
        password=make_password(data.password),
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name
    )
    Profile.objects.create(user=user, role=data.role)
    return 201, user

@auth_router.get("/me", auth=JWTAuth(), response=UserOut)
def get_me(request):
    return request.user

@auth_router.put("/me", auth=JWTAuth(), response=UserOut)
def update_me(request, data: ProfileUpdateIn):
    user = request.user
    for attr, value in data.dict(exclude_none=True).items():
        setattr(user, attr, value)
    user.save()
    return user

# ==================== Course Endpoints ====================

@course_router.get("/", response=List[CourseOut])
def listCourses(request, search: str = None, min_price: int = None, max_price: int = None):
    """Mengambil daftar semua course dengan filter opsional."""
    qs = Course.objects.select_related('teacher').all()
    if search:
        qs = qs.filter(name__icontains=search)
    if min_price is not None:
        qs = qs.filter(price__gte=min_price)
    if max_price is not None:
        qs = qs.filter(price__lte=max_price)
    return qs

@course_router.get("/{id}", response=DetailCourseOut)
def detailCourse(request, id: int):
    """Mengambil detail course beserta daftar kontennya."""
    try:
        return Course.objects.prefetch_related(
            'coursecontent_set'
        ).select_related('teacher').get(pk=id)
    except Course.DoesNotExist:
        raise HttpError(404, "Course tidak ditemukan")

@course_router.post("/", auth=JWTAuth(), response={201: CourseOut})
@is_instructor
def createCourse(request, data: CourseIn):
    """Membuat course baru (Hanya Instructor)."""
    course = Course.objects.create(**data.dict(), teacher=request.user)
    return 201, course

@course_router.patch("/{id}", auth=JWTAuth(), response=CourseOut)
@is_course_owner
def updateCourse(request, id: int, data: CourseIn):
    """Mengupdate data course (Hanya Owner/Instructor)."""
    try:
        course = Course.objects.get(pk=id)
    except Course.DoesNotExist:
        raise HttpError(404, "Course tidak ditemukan")

    for attr, value in data.dict(exclude_none=True).items():
        setattr(course, attr, value)
    course.save()
    return course

@course_router.delete("/{id}", auth=JWTAuth(), response={204: None})
@is_admin
def deleteCourse(request, id: int):
    """Menghapus course (Hanya Admin)."""
    try:
        course = Course.objects.get(pk=id)
    except Course.DoesNotExist:
        raise HttpError(404, "Course tidak ditemukan")

    course.delete()
    return 204, None

# ==================== Enrollment Endpoints ====================

@enroll_router.post("/", auth=JWTAuth(), response={201: EnrollmentOut})
@is_student
def enroll_course(request, course_id: int):
    """Mendaftar ke course (Hanya Student)."""
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        raise HttpError(404, "Course tidak ditemukan")
    
    enrollment, created = CourseMember.objects.get_or_create(
        user_id=request.user,
        course_id=course,
        defaults={'roles': 'std'}
    )
    if not created:
        raise HttpError(400, "Anda sudah terdaftar di course ini")
    
    return 201, enrollment

@enroll_router.get("/my-courses", auth=JWTAuth(), response=List[EnrollmentOut])
@is_student
def my_courses(request):
    """Melihat daftar course yang diikuti."""
    return CourseMember.objects.filter(user_id=request.user).select_related('course_id')

@enroll_router.post("/{content_id}/progress", auth=JWTAuth(), response=ProgressOut)
@is_student
def mark_progress(request, content_id: int, data: ProgressIn):
    """Menandai progres konten (Hanya Student)."""
    try:
        content = CourseContent.objects.get(pk=content_id)
        # Pastikan user terdaftar di course tersebut
        if not CourseMember.objects.filter(user_id=request.user, course_id=content.course_id).exists():
            raise HttpError(403, "Anda tidak terdaftar di course ini")
    except CourseContent.DoesNotExist:
        raise HttpError(404, "Konten tidak ditemukan")
    
    progress, created = UserProgress.objects.update_or_create(
        user=request.user,
        content=content,
        defaults={'is_completed': data.is_completed}
    )
    return progress

# Register Routers
apiv1.add_router("/auth", auth_router)
apiv1.add_router("/courses", course_router)
apiv1.add_router("/enrollments", enroll_router)