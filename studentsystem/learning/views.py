from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from .forms import AssignmentForm, AssignmentSubmissionForm, StudyMaterialsForm, SubjectForm
from .models import Assignment, AssignmentSubmission, StudyMaterials, Subject


def admin_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin_role():
            messages.error(request, 'Admin access is required.')
            return redirect('learning:subject_list')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def subject_list(request):
    subjects = Subject.objects.all().order_by('name')
    return render(request, 'learning/subject_list.html', {'subjects': subjects})


@login_required
def subject_detail(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    return render(request, 'learning/subject_detail.html', {'subject': subject})


@admin_required
def subject_create(request):
    form = SubjectForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        subject = form.save(commit=False)
        subject.created_by = request.user
        subject.save()
        messages.success(request, 'Subject created.')
        return redirect('learning:subject_list')
    return render(request, 'learning/form.html', {'form': form, 'title': 'Create Subject'})


@admin_required
def subject_update(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    form = SubjectForm(request.POST or None, instance=subject)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Subject updated.')
        return redirect('learning:subject_detail', pk=subject.pk)
    return render(request, 'learning/form.html', {'form': form, 'title': 'Edit Subject'})


@admin_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted.')
        return redirect('learning:subject_list')
    return render(request, 'confirm_delete.html', {'object': subject, 'cancel_url': 'learning:subject_list'})


@login_required
def material_list(request):
    materials = StudyMaterials.objects.select_related('subject').all()
    return render(request, 'learning/material_list.html', {'materials': materials})


@admin_required
def material_create(request):
    form = StudyMaterialsForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        material = form.save(commit=False)
        material.uploaded_by = request.user
        material.save()
        messages.success(request, 'Study material uploaded.')
        return redirect('learning:material_list')
    return render(request, 'learning/form.html', {'form': form, 'title': 'Upload Study Material'})


@admin_required
def material_update(request, pk):
    material = get_object_or_404(StudyMaterials, pk=pk)
    form = StudyMaterialsForm(request.POST or None, request.FILES or None, instance=material)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Study material updated.')
        return redirect('learning:material_list')
    return render(request, 'learning/form.html', {'form': form, 'title': 'Edit Study Material'})


@admin_required
def material_delete(request, pk):
    material = get_object_or_404(StudyMaterials, pk=pk)
    if request.method == 'POST':
        material.delete()
        messages.success(request, 'Study material deleted.')
        return redirect('learning:material_list')
    return render(request, 'confirm_delete.html', {'object': material, 'cancel_url': 'learning:material_list'})


@login_required
def assignment_list(request):
    assignments = Assignment.objects.select_related('subject').all()
    return render(request, 'learning/assignment_list.html', {'assignments': assignments})


@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    submission = None
    if request.user.role == User.Roles.STUDENT:
        submission = AssignmentSubmission.objects.filter(assignment=assignment, student=request.user).first()
    return render(request, 'learning/assignment_detail.html', {'assignment': assignment, 'submission': submission})


@admin_required
def assignment_create(request):
    form = AssignmentForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        assignment = form.save(commit=False)
        assignment.created_by = request.user
        assignment.save()
        messages.success(request, 'Assignment created.')
        return redirect('learning:assignment_list')
    return render(request, 'learning/form.html', {'form': form, 'title': 'Create Assignment'})


@admin_required
def assignment_update(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    form = AssignmentForm(request.POST or None, request.FILES or None, instance=assignment)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Assignment updated.')
        return redirect('learning:assignment_detail', pk=assignment.pk)
    return render(request, 'learning/form.html', {'form': form, 'title': 'Edit Assignment'})


@admin_required
def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Assignment deleted.')
        return redirect('learning:assignment_list')
    return render(request, 'confirm_delete.html', {'object': assignment, 'cancel_url': 'learning:assignment_list'})


@login_required
def assignment_submit(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    submission = AssignmentSubmission.objects.filter(assignment=assignment, student=request.user).first()
    form = AssignmentSubmissionForm(request.POST or None, request.FILES or None, instance=submission)
    if request.method == 'POST' and form.is_valid():
        item = form.save(commit=False)
        item.assignment = assignment
        item.student = request.user
        item.save()
        messages.success(request, 'Assignment submitted.')
        return redirect('learning:assignment_detail', pk=assignment.pk)
    return render(request, 'learning/form.html', {'form': form, 'title': 'Submit Assignment'})
