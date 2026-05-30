from django.contrib import admin

from . models import Subject, StudyMaterials, Assignment, AssignmentSubmission


admin.site.register(Subject)
admin.site.register(StudyMaterials)
admin.site.register(Assignment)
admin.site.register(AssignmentSubmission)
