from django.core.management.base import BaseCommand
from django.db.models import Count, Avg, Sum, Max, Min, Q
from django.contrib.auth.models import User
from courses.models import Course, CourseMember, CourseContent, Comment


class Command(BaseCommand):
    help = 'Demonstrasi query optimization untuk Simple LMS'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== Django ORM Query Optimization Demo ===\n'))
        
        # Demo 1: Mengakses relasi ForeignKey
        self.demo_foreignkey_access()
        
        # Demo 2: Menggunakan reverse relation
        self.demo_reverse_relation()
        
        # Demo 3: Filter melewati relasi
        self.demo_filter_through_relation()
        
        # Demo 4: Aggregate functions
        self.demo_aggregate()
        
        # Demo 5: Annotate untuk perhitungan
        self.demo_annotate()
        
        # Demo 6: Query menggunakan Q objects
        self.demo_q_objects()
        
        self.stdout.write(self.style.SUCCESS('\n=== Demo Selesai ==='))

    def demo_foreignkey_access(self):
        """Demo mengakses data dari ForeignKey"""
        self.stdout.write(self.style.WARNING('\n[DEMO 1] Mengakses Relasi ForeignKey'))
        
        courses = Course.objects.all()[:2]
        for course in courses:
            self.stdout.write(f"Course: {course.name}")
            self.stdout.write(f"  Teacher: {course.teacher.username}")
            self.stdout.write(f"  Price: Rp{course.price:,}")

    def demo_reverse_relation(self):
        """Demo menggunakan reverse relation"""
        self.stdout.write(self.style.WARNING('\n[DEMO 2] Menggunakan Reverse Relation'))
        
        # Mengambil semua course yang diajar oleh user pertama
        users = User.objects.all()[:2]
        for user in users:
            courses = user.course_set.all()
            self.stdout.write(f"User: {user.username}")
            self.stdout.write(f"  Courses taught: {courses.count()}")
            for course in courses:
                self.stdout.write(f"    - {course.name}")

    def demo_filter_through_relation(self):
        """Demo filter melewati relasi menggunakan double underscore"""
        self.stdout.write(self.style.WARNING('\n[DEMO 3] Filter Melewati Relasi'))
        
        # Cari semua course yang diajar oleh user tertentu
        courses = Course.objects.filter(teacher__username__icontains='admin')
        self.stdout.write(f"Courses taught by admin: {courses.count()}")
        for course in courses:
            self.stdout.write(f"  - {course.name} (Teacher: {course.teacher.username})")
        
        # Cari semua member yang terdaftar di course dengan harga > 40000
        members = CourseMember.objects.filter(course_id__price__gt=40000)
        self.stdout.write(f"\nMembers in courses with price > 40000: {members.count()}")

    def demo_aggregate(self):
        """Demo menggunakan aggregate untuk ringkasan data"""
        self.stdout.write(self.style.WARNING('\n[DEMO 4] Aggregate Functions'))
        
        # Hitung jumlah total course
        stats = Course.objects.aggregate(
            total_courses=Count('id'),
            avg_price=Avg('price'),
            max_price=Max('price'),
            min_price=Min('price'),
            total_revenue=Sum('price')
        )
        
        self.stdout.write(f"Total Courses: {stats['total_courses']}")
        self.stdout.write(f"Average Price: Rp{stats['avg_price']:,.0f}")
        self.stdout.write(f"Max Price: Rp{stats['max_price']:,}")
        self.stdout.write(f"Min Price: Rp{stats['min_price']:,}")
        self.stdout.write(f"Total Revenue: Rp{stats['total_revenue']:,}")

    def demo_annotate(self):
        """Demo menggunakan annotate untuk perhitungan per objek"""
        self.stdout.write(self.style.WARNING('\n[DEMO 5] Annotate untuk Perhitungan'))
        
        # Hitung jumlah member per course
        courses = Course.objects.annotate(
            member_count=Count('coursemember')
        ).order_by('-member_count')
        
        self.stdout.write("Courses with member count:")
        for course in courses[:5]:
            self.stdout.write(f"  {course.name}: {course.member_count} member")
        
        # Hitung jumlah konten per course
        courses_with_content = Course.objects.annotate(
            content_count=Count('coursecontent')
        ).filter(content_count__gt=0)
        
        self.stdout.write(f"\nCourses with content: {courses_with_content.count()}")

    def demo_q_objects(self):
        """Demo menggunakan Q objects untuk query kompleks"""
        self.stdout.write(self.style.WARNING('\n[DEMO 6] Query dengan Q Objects (OR/AND/NOT)'))
        
        # Cari course dengan harga < 30000 ATAU nama mengandung 'Web'
        courses = Course.objects.filter(
            Q(price__lt=30000) | Q(name__icontains='Web')
        )
        self.stdout.write(f"Courses with price < 30000 OR name contains 'Web': {courses.count()}")
        
        # NOT query
        courses = Course.objects.filter(~Q(price__lt=50000))
        self.stdout.write(f"Courses with price >= 50000: {courses.count()}")
        
        # Kombinasi AND dan OR
        courses = Course.objects.filter(
            Q(price__lt=50000) | Q(price__gt=100000),
            teacher__username__icontains='admin'
        )
        self.stdout.write(f"Courses (price < 50000 OR > 100000) AND teacher is admin: {courses.count()}")

