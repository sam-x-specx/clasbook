# from django.urls import path
# from .import views

# app_name = "stdadd" # <-- appname

# urlpatterns = [
#     path("/studentadder", views.stdadd ,name='stdadder'), # <-- htmlpage(stdadder) as name send to base.html and url show like "/stdadd" on that page
#     path("/password", views.stdadd ,name='password_prompt'), # <-- htmlpage(stdadder) as name send to base.html and url show like "/stdadd" on that page
# ]



from django.urls import path
from . import views

app_name = "stdadd"

urlpatterns = [
    # Main student management page
    path('studentadder/', views.stdadd, name='stdadder'),

    # Password prompt (if still used)
    path('password/', views.password_prompt, name='password_prompt'),

    # ── API endpoints used by JavaScript ────────────────────────────────
    path('api/active-days/',    views.get_active_days,       name='get_active_days'),
    path('api/attendance-date/', views.get_attendance_by_date, name='get_attendance_by_date'),
    path('api/toggle-active-day/', views.toggle_active_day,   name='toggle_active_day'),
    path('api/class-day-number/',     views.get_class_day_number,   name='get_class_day_number'),
]
