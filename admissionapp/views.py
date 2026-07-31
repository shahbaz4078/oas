from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from .models import Student
from .models import Enquiry
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Courses
import os
from django.utils import timezone






def home(request):
    return render(request, 'home.html')


# Create your views here.
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard or any other page after successful login
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
        
    return render(request, 'login.html')

@login_required(login_url='admin_login')
def dashboard(request):
    return render(request, 'dashboard.html')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')  # Redirect to the home page after logout

def edit(request):
    return render(request, 'edit.html')



def add_student(request):
    courses = Courses.objects.all()

    if request.method == "POST":
        course = get_object_or_404(
            Courses,
            id=request.POST.get("course")
        )

        student = Student.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            password=request.POST.get("password"),
            mobile=request.POST.get("mobile"),
            course=course,          # ForeignKey object
            gender=request.POST.get("gender"),
            dob=request.POST.get("dob"),
            address=request.POST.get("address"),
            status="Pending"
        )

        send_mail(
            subject="Student Registration",
            message=f"""
Dear {student.name},

Your password is: {student.password}

You have been registered successfully for {student.course.coursename}.

Regards,
Sipher Web Academy
""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[student.email],
            fail_silently=False,
        )

        return redirect("dashboard")

    return render(request, "add_student.html", {"courses": courses})
def all_student(request):
    students = Student.objects.all()
    return render(request, 'all_student.html', {
        'students': students
    })

def delete(request,id):
    student=get_object_or_404(Student,id=id)
    student.delete()
    return redirect('all_student')



def enquiry(request):
    courses = Courses.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        course = request.POST.get('course')
        message = request.POST.get('message')

        Enquiry.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            course=course,
            message=message,
        )

        send_mail(
            subject="Thank You for Your Enquiry",
            message=f"""
Dear {name},

Thank you for contacting Sipher Web Academy.

We have successfully received your enquiry regarding "{course}".

Our team will contact you shortly.

Regards,
Sipher Web Academy
Lucknow
""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        return redirect('home')

    return render(request, "enquiry.html", {
        "courses": courses
    })

def all_enquiry(request):
    enquiries = Enquiry.objects.all()
    return render(request, 'all_enquiry.html', {
        'enquiries': enquiries
    })



def student_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')


        try:
            student = Student.objects.get(email=email, password=password)

            # Create session
            request.session['student_id'] = student.id
            request.session['student_name'] = student.name
            request.session['student_email'] = student.email

            return redirect('student_dashboard')

        except Student.DoesNotExist:
            return render(
                request,
                'student/student_login.html',
                {'error': 'Invalid email or password'}
            )

    return render(request, 'student/student_login.html')


def student_dashboard(request):
    student_id = request.session.get("student_id")
    if not student_id:
        return redirect("student_login")

    student = get_object_or_404(Student, id=student_id)

    return render(request, "student/student_dashboard.html", {
        "student": student,
    })
def student_logout(request):
    request.session.flush()
    logout(request)
    return redirect('student_login') 


def add_courses(request):
    if request.method == "POST":
        coursename = request.POST.get('coursename')
        session = request.POST.get('session')
        duration = request.POST.get('duration')
        fees = request.POST.get('fees')

        Courses.objects.create(
            coursename=coursename,
            session=session,
            duration=duration,
            fees=fees
        )
        return redirect('dashboard')
       
    return render(request, 'myadmin/add_courses.html')



        

def all_courses(request):
    courses = Courses.objects.all()
    return render(request, 'myadmin/all_courses.html', {
        'courses': courses
    })

def course_delete(request,id):
    course=get_object_or_404(Courses,id=id)
    course.delete()
    return redirect('all_courses')

def courses(request):
    return render(request, 'courses.html')


def student_application(request):
    student_id = request.session.get("student_id")
    if not student_id:
        return redirect("student_login")

    student = get_object_or_404(Student, id=student_id)
    courses = Courses.objects.all()

    # Prevent resubmission
    if student.application_status != "Not Submitted":
        return render(
            request,
            "student/student_application.html",
            {
                "student": student,
                "courses": courses,
                "submitted": True,
            },
        )

    if request.method == "POST":

        # Basic Details
        student.name = request.POST.get("name")
        student.email = request.POST.get("email")
        student.password = request.POST.get("password")
        student.mobile = request.POST.get("mobile")

        # Course
        course_id = request.POST.get("course")
        if course_id:
            student.course = get_object_or_404(Courses, id=course_id)

        student.gender = request.POST.get("gender")
        student.dob = request.POST.get("dob")
        student.address = request.POST.get("address")

        # Personal Details
        student.father_name = request.POST.get("father_name")
        student.mother_name = request.POST.get("mother_name")
        student.category = request.POST.get("category")
        student.blood_group = request.POST.get("blood_group")
        student.aadhaar = request.POST.get("aadhaar")
        student.nationality = request.POST.get("nationality")
        student.religion = request.POST.get("religion")

        # Contact Details
        student.alternate_mobile = request.POST.get("alternate_mobile")
        student.emergency_contact = request.POST.get("emergency_contact")

        # Address
        student.city = request.POST.get("city")
        student.district = request.POST.get("district")
        student.state = request.POST.get("state")
        student.country = request.POST.get("country")
        student.pincode = request.POST.get("pincode")

        # Academic
        student.session = request.POST.get("session")
        student.qualification = request.POST.get("qualification")
        student.board_university = request.POST.get("board_university")
        student.passing_year = request.POST.get("passing_year") or None
        student.percentage = request.POST.get("percentage") or None

        # Guardian
        student.guardian_name = request.POST.get("guardian_name")
        student.guardian_relation = request.POST.get("guardian_relation")
        student.guardian_mobile = request.POST.get("guardian_mobile")
        student.guardian_email = request.POST.get("guardian_email")
        student.guardian_occupation = request.POST.get("guardian_occupation")

        # Rename uploaded files
        email_prefix = (
            student.email.replace("@", "_").replace(".", "_")
            if student.email
            else f"student_{student.id}"
        )

        upload_fields = [
            "photo",
            "signature",
            "aadhaar_file",
            "marksheet_10",
            "marksheet_12",
            "graduation_marksheet",
            "transfer_certificate",
            "character_certificate",
        ]

        for field in upload_fields:
            uploaded_file = request.FILES.get(field)
            if uploaded_file:
                ext = os.path.splitext(uploaded_file.name)[1]
                uploaded_file.name = f"{email_prefix}_{field}{ext}"
                setattr(student, field, uploaded_file)

        # Mark application submitted
        student.application_status = "Submitted"

        student.save()

        return redirect("student_application")

    return render(
        request,
        "student/student_application.html",
        {
            "student": student,
            "courses": courses,
            "submitted": False,
        },
    )

def application(request):
    students = Student.objects.all()
    return render(request, 'myadmin/application.html', {
        'students': students
    })

def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.name = request.POST.get("name")
        student.email = request.POST.get("email")
        student.password = request.POST.get("password")
        student.mobile = request.POST.get("mobile")
        student.course = request.POST.get("course")
        student.gender = request.POST.get("gender")
        student.dob = request.POST.get("dob")
        student.address = request.POST.get("address")

        student.save()

    return redirect("all_student")

def update_student_status(request, id):
    student = get_object_or_404(Student,id=id)
    if request.method == "POST":
        student.status = request.POST.get("status")
        student.save()
    return redirect("all_student")





#student fee submission
def student_fee_submission(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('student/student_login')
    student = get_object_or_404(Student, id=student_id)

    course = get_object_or_404(Courses, coursename=student.course)
    if request.method == "POST":
        student.payment_screenshot = request.FILES.get("payment_screenshot")
        student.payment_status = "Submitted"
        student.status = "Fee Submission"
        student.save()
        return redirect("student_fee_submission")
    return render(request, "student/student_fee_submission.html", {"student": student, "course": course})

def fees_status(request):
    students = Student.objects.select_related("course").all()

    return render(request, "myadmin/fees_status.html", {
        "students": students
    })

def verify_payment(request,id):
    student = get_object_or_404(Student,id=id)
    student.payment_status = "Verified"
    student.status = "Enrolled"
    student.payment_verified_date = timezone.now()
    student.save()
    return redirect("fees_status")

def reject_payment(request,id):
    student = get_object_or_404(Student,id=id)
    student.payment_status = "Pending"
    student.payment_screenshot = None
    student.status = "Fee Submission"
    student.save()
    return redirect("fees_status")

def enquity_delete(request,id):
    enquiry=get_object_or_404(Enquiry,id=id)
    enquiry.delete()
    return redirect('all_enquiry')