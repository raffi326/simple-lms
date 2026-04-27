from django.db import models
from django.contrib.auth.models import User


ROLE_CHOICES = [
    ('student', 'Student'),
    ('instructor', 'Instructor'),
    ('admin', 'Admin'),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Course(models.Model):
    name = models.CharField("nama matkul", max_length=100)
    description = models.TextField("deskripsi", default='-')
    price = models.IntegerField("harga", default=10000)
    image = models.ImageField("gambar", null=True, blank=True)
    teacher = models.ForeignKey(
        User,
        verbose_name="pengajar",
        on_delete=models.RESTRICT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Mata Kuliah"
        verbose_name_plural = "Mata Kuliah"


ROLE_OPTIONS = [
    ('std', "Siswa"),
    ('ast', "Asisten"),
]


class CourseMember(models.Model):
    course_id = models.ForeignKey(
        Course,
        verbose_name="matkul",
        on_delete=models.RESTRICT
    )
    user_id = models.ForeignKey(
        User,
        verbose_name="siswa",
        on_delete=models.RESTRICT
    )
    roles = models.CharField(
        "peran",
        max_length=3,
        choices=ROLE_OPTIONS,
        default='std'
    )

    def __str__(self):
        return f"{self.user_id} - {self.course_id} ({self.roles})"

    class Meta:
        verbose_name = "Anggota Kelas"
        verbose_name_plural = "Anggota Kelas"


class CourseContent(models.Model):
    name = models.CharField("judul konten", max_length=200)
    description = models.TextField("deskripsi", default='-')
    video_url = models.CharField(
        'URL Video',
        max_length=200,
        null=True,
        blank=True
    )
    file_attachment = models.FileField("File", null=True, blank=True)
    course_id = models.ForeignKey(
        Course,
        verbose_name="matkul",
        on_delete=models.RESTRICT
    )
    parent_id = models.ForeignKey(
        "self",
        verbose_name="induk",
        on_delete=models.RESTRICT,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Konten Kelas"


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(CourseContent, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'content')
        verbose_name = "Progres User"
        verbose_name_plural = "Progres User"

    def __str__(self):
        return f"{self.user.username} - {self.content.name} - {self.is_completed}"
        verbose_name_plural = "Konten Kelas"


class Comment(models.Model):
    content_id = models.ForeignKey(
        CourseContent,
        verbose_name="konten",
        on_delete=models.CASCADE
    )
    member_id = models.ForeignKey(
        CourseMember,
        verbose_name="pengguna",
        on_delete=models.CASCADE
    )
    comment = models.TextField('komentar')

    def __str__(self):
        return f"Komentar oleh {self.member_id} pada {self.content_id}"

    class Meta:
        verbose_name = "Komentar"
        verbose_name_plural = "Komentar"