from django import forms
from . models import Subject, StudyMaterials, Assignment, AssignmentSubmission


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'description']
        widgets = {"description": forms.Textarea(attrs={"rows": 6})}


class StudyMaterialsForm(forms.ModelForm):
    class Meta:
        model = StudyMaterials
        fields = ['subject', 'title', 'description', 'file']
        widgets = {"description": forms.Textarea(attrs={"rows": 6})}


class AssignmentForm(forms.ModelForm):

    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    class Meta:
        model = Assignment
        fields = ['subject', 'title', 'description', 'file', 'due_date']
        widgets = {"description": forms.Textarea(attrs={"rows": 6})}


class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['file', 'answer_text']
        widgets = {"answer_text": forms.Textarea(attrs={"rows": 6})}
