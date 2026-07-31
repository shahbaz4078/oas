from django.db import models
from django.db import models

class Student(models.Model):
    STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('document verification', 'Document Verification'),
    ('enrolled', 'Enrolled'),
    ('rejected', 'Rejected'),
    )

    APPLICATION_STATUS = [
    ("Not Submitted", "Not Submitted"),
    ("Submitted", "Submitted"),
    ("Approved", "Approved"),
    ("Rejected", "Rejected"),
     ]

    application_status = models.CharField(
    max_length=20,
    choices=APPLICATION_STATUS,
    default="Not Submitted"
 )

    # Existing Fields
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    course = models.ForeignKey("Courses",
    on_delete=models.SET_NULL,
    null=True,
    blank=True
     )
    gender = models.CharField(max_length=10)
    dob = models.TextField()
    address = models.TextField()
    status = models.CharField(max_length=20, default="Pending")


    # Additional Personal Details
    father_name = models.CharField(max_length=100,blank=True, null=True)
    mother_name = models.CharField(max_length=100,blank=True, null=True)
    category = models.CharField(max_length=20, blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    aadhaar = models.CharField(max_length=12,blank=True, null=True)
    nationality = models.CharField(max_length=50, default="Indian")
    religion = models.CharField(max_length=50,blank=True, null=True)

    # Contact Details
    alternate_mobile = models.CharField(max_length=15, blank=True, null=True)
    emergency_contact = models.CharField(max_length=15,blank=True, null=True)

    # Address Details
    city = models.CharField(max_length=100,blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default="India")
    pincode = models.CharField(max_length=6,blank=True, null=True)

    # Academic Details
    session = models.CharField(max_length=20,blank=True, null=True)
    qualification = models.CharField(max_length=100,blank=True, null=True)
    board_university = models.CharField(max_length=100 , blank=True, null=True)
    passing_year = models.PositiveIntegerField( blank=True, null=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # Guardian Details
    guardian_name = models.CharField(max_length=100,blank=True, null=True)
    guardian_relation = models.CharField(max_length=50,blank=True, null=True)
    guardian_mobile = models.CharField(max_length=15,blank=True, null=True)
    guardian_email = models.EmailField(blank=True, null=True)
    guardian_occupation = models.CharField(max_length=100,blank=True, null=True)
    assign_course=models.CharField(max_length=100,blank=True, null=True)


    # Documents
    photo = models.ImageField(upload_to='application/',blank=True, null=True)
    signature = models.ImageField(upload_to='applications/',blank=True, null=True)
    aadhaar_file = models.FileField(upload_to='applications/', blank=True, null=True)
    marksheet_10 = models.FileField(upload_to='applications/',blank=True, null=True)
    marksheet_12 = models.FileField(upload_to='applications/', blank=True, null=True)
    graduation_marksheet = models.FileField(upload_to='applications/', blank=True, null=True)
    transfer_certificate = models.FileField(upload_to='applications/', blank=True, null=True)
    character_certificate = models.FileField(upload_to='applications/', blank=True, null=True)

    PAYMENT_STATUS = (
    ("Pending", "Pending"),
    ("Submitted", "Submitted"),
)
    payment_status = models.CharField(max_length=20,choices=PAYMENT_STATUS, default="Pending")
    payment_screenshot = models.ImageField(upload_to='payment_screenshots/', blank=True, null=True)
    course_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    payment_verified_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # Record Information
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name
    

class Enquiry(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    mobile=models.CharField(max_length=10)
    course=models.CharField(max_length=50)
    message=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Courses(models.Model):
    coursename=models.CharField(max_length=100)
    session=models.CharField(max_length=100)
    duration=models.CharField(max_length=100)
    fees=models.CharField(max_length=100)

    def __str__(self):
        return self.coursename