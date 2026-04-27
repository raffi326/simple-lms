# core/schemas.py
from ninja import Schema, Field
from datetime import datetime
from typing import Optional, List


class UserOut(Schema):
    """Schema untuk data User yang dikembalikan dalam response."""
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    role: str = Field(None, alias="profile.role")


class RegisterIn(Schema):
    username: str
    password: str
    email: str
    first_name: str = ""
    last_name: str = ""
    role: str = "student"


class LoginIn(Schema):
    username: str
    password: str


class ProfileUpdateIn(Schema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None


class TokenOut(Schema):
    access: str
    refresh: str


class EnrollmentOut(Schema):
    id: int
    course_name: str = Field(None, alias="course_id.name")
    roles: str
    user_username: str = Field(None, alias="user_id.username")


class ProgressIn(Schema):
    content_id: int
    is_completed: bool


class ProgressOut(Schema):
    id: int
    content_name: str = Field(None, alias="content.name")
    is_completed: bool
    completed_at: datetime


class CourseIn(Schema):
    """Schema untuk input saat membuat/mengupdate Course."""
    name: str
    description: str = '-'
    price: int = 10000


class CourseOut(Schema):
    """Schema untuk output data Course."""
    id: int
    name: str
    description: str
    price: int
    image: Optional[str] = ''
    teacher: UserOut
    created_at: datetime
    updated_at: datetime


class ContentTitleOut(Schema):
    """Schema untuk menampilkan judul konten saja."""
    id: int
    name: str


class DetailCourseOut(CourseOut):
    """Schema untuk detail Course beserta daftar konten."""
    contents: List[ContentTitleOut] = Field(
        ..., alias="coursecontent_set"
    )