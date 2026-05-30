from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from learning.models import Assignment, AssignmentSubmission, StudyMaterials, Subject

from .forms import (
    LoginForm,
    StudentCreateForm,
    StudentProfileForm,
    StudentUserUpdateForm,
    UserOnboardingForm,
    UserProfileUpdateForm,
)
from .models import StudentProfile, User


def home(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    return render(request, 'accounts/home.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('accounts:dashboard')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def dashboard_redirect(request):
    if request.user.is_admin_role():
        return redirect('accounts:admin_dashboard')
    if request.user.role == User.Roles.STUDENT:
        return redirect('accounts:student_dashboard')
    return render(request, 'accounts/dashboard.html')


@login_required
def admin_dashboard(request):
    if not request.user.is_admin_role():
        return redirect('accounts:student_dashboard')
    context = {
        'student_count': User.objects.filter(role=User.Roles.STUDENT).count(),
        'subject_count': Subject.objects.count(),
        'material_count': StudyMaterials.objects.count(),
        'assignment_count': Assignment.objects.count(),
        'recent_students': User.objects.filter(role=User.Roles.STUDENT).order_by('-created_at')[:5],
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
def student_dashboard(request):
    profile = getattr(request.user, 'student_profile', None)
    submissions = AssignmentSubmission.objects.filter(student=request.user)
    context = {
        'profile': profile,
        'subject_count': Subject.objects.count(),
        'material_count': StudyMaterials.objects.count(),
        'assignment_count': Assignment.objects.count(),
        'submission_count': submissions.count(),
        'recent_assignments': Assignment.objects.order_by('-created_at')[:5],
    }
    return render(request, 'accounts/student_dashboard.html', context)


def admin_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin_role():
            messages.error(request, 'Admin access is required.')
            return redirect('accounts:student_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def student_list(request):
    students = User.objects.filter(
        role=User.Roles.STUDENT).select_related('student_profile')
    return render(request, 'accounts/student_list.html', {'students': students})


@admin_required
def user_list(request):
    users = User.objects.all().order_by('role', 'username')
    return render(request, 'accounts/user_list.html', {'users': users})


@admin_required
def user_create(request):
    form = UserOnboardingForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        messages.success(request, f'{user.get_full_name() or user.username} was onboarded successfully.')
        return redirect('accounts:user_list')
    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Onboard User'})


@admin_required
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = UserProfileUpdateForm(request.POST or None, request.FILES or None, instance=user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'User details updated.')
        return redirect('accounts:user_list')
    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Edit User'})


@admin_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted.')
        return redirect('accounts:user_list')
    return render(request, 'confirm_delete.html', {'object': user, 'cancel_url': 'accounts:user_list'})


@admin_required
def student_create(request):
    form = StudentCreateForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Student account created successfully.')
        return redirect('accounts:student_list')
    return render(request, 'accounts/student_form.html', {'form': form, 'title': 'Create Student'})


@admin_required
def student_update(request, pk):
    student = get_object_or_404(User, pk=pk, role=User.Roles.STUDENT)
    profile, _ = StudentProfile.objects.get_or_create(
        user=student,
        defaults={'roll_number': f'ROLL-{student.pk}',
                  'course': 'Not assigned', 'semester': 1},
    )
    user_form = StudentUserUpdateForm(
        request.POST or None, request.FILES or None, instance=student)
    profile_form = StudentProfileForm(request.POST or None, instance=profile)
    if request.method == 'POST' and user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        messages.success(request, 'Student details updated.')
        return redirect('accounts:student_list')
    return render(
        request,
        'accounts/student_edit.html',
        {'user_form': user_form, 'profile_form': profile_form, 'student': student},
    )


@admin_required
def student_delete(request, pk):
    student = get_object_or_404(User, pk=pk, role=User.Roles.STUDENT)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student account deleted.')
        return redirect('accounts:student_list')
    return render(request, 'confirm_delete.html', {'object': student, 'cancel_url': 'accounts:student_list'})

# Create your views here.
