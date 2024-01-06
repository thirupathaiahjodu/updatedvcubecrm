from django.shortcuts import render
# Create your views here.
# views.py
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *
from django.urls import reverse,NoReverseMatch
from django.shortcuts import redirect 
from django.http import HttpResponseServerError
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from decimal import Decimal
from django.core.validators import MaxValueValidator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def register(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid()==True:
           print('hello')
           user=User.objects.create_superuser(
           username=form.cleaned_data['username'],
           email=form.cleaned_data['email'],
           password=form.cleaned_data['password'],)
           user.save()
           return HttpResponse('full loaded')
        return HttpResponse('succes')
        
    else:
        x=UserRegistrationForm()
        return render(request,'home/register.html',{'form':x})

def homefun(request):
    return render(request,'home/homepage.html')

def search_students(request):
    query = request.GET.get('query', '')
    results = []

    if query:
        results = Studentuser.objects.search(query).select_related('batch')

    return render(request, 'base.html', {'results': results})

def login_view(request):
    try:
        if request.method == 'POST':
            uname = request.POST['username']
            print(uname)
            pwd = request.POST['pwd']
            print(pwd)
            if User.objects.filter(username=uname).exists():
                print("User exists")
            else:
                 print("User does not exist")
            valid_user = authenticate(username=uname, password=pwd)
            print(valid_user)
            if valid_user is not None:
                login(request, valid_user)

                if valid_user.is_superuser:
                    return redirect('student_course_list')

                elif valid_user.is_staff:
                    return redirect('student_course_list')

                elif valid_user.is_active:
                    return redirect('student_home_url')

                else:
                    return HttpResponse('User not defined')

            else:
                error_message = 'Wrong password 🙄 Please check the password and try again..!!!!'
                login_url = reverse('login')
                return render(request, 'home/login.html',
                              {'error_message': error_message, 'login': login})

        return render(request, 'home/login.html')
    except Exception as e:
        return HttpResponse("Error: " + str(e))


def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('home')

# Create functions
def create_trainer(request):
    if request.method == 'POST':
        form = TrainerForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                return redirect('get_all_trainers')  # Redirect to the list view after successful form submission
        except Exception as e:
            return render_error_response(e, 'create_trainer')
    else:
        form = TrainerForm()

    return render(request, 'trainer/create_trainer.html', {'form': form})

def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                return redirect('get_all_courses')  # Redirect to the list view after successful form submission
        except ObjectDoesNotExist as e:
            return render_error_response(e, 'create_course', 'Trainer does not exist.')
        except Exception as e:
            print(f"An error occurred: {e}")
            return HttpResponseServerError()
    else:
        form = CourseForm()

    return render(request, 'course/create_course.html', {'form': form})


def create_batch(request):
    if request.method == 'POST':
        form = BatchForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                return redirect('get_all_batches')  # Redirect to the list view after successful form submission
        except ObjectDoesNotExist as e:
            return render_error_response(e, 'create_batch', 'Course does not exist.')
        except Exception as e:
            return render_error_response(e, 'create_batch')
    else:
        form = BatchForm()

    return render(request, 'batch/create_batch.html', {'form': form})

def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_course_list')
    else:
        form = StudentForm()

    return render(request, 'student/create_student.html', {'form': form})

import pandas as pd


def upload_student_data(request):
    try:
        if request.method == 'POST':
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)
            for index, row in df.iterrows():
                email = row['email']

                # Check if a student with the same email already exists
                if Student.objects.filter(email=email).exists():
                    # Skip creating a new entry for an existing student
                    continue

                name = row['name']
                mobile_number = row['mobile_number']
                alternative_number = row['alternative_number']
                gender = row['gender']
                graduation = row['graduation']
                date_of_joining = row['date_of_joining']
                course_name = row['course']
                batch_number = row['batch']
                trainer_name = row['trainer']
                admission_number=row['admission_number']
                g_stream=row['g_stream']
                g_yop=row['g_yop']
                g_percentag=row['g_percentag']
                intr_stream=row['intr_stream']
                intr_percentag=row['intr_percentag']
                intr_yop=row['intr_yop']
                ssc_percentag=row['ssc_percentag']
                ssc_yop=row['ssc_yop']
                training_mode=row['training_mode']
                
                try:
                    username=row['admission_number']
                    password=User.objects.make_random_password()
                    user = User.objects.create(
                        username=username,
                        password=make_password(password),
                        email=email
                    )
                    # Fetch Course and Batch objects based on their names
                    course = Course.objects.get(course_name=course_name)
                    batch = Batch.objects.get(batch_number=batch_number)
                    trainer = Trainer.objects.get(name=trainer_name)
                    # Create a new Student object
                    students = Student(
                        name=name,
                        email=email,
                        mobile_number=mobile_number,
                        alternative_number=alternative_number,
                        gender=gender,
                        graduation=graduation,
                        date_of_joining=date_of_joining,
                        course=course,
                        batch=batch,
                        status=row['status'],
                        admission_number=admission_number,
                        g_stream=g_stream,
                        g_yop=g_yop,
                        g_percentag=g_percentag,
                        intr_stream=intr_stream,
                        intr_percentag=intr_percentag,
                        intr_yop=intr_yop,
                        ssc_percentag=ssc_percentag,
                        ssc_yop=ssc_yop,
                        training_mode=training_mode


                    )
                    students.save()

                    # Add the trainer to the many-to-many relationship
                    students.trainer.set([trainer])
                    student_user_form = studentuserfrom({
                    'user': user,
                    'name':name,
                    'admission_number':admission_number,
                    'joining_date':date_of_joining,
                    'batch':batch,
                    'resume': '',
                    'course':course,
                    'image': '',
                    })
                    if student_user_form.is_valid():
                        student_user_form.save()
                    message = f'Thank you for Registering into VCube Software Solutions Pvt.Ltd.\n\n'
                    message += f'Username: {username}\nPassword: {password}\n\n'
                    message += f'Please keep your Credentials Confidential and change your password for security purposes.'
                    mail=settings.EMAIL_HOST_USER

        # Send email
                    send_mail(
                            'Your Account Details',
                                message,
                                mail,
                                [email]
                                )

                        
            
                except Course.DoesNotExist:
                    # Handle the case where the course does not exist
                    return HttpResponse(f"Error: Course '{course_name}' does not exist.")
                except Batch.DoesNotExist:
                    # Handle the case where the batch does not exist
                    return HttpResponse(f"Error: Batch '{batch_number}' does not exist.")
                except Trainer.DoesNotExist:
                    # Handle the case where the trainer does not exist
                    return HttpResponse(f"Error: Trainer '{trainer_name}' does not exist.")
          
            return redirect('student_upload_success')

        return render(request, 'student/student_upload.html')
    except Exception as e:
        return HttpResponse("Error: " + str(e))


def student_upload_success(request):
    return render(request, 'student/student_success.html')


def render_error_response(exception, template, message=None):
    response_data = {'error_message': str(exception)}
    if message:
        response_data['message'] = message
    return render(template, response_data)




# Get functions


def get_all_trainers(request):
    try:
        trainers = Trainer.objects.all()
        return render(request, 'trainer/trainer_list.html', {'trainers': trainers})
    except ObjectDoesNotExist as e:
        return render_error_response(e, 'get_all_trainers', 'No trainers found.')
    except Exception as e:
        return render_error_response(e, 'get_all_trainers', 'An error occurred while retrieving trainers.')

def get_all_courses(request):
    courses = Course.objects.all()
    return render(request, 'course/course_list.html', {'courses': courses})


def get_all_batches(request):
    try:
        batches = Batch.objects.all()
        return render(request, 'batch/batch_list.html', {'batches': batches})
    except NoReverseMatch as e:

        print(f"Error in URL reversal: {e}")
        return render(request, 'error_page.html', {'error_message': str(e)})


# def get_all_students(request, batch_id):
#     try:
#         # Assuming your Student model has a foreign key field 'batch'
#         students = Student.objects.filter(batch__id=batch_id)
#         return render(request, 'student/student_list.html', {'students': students, 'batch_id': batch_id})
#     except Exception as e:
#         return render_error_response(request, e, 'get_all_students')

    

class studentCourseListView(View):
    def get(self, request):
        courses = Course.objects.all()
        return render(request, 'student/course_list.html', {'courses': courses},)
    
class studentBatchListView(View):
    def get(self, request, course_id):
        batches = Batch.objects.filter(course__id=course_id)
        return render(request, 'student/batch_list.html', {'batches': batches, 'course_id': course_id})
    
class StudentListView(View):
    def get(self, request, batch_number):
        students = Student.objects.filter(batch__batch_number=batch_number)
        return render(request, 'student/student_list.html', {'students': students, 'batch_number': batch_number})
    
import logging
from django.shortcuts import render
from django.http import HttpResponseServerError
from django.core.exceptions import ObjectDoesNotExist

# Set up logging
logger = logging.getLogger(__name__)

def render_error_response(request, exception, view_name, error_message=None):
    """
    Handle and log errors, then render an error template.

    Parameters:
    - request: Django HTTP request object
    - exception: The exception that occurred
    - view_name: The name of the view where the error occurred
    - error_message: A custom error message to display (default: None)

    Returns:
    - Rendered HTML response with the error message
    """
    # Log the error for further analysis
    logger.error(f"Error in view '{view_name}': {exception}")

    context = {'error_message': error_message} if error_message else {}
    return render(request, 'error_template.html', context, status=500)

def get_trainer_by_id(request, trainer_id):
    try:
        trainer = Trainer.objects.get(pk=trainer_id)
        return render(request, 'trainer/trainer_detail.html', {'trainer': trainer})
    except ObjectDoesNotExist as e:
        return render_error_response(e, 'get_trainer_by_id', f'Trainer with ID {trainer_id} does not exist.')
    except Exception as e:
        return render_error_response(e, 'get_trainer_by_id')

def get_course_by_id(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
        return render(request, 'course/course_detail.html', {'course': course})
    except ObjectDoesNotExist as e:
        return render_error_response(e, 'get_course_by_id', f'Course with ID {course_id} does not exist.')
    except Exception as e:
        return render_error_response(e, 'get_course_by_id')


def batch_detail(request, batch_id):
    batch = get_object_or_404(Batch, pk=batch_id)
    return render(request, 'batch/batch_detail.html', {'batch': batch})



def get_student_by_id(request, student_id):
    try:
        student = Student.objects.get(pk=student_id)
        return render(request, 'student/student_detail.html', {'student': student})
    except ObjectDoesNotExist as e:
        return render_error_response(e, 'get_student_by_id', f'Student with ID {student_id} does not exist.')
    except Exception as e:
        return render_error_response(e, 'get_student_by_id')

def get_trainers(request):
    course_id = request.GET.get('course_id')
    try:
        course = Course.objects.get(pk=course_id)
        trainers = Trainer.objects.filter(course=course).values('id','name')
        return JsonResponse({'trainers': list(trainers)})
    except Course.DoesNotExist:
        return JsonResponse({'trainers': []})
        

# Update functions
def update_trainer(request, trainer_id):
    if request.method == 'POST':
        form = TrainerForm(request.POST, instance=get_object_or_404(Trainer, pk=trainer_id))
        try:
            if form.is_valid():
                form.save()
                return redirect('get_all_trainers')  # Redirect to the list view after successful form submission
        except ObjectDoesNotExist as e:
            return render_error_response(e, 'update_trainer', f'Trainer with ID {trainer_id} does not exist.')
        except Exception as e:
            return render_error_response(e, 'update_trainer')
    else:
        trainer = get_object_or_404(Trainer, pk=trainer_id)
        form = TrainerForm(instance=trainer)

    return render(request, 'trainer/update_trainer.html', {'form': form, 'trainer_id': trainer_id})

def update_course(request, course_id):
    if request.method == 'POST':
        form = CourseForm(request.POST,request.FILES, instance=get_object_or_404(Course, pk=course_id))
        try:
            if form.is_valid():
                form.save()
                return redirect('get_all_courses')  # Redirect to the list view after successful form submission
        except ObjectDoesNotExist as e:
            return render_error_response(e, 'update_course', f'Course with ID {course_id} does not exist.')
        except Exception as e:
            return render_error_response(e, 'update_course')
    else:
        course = get_object_or_404(Course, pk=course_id)
        form = CourseForm(instance=course)

    return render(request, 'course/update_course.html', {'form': form, 'course_id': course_id})

def update_batch(request, batch_id):
    if request.method == 'POST':
        form = BatchForm(request.POST, instance=get_object_or_404(Batch, pk=batch_id))
        try:
            if form.is_valid():
                form.save()
                return redirect('get_all_batches')  # Redirect to the list view after successful form submission
        except ObjectDoesNotExist as e:
            return render_error_response(e, 'update_batch', f'Batch with ID {batch_id} does not exist.')
        except Exception as e:
            return render_error_response(e, 'update_batch')
    else:
        batch = get_object_or_404(Batch, pk=batch_id)
        form = BatchForm(instance=batch)

    return render(request, 'batch/update_batch.html', {'form': form, 'batch_id': batch_id})


def update_student(request, student_id):
    if request.method == 'POST':
        try:
            student = get_object_or_404(Student, pk=student_id)
            form = StudentForm(request.POST, instance=student)
            
            if form.is_valid():
                form.save()
                batch_number = student.batch.batch_number
                return redirect('get_all_students', batch_number=batch_number)
        except ObjectDoesNotExist as e:
            return HttpResponse(f'Student with ID {student_id} does not exist.', status=404)
        except Exception as e:
            return HttpResponse('An error occurred during student update.', status=500)

    else:
        student = get_object_or_404(Student, pk=student_id)
        form = StudentForm(instance=student)

    return render(request, 'student/update_student.html', {'form': form, 'student_id': student_id,'batch_number': student.batch.batch_number})

# Delete functions


from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

def delete_trainer(request, trainer_id):
    try:
        trainer = Trainer.objects.get(pk=trainer_id)
        trainer_name = trainer.name
        trainer.delete()
        return render(request,'trainer/delete_success.html')
    except Trainer.DoesNotExist:
        return HttpResponse(f'Trainer with ID {trainer_id} does not exist.', status=404)
    except Exception as e:
        return HttpResponse(f'An error occurred: {str(e)}', status=500)


def delete_course(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
        course_name = course.course_name
        course.delete()
        return render(request,'trainer/delete_success.html')
    except Trainer.DoesNotExist:
        return HttpResponse(f'Trainer with ID {course_name} does not exist.', status=404)
    except Exception as e:
        return HttpResponse(f'An error occurred: {str(e)}', status=500)

def delete_batch(request, batch_id):
    try:
        batch = Batch.objects.get(pk=batch_id)
        batch_number = batch.batch_number
        batch.delete()
        return redirect('get_all_batches')
    except ObjectDoesNotExist as e:
        return render_error_response(e, 'delete_batch', f'Batch with ID {batch_id} does not exist.')


def delete_student(request, student_id):
    try:
        student = Student.objects.get(pk=student_id)
        student_name = student.name
        student.delete()
        batch_number = student.batch.batch_number
        return redirect('get_all_students', batch_number=batch_number)
    except ObjectDoesNotExist as e:
        return render_error_response(e, 'delete_student', f'Student with ID {student_id} does not exist.')
    except Exception as e:
        return render_error_response(e, 'delete_student')
    


def add_user(request):
    try:
        if request.method == 'POST':
            record_id = request.POST.get('record_id')
            student = Student.objects.get(id=record_id)
            # Extract course name and batch number
            course_name = student.course.course_name.lower()
            batch_number = f"b{student.batch.batch_number}"
            username = student.name.lower().replace(" ", "")
            # Create the admission number
            #admission_number = f"{course_name[:2]}{course_name[-10:-9]}{course_name[-5:-4]}-B-{str(Studentuser.objects.filter(batch=student.batch).count() + 1).zfill(3)}"


            password = User.objects.make_random_password()

            # Send the username, password, and message to the user via email

            message = f'Thank you for Registering into VCube Software Solutions Pvt.Ltd.\n\n'
            message += f'Username: {username}\nPassword: {password}\n\n'
            message += f'Please keep your Credentials Confidential and change your password for security purposes.'

            '''try:
                send_mail(
                    'Your Account Details',
                    message,
                    'shivayadav12088@gmail.com',
                    [student.email],
                    fail_silently=False,
                )
                student.status = 'Yes'
            except Exception as e:
                student.status = 'No'''

            user = User.objects.create(
                username=username,
                password=make_password(password),
                email=student.email
                )

            student_user_form = studentuserfrom({
                'user': user,
                'admission_number':student.admission_number,
                'joining_date': student.date_of_joining,
                'batch': student.batch,
                'resume': '',
                'course': student.course,
                'image': '',
            })

            # Directly save the form without checking is_valid
            student_user_form.save()

            return redirect('student_upload_success')  # Replace 'student_upload_success' with your actual success URL

        return HttpResponseNotAllowed(['POST'])
    except Exception as e:
        return HttpResponse("Error: " + str(e))


class CourseListView(View):
    def get(self, request):
        courses = Course.objects.all()
        return render(request, 'show/course_list.html', {'courses': courses},)

class BatchListView(View):
    def get(self, request, course_id):
        batches = Batch.objects.filter(course__id=course_id)
        return render(request, 'show/batch_list.html', {'batches': batches, 'course_id': course_id})

class StudentuserListView(View):
    def get(self, request, batch_number):
        batch = Batch.objects.get(batch_number=batch_number)
        students = Studentuser.objects.filter(batch__batch_number=batch_number)
        return render(request, 'show/student_list.html', {'students': students, 'batch_number': batch_number})
    


def staff_student_details(request, student_id):
    student = get_object_or_404(Studentuser, id=student_id)
    tests = Test.objects.filter(student=student)
    attendance = Attendance.objects.filter(student=student)
    labs = lab.objects.filter(student=student)
    soft_skills = softskills.objects.filter(student=student)
    interviews = Interview.objects.filter(student=student)
    mocks=Mockinterview.objects.filter(student=student)

    total_test_attendance_ratio, total_test_marks, total_max_test_marks = calculate_total_marks_and_attendance(Test, student, count_present=True)
    total_interview_attendance_ratio, total_interview_marks, total_max_interview_marks = calculate_total_marks_and_attendance(Interview, student, count_present=True)
    attendance_total_days, attendance_total_present, attendance_ratio = calculate_attendance(Attendance, student)
    total_mock_attendance_ratio, total_mock_marks, total_max_mock_marks = calculate_total_marks_and_attendance(Mockinterview, student, count_present=True)

    # Lab
    lab_total_days, lab_total_present, lab_ratio = calculate_attendance(lab, student)

    # Communication
    communication_total_days, communication_total_present, communication_ratio = calculate_attendance(communication, student)

    # Softskills
    softskills_total_days, softskills_total_present, softskills_ratio = calculate_attendance(softskills, student)
    # Example usage
    accepted_count, rejected_count , not_attended= calculate_interview_stats(Interview,student)
    #changed

    context = {
        'student': student,
        'mocks':mocks,
        'tests': tests,
        'attendance': attendance,
        'labs': labs,
        'soft_skills': soft_skills,
        'interviews': interviews,
        'total_test_marks': total_test_marks,
        'total_max_test_marks': total_max_test_marks,
        'test_attendance_ratio': total_test_attendance_ratio,
        'total_interview_marks': total_interview_marks,
        'total_max_interview_marks': total_max_interview_marks,
        'interview_attendance_ratio': total_interview_attendance_ratio,
        'attendance_total_days': attendance_total_days,
        'attendance_total_present': attendance_total_present,
        'attendance_ratio': attendance_ratio,
        'lab_total_days': lab_total_days,
        'lab_total_present': lab_total_present,
        'lab_ratio': lab_ratio,
        'communication_total_days': communication_total_days,
        'communication_total_present': communication_total_present,
        'communication_ratio': communication_ratio,
        'softskills_total_days': softskills_total_days,
        'softskills_total_present': softskills_total_present,
        'softskills_ratio': softskills_ratio,
        'total_mock_marks': total_mock_marks,
        'total_max_mock_marks': total_max_mock_marks,
        'mock_attendance_ratio': total_mock_attendance_ratio,
        'accepted_count':accepted_count,
        'rejected_count':rejected_count,
        'not_attended':not_attended

    }

    return render(request, 'show/student_detail.html', context)

def edit_student_user(request, student_id):
    student = get_object_or_404(Studentuser, id=student_id)

    if request.method == 'POST':
        form = studentuserfrom(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            batch_number = student.batch.batch_number
            return redirect('student-list', batch_number=batch_number)  # Change 'student_profile' to your actual profile view name
    else:
        form = studentuserfrom(instance=student)

    return render(request, 'show/edit_student_user.html', {'form': form, 'student': student})


# //////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////student home......................................................................................
# .....................................................................................///////////////////
from django.db.models import Sum

def calculate_total_marks_and_attendance(model, student, count_present=False):
    total_present = 0
    total_days = model.objects.filter(student=student).count()
    max_marks = 0
    total_marks = 0  # Default value

    if count_present and hasattr(model, 'present'):
        total_present = model.objects.filter(student=student, present=True).count()

    if hasattr(model, 'marks'):
        total_marks = model.objects.filter(student=student).aggregate(total=Sum('marks'))['total'] or 0

        if hasattr(model, 'max_marks'):
            max_marks = model.objects.filter(student=student).aggregate(total=Sum('max_marks'))['total'] or 0

    attendance_ratio = f"{total_present}/{total_days}" if total_days > 0 else "N/A"

    return attendance_ratio, total_marks, max_marks

from django.db.models import Count

def calculate_attendance(model, student):
    total_days = model.objects.filter(student=student).count()
    total_present = model.objects.filter(student=student, present=True).count()
    
    attendance_ratio = f"{total_present}/{total_days}" if total_days > 0 else "N/A"

    return total_days, total_present, attendance_ratio

def calculate_interview_stats(model, student):
    accepted_count = model.objects.filter(student=student, student_status='Accepted').count()
    rejected_count = model.objects.filter(student=student, student_status='Rejected').count()
    not_attended=model.objects.filter(student=student, student_status='None').count()

    return accepted_count, rejected_count,not_attended




def student_home(request):
    try:
        student = request.user.studentuser
        tests = Test.objects.filter(student=student)
        attendance = Attendance.objects.filter(student=student)
        labs = lab.objects.filter(student=student)
        soft_skills = softskills.objects.filter(student=student)
        interviews = Interview.objects.filter(student=student)

        total_test_attendance_ratio, total_test_marks, total_max_test_marks = calculate_total_marks_and_attendance(Test, student, count_present=True)
        total_interview_attendance_ratio, total_interview_marks, total_max_interview_marks = calculate_total_marks_and_attendance(Interview, student, count_present=True)
        attendance_total_days, attendance_total_present, attendance_ratio = calculate_attendance(Attendance, student)
        total_mock_attendance_ratio, total_mock_marks, total_max_mock_marks = calculate_total_marks_and_attendance(Mockinterview, student, count_present=True)


        # Lab
        lab_total_days, lab_total_present, lab_ratio = calculate_attendance(lab, student)
        
        # Communication
        communication_total_days, communication_total_present, communication_ratio = calculate_attendance(communication, student)

        # Softskills
        softskills_total_days, softskills_total_present, softskills_ratio = calculate_attendance(softskills, student)

        accepted_count, rejected_count,not_attended = calculate_interview_stats(Interview,student)

        context = {
            'student': student,
            'tests': tests,
            'attendance': attendance,
            'labs': labs,
            'soft_skills': soft_skills,
            'interviews': interviews,
            'total_test_marks': total_test_marks,
            'total_max_test_marks': total_max_test_marks,
            'test_attendance_ratio': total_test_attendance_ratio,
            'total_interview_marks': total_interview_marks,
            'total_max_interview_marks': total_max_interview_marks,
            'interview_attendance_ratio': total_interview_attendance_ratio,
            'attendance_total_days': attendance_total_days,
            'attendance_total_present': attendance_total_present,
            'attendance_ratio': attendance_ratio,
            'lab_total_days': lab_total_days,
            'lab_total_present': lab_total_present,
            'lab_ratio': lab_ratio,
            'communication_total_days': communication_total_days,
            'communication_total_present': communication_total_present,
            'communication_ratio': communication_ratio,
            'softskills_total_days': softskills_total_days,
            'softskills_total_present': softskills_total_present,
            'softskills_ratio': softskills_ratio,
            'total_mock_marks': total_mock_marks,
            'total_max_mock_marks': total_max_mock_marks,
            'mock_attendance_ratio': total_mock_attendance_ratio,
            'accepted_count':accepted_count,
            'rejected_count':rejected_count,
            'not_attended':not_attended
        }

        return render(request, 'student_user/student_profile.html', context)

    except ObjectDoesNotExist:
        return render(request, 'error_template.html')
#upload data from excel
import math

def upload_test_data(request):
    try:
        if request.method == 'POST':
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            for index, row in df.iterrows():
                admission_number = row['admission_number']
                test_date = row['test_date']
                
                # Check for NaN values in the 'marks' column
                marks = row['marks']
                if isinstance(marks, float) and math.isnan(marks):
                    marks = 0

                # Check for NaN values and empty strings in the 'present' column
                present = row['present']
                if pd.isna(present) or present == '' or str(present).strip().lower() == 'false':
                    present = False
                else:
                    present = True

                try:
                    student = Studentuser.objects.get(admission_number=admission_number)
                except Studentuser.DoesNotExist:
                    return HttpResponse(f"Error: Studentuser with admission number '{admission_number}' does not exist.")

                test = Test(
                    student=student,
                    test_date=test_date,
                    marks=Decimal(marks),
                    present=present,
                    max_marks=row.get('max_marks', 10),
                )
                test.save()

            return render(request, 'upload/success.html')

        return render(request, 'upload/test_upload.html')
    except Exception as e:
        return HttpResponse("Error: " + str(e))
    
def upload_attendance_data(request):
    try:
        if request.method == 'POST':
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            for index, row in df.iterrows():
                admission_number = row['admission_number']
                date = row['date']
                present = row.get('present', False)  # Default to False if 'present' column is not present

                student = Studentuser.objects.get(admission_number=admission_number)
                

                attendance = Attendance(
                    student=student,
                    date=date,
                    present=present,
                )
                attendance.save()
                

            return render(request, 'upload/success.html')

        return render(request, 'upload/attendance_upload.html')
    except Exception as e:
        return HttpResponse("Error: " + str(e))
    
def upload_lab_data(request):
    try:
        if request.method == 'POST':
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            for index, row in df.iterrows():
                admission_number = row['admission_number']
                date = row['date']

                  # Default to False if 'present' column is not present
                present = row['present']
                if pd.isna(present) or present == '' or str(present).strip().lower() == 'false':
                    present = False
                else:
                    present = True
                try:
                    student = Studentuser.objects.get(admission_number=admission_number)
                except Studentuser.DoesNotExist:
                    return HttpResponse(f"Error: Studentuser with admission number '{admission_number}' does not exist.")


                lab_instance = lab(
                    student=student,
                    date=date,
                    present=present,
                )
                lab_instance.save()

            return render(request, 'upload/success.html')

        return render(request, 'upload/lab_upload.html')
    except Exception as e:
        return HttpResponse("Error: " + str(e))


    
def upload_softskills_data(request):
    try:
        if request.method == 'POST':
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            for index, row in df.iterrows():
                admission_number = row['admission_number']
                date = row['date']
                topic = row['topic']
                present = row['present']
                if pd.isna(present) or present == '' or str(present).strip().lower() == 'false':
                    present = False
                else:
                    present = True
                try:
                    student = Studentuser.objects.get(admission_number=admission_number)
                except Studentuser.DoesNotExist:
                    return HttpResponse(f"Error: Studentuser with admission number '{admission_number}' does not exist.")

                softskills_instance = softskills(
                    student=student,
                    date=date,
                    present=present,
                    topic=topic,
                )
                softskills_instance.save()

            return render(request, 'upload/success.html')

        return render(request, 'upload/softskills_upload.html')
    except Exception as e:
        return HttpResponse("Error: " + str(e))

def upload_interview_data(request):
    try:
        if request.method == 'POST':
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            for index, row in df.iterrows():
                admission_number = row['admission_number']
                interview_date = row['date']
                company_name=row['company_name']
                status=row['student_status']
                present = row.get('present', False)  # Default to False if 'present' column is not present
                if pd.isna(present) or present == '' or str(present).strip().lower() == 'false':
                    present = False
                else:
                    present = True
                try:
                    student = Studentuser.objects.get(admission_number=admission_number)
                except Studentuser.DoesNotExist:
                    return HttpResponse(f"Error: Studentuser with admission number '{admission_number}' does not exist.")


                interview_instance = Interview(
                    student=student,
                    date=interview_date,
                    present=present,
                    company_name=company_name,
                    student_status=status
                )
                interview_instance.save()

            return render(request, 'upload/success.html')

        return render(request, 'upload/interview_upload.html')
    except Exception as e:
        return HttpResponse("Error: " + str(e))



from django.utils import timezone

@login_required
def update_profile(request):
    if request.method == 'POST':
        # Handle image update
        if 'image' in request.FILES:
            image = request.FILES['image']
            request.user.studentuser.image = image
            request.user.studentuser.save()

        # Handle resume update
        if 'resume' in request.FILES:
            resume = request.FILES['resume']
            # Append current date and time to the file name to make it unique
            timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
            resume.name = f"{timestamp}_{resume.name}"
            request.user.studentuser.resume = resume
            request.user.studentuser.save()

        return redirect('student_home_url')  # Redirect to the user's profile page

    return render(request, 'student_user/update_proffile.html')


def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        #print(form)
        if form.is_valid():
           # print('hello')
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'home/change_password.html', {'form': form})

from django.contrib.auth.views import PasswordResetView

def custom_forgot_password(request):
    # Custom logic before rendering the forgot password page
    context = {
        'custom_message': 'Enter your email to reset your password.',
    }
    return PasswordResetView.as_view(extra_context=context)(request, template_name='home/forgot_password.html')


from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

class YourPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'home/confirmation.html'  
    success_url = reverse_lazy('login')  

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):

        return super().form_invalid(form)

from django.contrib.auth.views import PasswordResetDoneView
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'home/custom_password_reset_done.html'


def upload_mock_data(request):
    try:
        if request.method == 'POST':
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            for index, row in df.iterrows():
                admission_number = row['admission_number']
                date = row['date']
                present = row.get('present', False)  # Default to False if 'present' column is not present
                marks=row['marks']
                max_marks=row['max_marks']
                if isinstance(marks, float) and math.isnan(marks):
                    marks = 0
                # Check for NaN values and empty strings in the 'present' column
                present = row['present']
                if pd.isna(present) or present == '' or str(present).strip().lower() == 'false':
                    present = False
                else:
                    present = True

                try:
                    student = Studentuser.objects.get(admission_number=admission_number)
                except Studentuser.DoesNotExist:
                    return HttpResponse(f"Error: Studentuser with admission number '{admission_number}' does not exist.")

    
                #student = Studentuser.objects.get(admission_number=admission_number)

                mock = Mockinterview(
                    student=student,
                    date=date,
                    marks=Decimal(marks),
                    present=present,
                    max_marks=row.get('max_marks', 10),
                )
                mock.save()

            return render(request, 'upload/success.html')

        return render(request, 'upload/mock_upload.html')
    except Exception as e:
        return HttpResponse("Error: " + str(e))

def mail(request,student_email):
    #student = get_object_or_404(User, email=student_email)
    try:
        student = get_object_or_404(User, email=student_email)
        username = student.username  # Assuming username is the actual attribute to retrieve the username
        print(username)
        password = User.objects.make_random_password()
        message = f'Thank you for Registering into VCube Software Solutions Pvt.Ltd.\n\n'
        message += f'Username: {username}\nPassword: {password}\n\n'
        message += f'Please keep your Credentials Confidential and change your password for security purposes.'
        mail=settings.EMAIL_HOST_USER

        # Send email
        send_mail(
            'Your Account Details',
            message,
            mail,
            [student.email]
        )
        # Update student status
        #student.save()
        return HttpResponse('email set succesfully')
    except Exception as e:
        return HttpResponse('ERROR:' +str(e))

# def mail(request, student_email):
#     try:
#         student = get_object_or_404(User, email=student_email)
#         username = student.username
#         password = User.objects.make_random_password()
#         message = f'Thank you for registering into VCube Software Solutions Pvt.Ltd.\n\n'
#         message += f'Username: {username}\nPassword: {password}\n\n'
#         message += f'Please keep your credentials confidential and change your password for security purposes.'

#         # Explicitly set email configuration
#         mail_settings = {
#             'subject': 'Your Account Details',
#             'message': message,
#             'from_email': settings.DEFAULT_FROM_EMAIL,
#             'recipient_list': [student.email],
#             'fail_silently': False,  # Set to True to suppress errors (not recommended during development)
#         }

#         # Send email
#         send_mail(**mail_settings)

#         return HttpResponse('Email sent successfully')
#     except Exception as e:
#         return HttpResponse('ERROR: ' + str(e))