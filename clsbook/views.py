# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.http import Http404
# from .models import ClassBook
# from .forms import ClassBookForm


# @login_required
# def clsbook(request):
#     """Display only classbooks created by the logged-in user"""
#     # Filter by current user
#     classbooks = ClassBook.objects.filter(created_by=request.user)
    
#     # Get unique counts from user's classbooks only
#     unique_classes = list(set(classbooks.values_list('class_name', flat=True)))
#     unique_teachers = list(set(classbooks.values_list('teacher_name', flat=True)))
#     unique_sections = list(set(classbooks.values_list('section', flat=True)))
    
#     context = {
#         'classbooks': classbooks,
#         'unique_classes': sorted(unique_classes),  # Sorted list for displaying as tags
#         'unique_classes_count': len(unique_classes),
#         'unique_teachers_count': len(unique_teachers),
#         'unique_sections_count': len(unique_sections),
#     }
    
#     return render(request, 'clsbook/clsbookhome.html', context)


# @login_required
# def create_classbook(request):
#     """Create a new classbook for the logged-in user"""
#     if request.method == 'POST':
#         form = ClassBookForm(request.POST)

#         if form.is_valid():
#             # Pass the current user to save method
#             classbook = form.save(commit=True, user=request.user)
#             messages.success(
#                 request,
#                 f'Class Book "{classbook}" created successfully!'
#             )
#             return redirect('clsbook:clsbook')
#         else:
#             messages.error(
#                 request,
#                 'Please correct the errors below.'
#             )
#     else:
#         # Pre-fill form with user's information
#         form = ClassBookForm(initial={
#             'teacher_email': request.user.email,
#             'teacher_name': request.user.get_full_name() or request.user.username
#         })

#     return render(
#         request,
#         'clsbook/create_classbook.html',
#         {'form': form}
#     )


# @login_required
# def delete_classbook(request, pk):
#     """Delete a classbook (only if user owns it)"""
#     # Ensure user can only delete their own classbooks
#     classbook = get_object_or_404(ClassBook, pk=pk, created_by=request.user)

#     if request.method == 'POST':
#         classbook_name = str(classbook)
#         classbook.delete()
#         messages.success(
#             request,
#             f'Class Book "{classbook_name}" deleted successfully!'
#         )
#         return redirect('clsbook:clsbook')

#     return render(
#         request,
#         'clsbook/delete_confirm.html',
#         {'classbook': classbook}
#     )


# @login_required
# def reset_password(request, pk):
#     """Reset password for a classbook (only if user owns it)"""
#     try:
#         # Ensure user can only reset password for their own classbooks
#         classbook = ClassBook.objects.get(pk=pk, created_by=request.user)
#     except ClassBook.DoesNotExist:
#         messages.error(request, 'Class Book not found or you do not have permission to access it.')
#         return redirect('clsbook:clsbook')

#     if request.method == 'POST':
#         new_password = request.POST.get('new_password')
#         confirm_password = request.POST.get('confirm_password')
        
#         if new_password and new_password == confirm_password:
#             classbook.set_password(new_password)
#             classbook.save()
#             messages.success(
#                 request, 
#                 f'Password reset successfully for "{classbook.class_name} - {classbook.section}"!'
#             )
#             return redirect('clsbook:clsbook')
#         else:
#             messages.error(request, 'Passwords do not match or are empty.')

#     return render(request, 'clsbook/reset_password.html', {'classbook': classbook})





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import ClassBook
from .forms import ClassBookForm


# @login_required
# def clsbook(request):
#     """Display all classbooks but allow management of only user's own"""
#     # Get ALL classbooks for viewing
#     all_classbooks = ClassBook.objects.all()
    
#     # Get user's own classbooks for stats
#     user_classbooks = all_classbooks.filter(created_by=request.user)
    
#     # Stats from user's classbooks only
#     unique_classes = list(set(user_classbooks.values_list('class_name', flat=True)))
#     unique_teachers = list(set(user_classbooks.values_list('teacher_name', flat=True)))
#     unique_sections = list(set(user_classbooks.values_list('section', flat=True)))
    
#     context = {
#         'classbooks': all_classbooks,  # Show ALL classbooks in table
#         'user_classbooks_count': user_classbooks.count(),  # User's own count
#         'unique_classes': sorted(unique_classes),
#         'unique_classes_count': len(unique_classes),
#         'unique_teachers_count': len(unique_teachers),
#         'unique_sections_count': len(unique_sections),
#         'total_classbooks_count': all_classbooks.count(),  # Total in system
#     }
    
#     return render(request, 'clsbook/clsbookhome.html', context)



@login_required
def clsbook(request):
    """Display all classbooks + global stats for everyone"""
    # Get ALL classbooks for viewing (same as before)
    all_classbooks = ClassBook.objects.all()
    
    # User's own classbooks (still useful for some UI elements or personal stats if needed)
    user_classbooks = all_classbooks.filter(created_by=request.user)
    
    # === GLOBAL STATS (what you want now) ===
    # All unique class names across the system
    unique_classes = list(set(all_classbooks.values_list('class_name', flat=True)))
    
    # All unique teacher names across the system
    unique_teachers = list(set(all_classbooks.values_list('teacher_name', flat=True)))
    
    # All unique sections across the system
    unique_sections = list(set(all_classbooks.values_list('section', flat=True)))
    
    context = {
        'classbooks': all_classbooks,               # Show ALL classbooks in table
        'user_classbooks_count': user_classbooks.count(),  # Optional: keep user's own count if you want to display it somewhere
        
        # Global / total counts
        'unique_classes': sorted(unique_classes),
        'unique_classes_count': len(unique_classes),          # ← Total Classes
        'unique_teachers_count': len(unique_teachers),        # ← Active Teachers (total unique names)
        'unique_sections_count': len(unique_sections),        # ← Total Sections
        
        'total_classbooks_count': all_classbooks.count(),     # Total number of classbooks created
    }
    
    return render(request, 'clsbook/clsbookhome.html', context)





@login_required
def create_classbook(request):
    """Create a new classbook for the logged-in user"""
    if request.method == 'POST':
        form = ClassBookForm(request.POST)

        if form.is_valid():
            # Pass the current user to save method
            classbook = form.save(commit=True, user=request.user)
            messages.success(
                request,
                f'Class Book "{classbook}" created successfully!'
            )
            return redirect('clsbook:clsbook')
        else:
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        # Pre-fill form with user's information
        form = ClassBookForm(initial={
            'teacher_email': request.user.email,
            'teacher_name': request.user.get_full_name() or request.user.username
        })

    return render(
        request,
        'clsbook/create_classbook.html',
        {'form': form}
    )


@login_required
def delete_classbook(request, pk):
    """Delete a classbook (only if user owns it)"""
    # Ensure user can only delete their own classbooks
    classbook = get_object_or_404(ClassBook, pk=pk, created_by=request.user)

    if request.method == 'POST':
        classbook_name = str(classbook)
        classbook.delete()
        messages.success(
            request,
            f'Class Book "{classbook_name}" deleted successfully!'
        )
        return redirect('clsbook:clsbook')

    return render(
        request,
        'clsbook/delete_confirm.html',
        {'classbook': classbook}
    )


@login_required
def reset_password(request, pk):
    """Reset password for a classbook (only if user owns it)"""
    try:
        # Ensure user can only reset password for their own classbooks
        classbook = ClassBook.objects.get(pk=pk, created_by=request.user)
    except ClassBook.DoesNotExist:
        messages.error(request, 'Class Book not found or you do not have permission to access it.')
        return redirect('clsbook:clsbook')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password and new_password == confirm_password:
            classbook.set_password(new_password)
            classbook.save()
            messages.success(
                request, 
                f'Password reset successfully for "{classbook.class_name} - {classbook.section}"!'
            )
            return redirect('clsbook:clsbook')
        else:
            messages.error(request, 'Passwords do not match or are empty.')

    return render(request, 'clsbook/reset_password.html', {'classbook': classbook})
