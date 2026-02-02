# from django.shortcuts import render

# # Create your views here.
# def studentviewer(request):
#     return render(request ,"studentviewer/studentviewerhome.html")

# studentviewer/views.py
# from django.shortcuts import render
# from clsbook.models import ClassBook, Student

# def studentviewer(request):
#     classbooks = ClassBook.objects.all()
#     selected_class = request.GET.get('classbook')
#     students = Student.objects.all()

#     if selected_class:
#         students = students.filter(class_book_id=selected_class)

#     return render(request, 'studentviewer/studentviewerhome.html', {
#         'classbooks': classbooks,
#         'students': students,
#         'selected_class': selected_class,
#     })


# # studentviewer/views.py
# from django.shortcuts import render
# from django.db.models import Count, Sum
# from clsbook.models import ClassBook, Student, AttendanceRecord
# from django.utils import timezone

# def studentviewer(request):
#     classbooks = ClassBook.objects.all()
#     selected_class_id = request.GET.get('classbook')
#     section_filter = request.GET.get('section')

#     students = Student.objects.all()

#     if selected_class_id:
#         students = students.filter(class_book_id=selected_class_id)
#         selected_class = ClassBook.objects.get(id=selected_class_id)
#     else:
#         selected_class = None

#     if section_filter:
#         students = students.filter(class_book__section=section_filter)

#     # Calculate stats
#     total_students = Student.objects.count()
#     today = timezone.now().date()
#     total_present_today = AttendanceRecord.objects.filter(date=today, present=True).count()

#     # Add percentage to each student
#     for s in students:
#         if s.attendance_total > 0:
#             # Simple percentage (you can improve with total classes taken)
#             s.attendance_percentage = (s.attendance_total / max(1, AttendanceRecord.objects.filter(student=s).count())) * 100
#         else:
#             s.attendance_percentage = 0

#     # Get unique sections for filter
#     all_sections = ClassBook.objects.values_list('section', flat=True).distinct()

#     return render(request, 'studentviewer/studentviewerhome.html', {
#         'classbooks': classbooks,
#         'students': students,
#         'selected_class': selected_class,
#         'total_students': total_students,
#         'total_present_today': total_present_today,
#         'all_sections': all_sections,
#     })












# # studentviewer/views.py
# from django.shortcuts import render
# from django.db.models import Q, Count
# from clsbook.models import ClassBook, Student, AttendanceRecord, ClassDay  # Assuming ClassDay model for active days
# from django.utils import timezone

# def studentviewer(request):
#     classbooks = ClassBook.objects.all()
#     selected_class_id = request.GET.get('classbook')
#     search_query = request.GET.get('search_query', '')
#     percentage_filter = request.GET.get('percentage_filter', '')

#     students = Student.objects.all()

#     if selected_class_id:
#         students = students.filter(class_book_id=selected_class_id)

#     # Search filter
#     if search_query:
#         students = students.filter(
#             Q(first_name__icontains=search_query) |
#             Q(middle_name__icontains=search_query) |
#             Q(last_name__icontains=search_query) |
#             Q(college_regd__icontains=search_query) |
#             Q(roll__icontains=search_query)
#         )

#     # Calculate stats for each student
#     for s in students:
#         # Total active classes for the student's class
#         total_classes = ClassDay.objects.filter(class_book=s.class_book, is_active=True).count()
#         s.total_classes = total_classes

#         # Attended (present)
#         attended = AttendanceRecord.objects.filter(student=s, present=True).count()
#         s.attended = attended

#         # Absent
#         s.absent = total_classes - attended

#         # Percentage
#         s.percentage = (attended / total_classes * 100) if total_classes > 0 else 0

#     # Percentage filter
#     if percentage_filter == 'below_10':
#         students = [s for s in students if s.percentage < 10]
#     elif percentage_filter == 'below_45':
#         students = [s for s in students if s.percentage < 45]
#     elif percentage_filter == 'below_60':
#         students = [s for s in students if s.percentage < 60]
#     elif percentage_filter == '60_to_75':
#         students = [s for s in students if 60 <= s.percentage <= 75]
#     elif percentage_filter == 'above_75':
#         students = [s for s in students if s.percentage > 75]
        

#     # Get unique sections for filter (if needed, but not used in template yet)
#     all_sections = ClassBook.objects.values_list('section', flat=True).distinct()

#     return render(request, 'studentviewer/studentviewerhome.html', {
#         'classbooks': classbooks,
#         'students': students,
#         'selected_class': selected_class_id,
#         'search_query': search_query,
#         'percentage_filter': percentage_filter,
#         'all_sections': all_sections,
#     })











# # studentviewer/views.py
# from django.shortcuts import render
# from django.db.models import Q, Count
# from clsbook.models import ClassBook, Student, AttendanceRecord, ClassDay
# from django.utils import timezone
# from datetime import date

# def studentviewer(request):
#     classbooks = ClassBook.objects.all()
#     selected_class_id = request.GET.get('classbook')
#     search_query = request.GET.get('search_query', '')
#     percentage_filter = request.GET.get('percentage_filter', '')

#     today = timezone.now().date()   # or date.today()

#     students = Student.objects.all()

#     # ── Class filter ────────────────────────────────────────────────
#     selected_class = None
#     teacher_name = None

#     if selected_class_id:
#         try:
#             selected_class = ClassBook.objects.get(id=selected_class_id)
#             students = students.filter(class_book_id=selected_class_id)
#             teacher_name = selected_class.teacher_name  # assuming this field exists
#         except ClassBook.DoesNotExist:
#             selected_class_id = None  # fallback to all

#     # ── Search filter ───────────────────────────────────────────────
#     if search_query:
#         students = students.filter(
#             Q(first_name__icontains=search_query) |
#             Q(middle_name__icontains=search_query) |
#             Q(last_name__icontains=search_query) |
#             Q(college_regd__icontains=search_query) |
#             Q(roll__icontains=search_query)
#         )

#     # ── Calculate today's present & absent counts ──────────────────
#     present_today = 0
#     absent_today = 0

#     if selected_class:
#         # Only this class
#         present_today = AttendanceRecord.objects.filter(
#             student__class_book=selected_class,
#             date=today,
#             present=True
#         ).count()

#         total_students_today = Student.objects.filter(class_book=selected_class).count()
#         absent_today = total_students_today - present_today
#     else:
#         # All classes
#         present_today = AttendanceRecord.objects.filter(
#             date=today,
#             present=True
#         ).count()

#         # For absent: total students who have any record today minus present
#         # (more accurate if not all students have records every day)
#         students_with_record_today = AttendanceRecord.objects.filter(date=today).values('student').distinct().count()
#         absent_today = students_with_record_today - present_today   # conservative

#         # Alternative (if you assume all students should have record):
#         # total_students = Student.objects.count()
#         # absent_today = total_students - present_today

#     # ── Per-student stats (unchanged) ──────────────────────────────
#     for s in students:
#         total_classes = ClassDay.objects.filter(class_book=s.class_book, is_active=True).count()
#         s.total_classes = total_classes

#         attended = AttendanceRecord.objects.filter(student=s, present=True).count()
#         s.attended = attended
#         s.absent = total_classes - attended
#         s.percentage = (attended / total_classes * 100) if total_classes > 0 else 0

#     # ── Percentage filter ──────────────────────────────────────────
#     if percentage_filter:
#         if percentage_filter == 'below_10':
#             students = [s for s in students if s.percentage < 10]
#         elif percentage_filter == 'below_45':
#             students = [s for s in students if s.percentage < 45]
#         elif percentage_filter == 'below_60':
#             students = [s for s in students if s.percentage < 60]
#         elif percentage_filter == '60_to_75':
#             students = [s for s in students if 60 <= s.percentage <= 75]
#         elif percentage_filter == 'above_75':
#             students = [s for s in students if s.percentage > 75]

#     return render(request, 'studentviewer/studentviewerhome.html', {
#         'classbooks': classbooks,
#         'students': students,
#         'selected_class': selected_class_id,   # string comparison in template
#         'search_query': search_query,
#         'percentage_filter': percentage_filter,
#         'present_today': present_today,
#         'absent_today': absent_today,
#         'teacher_name': teacher_name if selected_class else None,
#     })



















from django.shortcuts import render
from django.db.models import Q
from clsbook.models import ClassBook, Student, AttendanceRecord, ClassDay
from django.utils import timezone
from datetime import date


def studentviewer(request):
    classbooks = ClassBook.objects.all()
    selected_class_id = request.GET.get('classbook')
    search_query = request.GET.get('search_query', '')
    percentage_filter = request.GET.get('percentage_filter', '')
    show_mode = request.GET.get('show')  # 'absent_today' / 'present_today' / None

    today = timezone.now().date()

    # Base queryset
    students = Student.objects.all().select_related('class_book')

    selected_class = None
    teacher_name = None

    if selected_class_id:
        try:
            selected_class = ClassBook.objects.get(id=selected_class_id)
            students = students.filter(class_book=selected_class)
            teacher_name = selected_class.teacher_name   # assuming this field exists
        except ClassBook.DoesNotExist:
            selected_class_id = None

    # ── Get IDs of students present today ───────────────────────────────
    present_today_qs = AttendanceRecord.objects.filter(
        date=today,
        present=True
    ).values_list('student_id', flat=True)

    if selected_class:
        present_today_qs = present_today_qs.filter(student__class_book=selected_class)

    present_student_ids = set(present_today_qs)

    # ── Apply show mode ─────────────────────────────────────────────────
    page_title = "Student Viewer"

    if show_mode == 'absent_today':
        if selected_class:
            # Students in this class who are NOT present today
            all_in_class = Student.objects.filter(class_book=selected_class).values_list('id', flat=True)
            absent_ids = set(all_in_class) - present_student_ids
            students = students.filter(id__in=absent_ids)
        else:
            # Students with attendance record today but absent
            recorded_today = AttendanceRecord.objects.filter(date=today).values_list('student_id', flat=True).distinct()
            absent_ids = set(recorded_today) - present_student_ids
            students = students.filter(id__in=absent_ids)

        page_title = "Absent Today"

    elif show_mode == 'present_today':
        students = students.filter(id__in=present_student_ids)
        page_title = "Present Today"

    # ── Search filter ───────────────────────────────────────────────────
    if search_query:
        students = students.filter(
            Q(first_name__icontains=search_query) |
            Q(middle_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(college_regd__icontains=search_query) |
            Q(roll__icontains=search_query)
        )

    # ── Per-student statistics ──────────────────────────────────────────
    for student in students:
        total_classes = ClassDay.objects.filter(
            class_book=student.class_book,
            is_active=True
        ).count()

        attended = AttendanceRecord.objects.filter(
            student=student,
            present=True
        ).count()

        student.total_classes = total_classes
        student.attended = attended
        student.absent = total_classes - attended
        student.percentage = round((attended / total_classes * 100), 2) if total_classes > 0 else 0.0

    # ── Percentage range filter ─────────────────────────────────────────
    if percentage_filter:
        filtered = []
        for s in students:
            p = s.percentage
            if (percentage_filter == 'below_10' and p < 10) or \
               (percentage_filter == 'below_45' and p < 45) or \
               (percentage_filter == 'below_60' and p < 60) or \
               (percentage_filter == '60_to_75' and 60 <= p <= 75) or \
               (percentage_filter == 'above_75' and p > 75):
                filtered.append(s)
        students = filtered

    # ── Summary counts (always total — not affected by percentage/search) ──
    present_today_count = len(present_student_ids)

    if selected_class:
        total_students_in_scope = Student.objects.filter(class_book=selected_class).count()
        absent_today_count = total_students_in_scope - present_today_count
    else:
        recorded_today_count = AttendanceRecord.objects.filter(date=today).values('student').distinct().count()
        absent_today_count = recorded_today_count - present_today_count

    context = {
        'classbooks': classbooks,
        'students': students,
        'selected_class': selected_class_id,
        'search_query': search_query,
        'percentage_filter': percentage_filter,
        'present_today': present_today_count,
        'absent_today': absent_today_count,
        'teacher_name': teacher_name,
        'show_mode': show_mode,
        'page_title': page_title,
    }

    return render(request, 'studentviewer/studentviewerhome.html', context)
