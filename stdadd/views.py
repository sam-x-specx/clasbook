# # from django.shortcuts import render

# # # Create your views here.
# # def stdadd(request):
# #     return render(request ,"stdadd/stdadder.html")

# # stdadd/views.py
# # stdadd/views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from django.utils import timezone
# from django.contrib import messages
# from clsbook.models import ClassBook, Student, AttendanceRecord
# from clsbook.forms import StudentForm


# def stdadd(request):
#     classbooks = ClassBook.objects.all()
#     selected = None
#     students = []
#     today = timezone.now().date()

#     # Get selected classbook from dropdown
#     classbook_id = request.GET.get('classbook')
#     if classbook_id:
#         selected = get_object_or_404(ClassBook, id=classbook_id)
#         students = selected.students.all()

#         # Pre-compute today's attendance for checkboxes
#         for student in students:
#             student.is_present_today = AttendanceRecord.objects.filter(
#                 student=student, date=today, present=True
#             ).exists()

#         # Password protection
#         session_classbook_id = request.session.get('classbook_id')
#         if session_classbook_id != selected.id:
#             if request.method == 'POST' and 'password' in request.POST:
#                 if selected.check_password(request.POST['password']):
#                     request.session['classbook_id'] = selected.id
#                     messages.success(request, 'Access granted!')
#                 else:
#                     messages.error(request, 'Wrong password!')
#                     return redirect('stdadd:password_prompt')
#             else:
#                 # Show password prompt
#                 return render(request, 'stdadd/password_prompt.html', {'classbook': selected})

#         # Handle Add Student
#         if request.method == 'POST' and 'add_student' in request.POST:
#             form = StudentForm(request.POST)
#             if form.is_valid():
#                 student = form.save(commit=False)
#                 student.class_book = selected
#                 student.save()
#                 messages.success(request, f'Student {student.first_name} {student.last_name} added!')
#                 return redirect(request.path + f'?classbook={selected.id}')
#         else:
#             form = StudentForm()

#         # Handle Attendance Submission
#         if request.method == 'POST' and 'attendance' in request.POST:
#             present_count = 0
#             for student in students:
#                 is_present = request.POST.get(f'att_{student.id}') == 'on'
#                 AttendanceRecord.objects.update_or_create(
#                     student=student,
#                     date=today,
#                     defaults={'present': is_present}
#                 )
#                 if is_present and not student.is_present_today:  # Only increment if newly marked present
#                     student.attendance_total += 1
#                     student.save()
#                     present_count += 1
#             messages.success(request, f'Attendance submitted for {today}! ({present_count} present)')
#             return redirect(request.path + f'?classbook={selected.id}')

#     else:
#         # No class selected
#         form = StudentForm()

#     return render(request, 'stdadd/stdadder.html', {
#         'classbooks': classbooks,
#         'selected': selected,
#         'students': students,
#         'today': today,
#         'student_form': StudentForm() if 'selected' not in locals() or not selected else StudentForm(),
#     })


# # # Optional: Keep reset_password if you want teacher to reset from here
# # # Or remove if it's only in clsbook app
# # def reset_password(request, pk):
# #     classbook = get_object_or_404(ClassBook, pk=pk)
# #     if request.method == 'POST':
# #         new_pass = request.POST.get('new_password')
# #         confirm_pass = request.POST.get('confirm_password')
# #         if new_pass and new_pass == confirm_pass:
# #             classbook.set_password(new_pass)
# #             classbook.save()
# #             messages.success(request, 'Password reset successfully!')
# #         else:
# #             messages.error(request, 'Passwords do not match or are empty.')
# #         return redirect('clsbook:home')
# #     return render(request, 'clsbook/reset_password.html', {'classbook': classbook})



# # def stdadd(request):
# #     classbooks = ClassBook.objects.all()
# #     selected = None
# #     students = []
# #     today = timezone.now().date()

# #     classbook_id = request.GET.get('classbook')
# #     if classbook_id:
# #         selected = get_object_or_404(ClassBook, id=classbook_id)
# #         students = selected.students.all()

# #         # Pre-compute today's attendance
# #         for student in students:
# #             student.is_present_today = AttendanceRecord.objects.filter(
# #                 student=student, date=today, present=True
# #             ).exists()

# #         # Always ask for password — no session storage
# #         if request.method == 'POST' and 'password' in request.POST:
# #             if selected.check_password(request.POST['password']):
# #                 # Password correct → show management page
# #                 pass  # continue below
# #             else:
# #                 messages.error(request, 'Incorrect password!')
# #                 return render(request, 'stdadd/password_prompt.html', {'classbook': selected})
# #         else:
# #             # First visit or back button → show password prompt
# #             return render(request, 'stdadd/password_prompt.html', {'classbook': selected})

# #         # === Below this line: only runs after correct password ===

# #         # Add Student
# #         if request.method == 'POST' and 'add_student' in request.POST:
# #             form = StudentForm(request.POST)
# #             if form.is_valid():
# #                 student = form.save(commit=False)
# #                 student.class_book = selected
# #                 student.save()
# #                 messages.success(request, f'Student {student.first_name} added!')
# #                 return redirect(f'/stdadd/?classbook={selected.id}')

# #         # Attendance Submit
# #         if request.method == 'POST' and 'attendance' in request.POST:
# #             present_count = 0
# #             for student in students:
# #                 is_present = request.POST.get(f'att_{student.id}') == 'on'
# #                 record, created = AttendanceRecord.objects.update_or_create(
# #                     student=student, date=today, defaults={'present': is_present}
# #                 )
# #                 if is_present and not student.is_present_today:
# #                     student.attendance_total += 1
# #                     student.save()
# #                     present_count += 1
# #             messages.success(request, f'Attendance submitted! ({present_count} present)')
# #             return redirect(f'/stdadd/?classbook={selected.id}')

# #     return render(request, 'stdadd/stdadder.html', {
# #         'classbooks': classbooks,
# #         'selected': selected,
# #         'students': students or [],
# #         'today': today,
# #         'student_form': StudentForm(),
# #     })

# def password_prompt(request):
#     return render(request ,"stdadd/password_prompt")




# # stdadd/views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from django.utils import timezone
# from django.contrib import messages
# from django.http import JsonResponse
# from clsbook.models import ClassBook, Student, AttendanceRecord
# from clsbook.forms import StudentForm
# from datetime import datetime, date
# from django.views.decorators.http import require_http_methods
# from django.views.decorators.csrf import csrf_exempt
# import json


# def stdadd(request):
#     classbooks = ClassBook.objects.all()
#     selected = None
#     students = []
#     today = timezone.now().date()
    
#     # Get the attendance date from POST or default to today
#     attendance_date_str = request.POST.get('attendance_date') or request.GET.get('date')
#     if attendance_date_str:
#         try:
#             attendance_date = datetime.strptime(attendance_date_str, '%Y-%m-%d').date()
#         except ValueError:
#             attendance_date = today
#     else:
#         attendance_date = today

#     # Get selected classbook from dropdown
#     classbook_id = request.GET.get('classbook')
#     if classbook_id:
#         selected = get_object_or_404(ClassBook, id=classbook_id)
#         students = selected.students.all()

#         # Pre-compute attendance for selected date
#         for student in students:
#             student.is_present_today = AttendanceRecord.objects.filter(
#                 student=student, date=attendance_date, present=True
#             ).exists()

#         # Password protection
#         session_classbook_id = request.session.get('classbook_id')
#         if session_classbook_id != selected.id:
#             if request.method == 'POST' and 'password' in request.POST:
#                 if selected.check_password(request.POST['password']):
#                     request.session['classbook_id'] = selected.id
#                     messages.success(request, 'Access granted!')
#                 else:
#                     messages.error(request, 'Wrong password!')
#                     return render(request, 'stdadd/password_prompt.html', {'classbook': selected})
#             else:
#                 # Show password prompt
#                 return render(request, 'stdadd/password_prompt.html', {'classbook': selected})

#         # Handle Add Student
#         if request.method == 'POST' and 'add_student' in request.POST:
#             form = StudentForm(request.POST)
#             if form.is_valid():
#                 student = form.save(commit=False)
#                 student.class_book = selected
#                 student.save()
#                 messages.success(request, f'Student {student.first_name} {student.last_name} added!')
#                 return redirect(request.path + f'?classbook={selected.id}')

#         # Handle Edit Student
#         if request.method == 'POST' and 'edit_student' in request.POST:
#             student_id = request.POST.get('student_id')
#             student = get_object_or_404(Student, id=student_id, class_book=selected)
            
#             student.first_name = request.POST.get('edit_first_name')
#             student.middle_name = request.POST.get('edit_middle_name', '')
#             student.last_name = request.POST.get('edit_last_name')
#             student.phone_number = request.POST.get('edit_phone_number')
#             student.email = request.POST.get('edit_email')
#             student.branch = request.POST.get('edit_branch')
#             student.college_regd = request.POST.get('edit_college_regd')
#             student.roll = request.POST.get('edit_roll')
#             student.address = request.POST.get('edit_address')
#             student.save()
            
#             messages.success(request, f'Student {student.first_name} {student.last_name} updated successfully!')
#             return redirect(request.path + f'?classbook={selected.id}')

#         # Handle Delete Student
#         if request.method == 'POST' and 'delete_student' in request.POST:
#             student_id = request.POST.get('delete_student_id')
#             student = get_object_or_404(Student, id=student_id, class_book=selected)
#             student_name = f"{student.first_name} {student.last_name}"
            
#             # Delete all attendance records for this student
#             AttendanceRecord.objects.filter(student=student).delete()
#             student.delete()
            
#             messages.success(request, f'Student {student_name} deleted successfully!')
#             return redirect(request.path + f'?classbook={selected.id}')

#         # Handle Attendance Submission with Date and Active Day
#         if request.method == 'POST' and 'attendance' in request.POST:
#             is_active_day = request.POST.get('is_active_day') == 'true'
#             present_count = 0
#             absent_count = 0
            
#             for student in students:
#                 is_present = request.POST.get(f'att_{student.id}') == 'on'
                
#                 # Update or create attendance record for the specific date
#                 record, created = AttendanceRecord.objects.update_or_create(
#                     student=student,
#                     date=attendance_date,
#                     defaults={'present': is_present, 'is_active_day': is_active_day}
#                 )
                
#                 if is_present:
#                     present_count += 1
#                 else:
#                     absent_count += 1
            
#             # Update class active day status if needed
#             if is_active_day:
#                 # Mark this date as an active class day
#                 # You might want to create a ClassDay model to track this
#                 pass
            
#             messages.success(
#                 request, 
#                 f'Attendance submitted for {attendance_date.strftime("%B %d, %Y")}! '
#                 f'({present_count} present, {absent_count} absent)'
#             )
#             return redirect(request.path + f'?classbook={selected.id}&date={attendance_date}')

#         # Get active days count for this class
#         active_days_count = AttendanceRecord.objects.filter(
#             student__class_book=selected,
#             is_active_day=True
#         ).values('date').distinct().count()

#     else:
#         active_days_count = 0

#     return render(request, 'stdadd/stdadder.html', {
#         'classbooks': classbooks,
#         'selected': selected,
#         'students': students,
#         'today': today,
#         'attendance_date': attendance_date,
#         'active_days_count': active_days_count,
#         'student_form': StudentForm(),
#     })


# # API endpoint to get active days (for calendar)
# def get_active_days(request):
#     classbook_id = request.GET.get('classbook')
#     if not classbook_id:
#         return JsonResponse({'active_days': []})
    
#     # Get all unique dates where attendance was marked as active day
#     active_days = AttendanceRecord.objects.filter(
#         student__class_book_id=classbook_id,
#         is_active_day=True
#     ).values_list('date', flat=True).distinct()
    
#     # Convert dates to string format
#     active_days_str = [day.strftime('%Y-%m-%d') for day in active_days]
    
#     return JsonResponse({'active_days': active_days_str})


# # API endpoint to get attendance for a specific date
# def get_attendance_by_date(request):
#     classbook_id = request.GET.get('classbook')
#     date_str = request.GET.get('date')
    
#     if not classbook_id or not date_str:
#         return JsonResponse({'error': 'Missing parameters'}, status=400)
    
#     try:
#         attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
#     except ValueError:
#         return JsonResponse({'error': 'Invalid date format'}, status=400)
    
#     # Get all students for this class with their attendance for the date
#     classbook = get_object_or_404(ClassBook, id=classbook_id)
#     students = classbook.students.all()
    
#     attendance_data = []
#     for student in students:
#         record = AttendanceRecord.objects.filter(
#             student=student,
#             date=attendance_date
#         ).first()
        
#         attendance_data.append({
#             'student_id': student.id,
#             'present': record.present if record else False,
#         })
    
#     # Check if this date is an active day
#     is_active = AttendanceRecord.objects.filter(
#         student__class_book=classbook,
#         date=attendance_date,
#         is_active_day=True
#     ).exists()
    
#     return JsonResponse({
#         'attendance': attendance_data,
#         'is_active_day': is_active
#     })


# # API endpoint to toggle active day status
# @require_http_methods(["POST"])
# def toggle_active_day(request):
#     try:
#         data = json.loads(request.body)
#         classbook_id = data.get('classbook_id')
#         date_str = data.get('date')
#         is_active = data.get('is_active', False)
        
#         if not classbook_id or not date_str:
#             return JsonResponse({'error': 'Missing parameters'}, status=400)
        
#         attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
#         classbook = get_object_or_404(ClassBook, id=classbook_id)
        
#         # Update all attendance records for this date
#         AttendanceRecord.objects.filter(
#             student__class_book=classbook,
#             date=attendance_date
#         ).update(is_active_day=is_active)
        
#         # If no records exist yet, we can create placeholder records
#         # or just wait until attendance is taken
        
#         # Get updated count
#         active_days_count = AttendanceRecord.objects.filter(
#             student__class_book=classbook,
#             is_active_day=True
#         ).values('date').distinct().count()
        
#         return JsonResponse({
#             'success': True,
#             'active_days_count': active_days_count
#         })
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)


# def password_prompt(request):
#     return render(request, "stdadd/password_prompt.html")































# # stdadd/views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from django.utils import timezone
# from django.contrib import messages
# from django.http import JsonResponse
# from clsbook.models import ClassBook, Student, AttendanceRecord, ClassDay
# from clsbook.forms import StudentForm
# from datetime import datetime, date
# from django.views.decorators.http import require_http_methods
# from django.views.decorators.csrf import csrf_exempt
# import json
# from django.shortcuts import get_object_or_404


# def stdadd(request):
#     classbooks = ClassBook.objects.all()
#     selected = None
#     students = []
#     today = timezone.now().date()
    
#     # Get the attendance date from POST or default to today
#     attendance_date_str = request.POST.get('attendance_date') or request.GET.get('date')
#     if attendance_date_str:
#         try:
#             attendance_date = datetime.strptime(attendance_date_str, '%Y-%m-%d').date()
#         except ValueError:
#             attendance_date = today
#     else:
#         attendance_date = today

#     # Get selected classbook from dropdown
#     classbook_id = request.GET.get('classbook')
#     if classbook_id:
#         selected = get_object_or_404(ClassBook, id=classbook_id)
#         students = selected.students.all()

#         # Pre-compute attendance for selected date
#         for student in students:
#             student.is_present_today = AttendanceRecord.objects.filter(
#                 student=student, date=attendance_date, present=True
#             ).exists()

#         # Password protection
#         session_classbook_id = request.session.get('classbook_id')
#         if session_classbook_id != selected.id:
#             if request.method == 'POST' and 'password' in request.POST:
#                 if selected.check_password(request.POST['password']):
#                     request.session['classbook_id'] = selected.id
#                     messages.success(request, 'Access granted!')
#                 else:
#                     messages.error(request, 'Wrong password!')
#                     return render(request, 'stdadd/password_prompt.html', {'classbook': selected})
#             else:
#                 # Show password prompt
#                 return render(request, 'stdadd/password_prompt.html', {'classbook': selected})

#         # Handle Add Student
#         if request.method == 'POST' and 'add_student' in request.POST:
#             form = StudentForm(request.POST)
#             if form.is_valid():
#                 student = form.save(commit=False)
#                 student.class_book = selected
#                 student.save()
#                 messages.success(request, f'Student {student.first_name} {student.last_name} added!')
#                 return redirect(request.path + f'?classbook={selected.id}')

#         # Handle Edit Student
#         if request.method == 'POST' and 'edit_student' in request.POST:
#             student_id = request.POST.get('student_id')
#             student = get_object_or_404(Student, id=student_id, class_book=selected)
            
#             student.first_name = request.POST.get('edit_first_name')
#             student.middle_name = request.POST.get('edit_middle_name', '')
#             student.last_name = request.POST.get('edit_last_name')
#             student.phone_number = request.POST.get('edit_phone_number')
#             student.email = request.POST.get('edit_email')
#             student.branch = request.POST.get('edit_branch')
#             student.college_regd = request.POST.get('edit_college_regd')
#             student.roll = request.POST.get('edit_roll')
#             student.address = request.POST.get('edit_address')
#             student.save()
            
#             messages.success(request, f'Student {student.first_name} {student.last_name} updated successfully!')
#             return redirect(request.path + f'?classbook={selected.id}')

#         # Handle Delete Student
#         if request.method == 'POST' and 'delete_student' in request.POST:
#             student_id = request.POST.get('delete_student_id')
#             student = get_object_or_404(Student, id=student_id, class_book=selected)
#             student_name = f"{student.first_name} {student.last_name}"
            
#             # Delete all attendance records for this student
#             AttendanceRecord.objects.filter(student=student).delete()
#             student.delete()
            
#             messages.success(request, f'Student {student_name} deleted successfully!')
#             return redirect(request.path + f'?classbook={selected.id}')

#         # Handle Attendance Submission with Date and Active Day
#         if request.method == 'POST' and 'attendance' in request.POST:
#             attendance_date_str = request.POST.get('attendance_date')
#             attendance_date = datetime.strptime(attendance_date_str, '%Y-%m-%d').date()
#             class_day = ClassDay.objects.filter(class_book=selected, date=attendance_date, is_active=True).first()
#             if not class_day:
#                 messages.error(request, 'Cannot submit attendance for non-class day!')
#                 return redirect(request.path + f'?classbook={selected.id}')

#             present_count = 0
#             absent_count = 0
            
#             for student in students:
#                 is_present = request.POST.get(f'att_{student.id}') == 'on'
                
#                 # Update or create attendance record for the specific date
#                 AttendanceRecord.objects.update_or_create(
#                     student=student,
#                     date=attendance_date,
#                     defaults={'present': is_present}
#                 )
                
#                 if is_present:
#                     present_count += 1
#                 else:
#                     absent_count += 1
            
#             messages.success(
#                 request, 
#                 f'Attendance submitted for {attendance_date.strftime("%B %d, %Y")}! '
#                 f'({present_count} present, {absent_count} absent)'
#             )
#             return redirect(request.path + f'?classbook={selected.id}&date={attendance_date}')

#         # Get active days count for this class
#         active_days_count = selected.class_days.filter(is_active=True).count()

#     else:
#         active_days_count = 0

#     return render(request, 'stdadd/stdadder.html', {
#         'classbooks': classbooks,
#         'selected': selected,
#         'students': students,
#         'today': today,
#         'attendance_date': attendance_date,
#         'active_days_count': active_days_count,
#         'student_form': StudentForm(),
#     })


# # API endpoint to get active days (for calendar)
# def get_active_days(request):
#     classbook_id = request.GET.get('classbook')
#     if not classbook_id:
#         return JsonResponse({'active_days': []})
    
#     # Get all unique dates where class day is active
#     active_days = ClassDay.objects.filter(class_book_id=classbook_id, is_active=True).values_list('date', flat=True)
    
#     # Convert dates to string format
#     active_days_str = [day.strftime('%Y-%m-%d') for day in active_days]
    
#     return JsonResponse({'active_days': active_days_str})


# # API endpoint to get attendance for a specific date
# def get_attendance_by_date(request):
#     classbook_id = request.GET.get('classbook')
#     date_str = request.GET.get('date')
    
#     if not classbook_id or not date_str:
#         return JsonResponse({'error': 'Missing parameters'}, status=400)
    
#     try:
#         attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
#     except ValueError:
#         return JsonResponse({'error': 'Invalid date format'}, status=400)
    
#     # Get all students for this class with their attendance for the date
#     classbook = get_object_or_404(ClassBook, id=classbook_id)
#     students = classbook.students.all()
    
#     attendance_data = []
#     for student in students:
#         record = AttendanceRecord.objects.filter(
#             student=student,
#             date=attendance_date
#         ).first()
        
#         attendance_data.append({
#             'student_id': student.id,
#             'present': record.present if record else False,
#         })
    
#     return JsonResponse({
#         'attendance': attendance_data
#     })


# # API endpoint to toggle active day status
# @csrf_exempt
# @require_http_methods(["POST"])
# def toggle_active_day(request):
#     try:
#         data = json.loads(request.body)
#         classbook_id = data.get('classbook_id')
#         date_str = data.get('date')
#         is_active = data.get('is_active')
        
#         if not classbook_id or not date_str:
#             return JsonResponse({'error': 'Missing parameters'}, status=400)
        
#         attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
#         classbook = get_object_or_404(ClassBook, id=classbook_id)
        
#         class_day, created = ClassDay.objects.get_or_create(
#             class_book=classbook,
#             date=attendance_date,
#             defaults={'is_active': is_active}
#         )
        
#         if not created:
#             class_day.is_active = is_active
#             class_day.save()
        
#         # Get updated count
#         class_days_count = classbook.class_days.filter(is_active=True).count()
        
#         return JsonResponse({
#             'success': True,
#             'class_days_count': class_days_count
#         })
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)


# def password_prompt(request):
#     return render(request, "stdadd/password_prompt.html")


# def get_class_day_number(request):
#     classbook_id = request.GET.get('classbook')
#     date_str = request.GET.get('date')

#     if not classbook_id or not date_str:
#         return JsonResponse({'error': 'Missing parameters'}, status=400)

#     try:
#         target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
#         classbook = get_object_or_404(ClassBook, id=classbook_id)

#         class_day = ClassDay.objects.filter(
#             class_book=classbook,
#             date=target_date,
#             is_active=True
#         ).first()

#         if not class_day:
#             return JsonResponse({'is_active': False, 'day_number': 0})

#         # Count active days up to and including this date
#         day_number = ClassDay.objects.filter(
#             class_book=classbook,
#             is_active=True,
#             date__lte=target_date
#         ).count()

#         return JsonResponse({
#             'is_active': True,
#             'day_number': day_number
#         })

#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)
    



# stdadd/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from clsbook.models import ClassBook, Student, AttendanceRecord, ClassDay
from clsbook.forms import StudentForm
from datetime import datetime, date
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json


def stdadd(request):
    classbooks = ClassBook.objects.all()
    selected = None
    students = []
    today = timezone.now().date()
    
    # Get the attendance date from POST or GET (calendar/date picker)
    attendance_date_str = request.POST.get('attendance_date') or request.GET.get('date')
    if attendance_date_str:
        try:
            attendance_date = datetime.strptime(attendance_date_str, '%Y-%m-%d').date()
        except ValueError:
            attendance_date = today
    else:
        attendance_date = today

    # Get selected classbook from dropdown
    classbook_id = request.GET.get('classbook')
    if classbook_id:
        selected = get_object_or_404(ClassBook, id=classbook_id)
        students = selected.students.all()

        # Pre-compute attendance for selected date
        for student in students:
            student.is_present_today = AttendanceRecord.objects.filter(
                student=student, date=attendance_date, present=True
            ).exists()

        # Password protection (session-based)
        session_classbook_id = request.session.get('classbook_id')
        if session_classbook_id != selected.id:
            if request.method == 'POST' and 'password' in request.POST:
                if selected.check_password(request.POST['password']):
                    request.session['classbook_id'] = selected.id
                    messages.success(request, 'Access granted!')
                else:
                    messages.error(request, 'Wrong password!')
                    return render(request, 'stdadd/password_prompt.html', {'classbook': selected})
            else:
                # Show password prompt
                return render(request, 'stdadd/password_prompt.html', {'classbook': selected})

        # ────────────────────────────────────────────────────────────────
        #               POST ACTION HANDLERS (only after password ok)
        # ────────────────────────────────────────────────────────────────

        # 1. Add Student
        if request.method == 'POST' and 'add_student' in request.POST:
            form = StudentForm(request.POST)
            if form.is_valid():
                student = form.save(commit=False)
                student.class_book = selected
                student.save()
                messages.success(request, f'Student {student.first_name} {student.last_name} added!')
                return redirect(request.path + f'?classbook={selected.id}')

        # 2. Edit Student
        if request.method == 'POST' and 'edit_student' in request.POST:
            student_id = request.POST.get('student_id')
            student = get_object_or_404(Student, id=student_id, class_book=selected)
            
            student.first_name = request.POST.get('edit_first_name')
            student.middle_name = request.POST.get('edit_middle_name', '')
            student.last_name = request.POST.get('edit_last_name')
            student.phone_number = request.POST.get('edit_phone_number')
            student.email = request.POST.get('edit_email')
            student.branch = request.POST.get('edit_branch')
            student.college_regd = request.POST.get('edit_college_regd')
            student.roll = request.POST.get('edit_roll')
            student.address = request.POST.get('edit_address')
            student.save()
            
            messages.success(request, f'Student {student.first_name} {student.last_name} updated successfully!')
            return redirect(request.path + f'?classbook={selected.id}')

        # 3. Delete Single Student
        if request.method == 'POST' and 'delete_student' in request.POST:
            student_id = request.POST.get('delete_student_id')
            student = get_object_or_404(Student, id=student_id, class_book=selected)
            student_name = f"{student.first_name} {student.last_name}"
            
            AttendanceRecord.objects.filter(student=student).delete()
            student.delete()
            
            messages.success(request, f'Student {student_name} deleted successfully!')
            return redirect(request.path + f'?classbook={selected.id}')

        # 4. NEW: Batch Delete Selected Students
        if request.method == 'POST' and 'batch_delete_students' in request.POST:
            student_ids = request.POST.getlist('student_ids[]')
            
            if not student_ids:
                messages.error(request, "No students were selected for deletion.")
                return redirect(request.path + f'?classbook={selected.id}&date={attendance_date_str}')

            try:
                students_to_delete = Student.objects.filter(
                    id__in=student_ids,
                    class_book=selected
                )
                
                count = students_to_delete.count()
                
                if count == 0:
                    messages.warning(request, "No valid students found to delete.")
                else:
                    # Clean up attendance records first
                    AttendanceRecord.objects.filter(student__in=students_to_delete).delete()
                    # Delete students
                    students_to_delete.delete()
                    
                    messages.success(request, f"Successfully deleted {count} student(s) and all their attendance records.")
                    
            except Exception as e:
                messages.error(request, f"Error during batch deletion: {str(e)}")
            
            return redirect(request.path + f'?classbook={selected.id}&date={attendance_date_str}')

        # 5. Normal Attendance Submission
        if request.method == 'POST' and 'attendance' in request.POST:
            attendance_date_str = request.POST.get('attendance_date')
            try:
                attendance_date = datetime.strptime(attendance_date_str, '%Y-%m-%d').date()
            except:
                attendance_date = today

            class_day = ClassDay.objects.filter(class_book=selected, date=attendance_date, is_active=True).first()
            if not class_day:
                messages.error(request, 'Cannot submit attendance for non-class day!')
                return redirect(request.path + f'?classbook={selected.id}&date={attendance_date_str}')

            present_count = 0
            absent_count = 0
            
            for student in students:
                is_present = request.POST.get(f'att_{student.id}') == 'on'
                
                AttendanceRecord.objects.update_or_create(
                    student=student,
                    date=attendance_date,
                    defaults={'present': is_present}
                )
                
                if is_present:
                    present_count += 1
                else:
                    absent_count += 1
            
            messages.success(
                request, 
                f'Attendance submitted for {attendance_date.strftime("%B %d, %Y")}! '
                f'({present_count} present, {absent_count} absent)'
            )
            return redirect(request.path + f'?classbook={selected.id}&date={attendance_date_str}')

        # 6. NEW: Delete ALL Attendance for Selected Date
        if request.method == 'POST' and 'delete_all_attendance' in request.POST:
            date_str = request.POST.get('delete_all_attendance_date')
            
            if not date_str:
                messages.error(request, "No date provided for attendance deletion.")
                return redirect(request.path + f'?classbook={selected.id}&date={attendance_date_str}')

            try:
                target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                
                deleted_count, _ = AttendanceRecord.objects.filter(
                    student__class_book=selected,
                    date=target_date
                ).delete()
                
                if deleted_count > 0:
                    messages.success(request, f"Deleted {deleted_count} attendance record(s) for {target_date.strftime('%b %d, %Y')}.")
                else:
                    messages.info(request, f"No attendance records found for {target_date.strftime('%b %d, %Y')}.")
                    
            except ValueError:
                messages.error(request, "Invalid date format.")
            except Exception as e:
                messages.error(request, f"Error clearing attendance: {str(e)}")
            
            return redirect(request.path + f'?classbook={selected.id}&date={date_str}')

        # Get active days count for banner
        active_days_count = selected.class_days.filter(is_active=True).count()

    else:
        active_days_count = 0

    return render(request, 'stdadd/stdadder.html', {
        'classbooks': classbooks,
        'selected': selected,
        'students': students,
        'today': today,
        'attendance_date': attendance_date,   # used in template for display
        'active_days_count': active_days_count,
        'student_form': StudentForm(),
    })


# ────────────────────────────────────────────────────────────────
#                     API ENDPOINTS (unchanged)
# ────────────────────────────────────────────────────────────────

def get_active_days(request):
    classbook_id = request.GET.get('classbook')
    if not classbook_id:
        return JsonResponse({'active_days': []})
    
    active_days = ClassDay.objects.filter(class_book_id=classbook_id, is_active=True).values_list('date', flat=True)
    active_days_str = [day.strftime('%Y-%m-%d') for day in active_days]
    
    return JsonResponse({'active_days': active_days_str})


def get_attendance_by_date(request):
    classbook_id = request.GET.get('classbook')
    date_str = request.GET.get('date')
    
    if not classbook_id or not date_str:
        return JsonResponse({'error': 'Missing parameters'}, status=400)
    
    try:
        attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)
    
    classbook = get_object_or_404(ClassBook, id=classbook_id)
    students = classbook.students.all()
    
    attendance_data = []
    for student in students:
        record = AttendanceRecord.objects.filter(
            student=student,
            date=attendance_date
        ).first()
        
        attendance_data.append({
            'student_id': student.id,
            'present': record.present if record else False,
        })
    
    return JsonResponse({'attendance': attendance_data})


@csrf_exempt
@require_http_methods(["POST"])
def toggle_active_day(request):
    try:
        data = json.loads(request.body)
        classbook_id = data.get('classbook_id')
        date_str = data.get('date')
        is_active = data.get('is_active')
        
        if not classbook_id or not date_str:
            return JsonResponse({'error': 'Missing parameters'}, status=400)
        
        attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        classbook = get_object_or_404(ClassBook, id=classbook_id)
        
        class_day, created = ClassDay.objects.get_or_create(
            class_book=classbook,
            date=attendance_date,
            defaults={'is_active': is_active}
        )
        
        if not created:
            class_day.is_active = is_active
            class_day.save()
        
        class_days_count = classbook.class_days.filter(is_active=True).count()
        
        return JsonResponse({
            'success': True,
            'class_days_count': class_days_count
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_class_day_number(request):
    classbook_id = request.GET.get('classbook')
    date_str = request.GET.get('date')

    if not classbook_id or not date_str:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        classbook = get_object_or_404(ClassBook, id=classbook_id)

        class_day = ClassDay.objects.filter(
            class_book=classbook,
            date=target_date,
            is_active=True
        ).first()

        if not class_day:
            return JsonResponse({'is_active': False, 'day_number': 0})

        day_number = ClassDay.objects.filter(
            class_book=classbook,
            is_active=True,
            date__lte=target_date
        ).count()

        return JsonResponse({
            'is_active': True,
            'day_number': day_number
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def password_prompt(request):
    return render(request, "stdadd/password_prompt.html")


