from django.shortcuts import redirect


def assignment_list(request):
    return redirect('learning:assignment_list')
