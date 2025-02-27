from django.shortcuts import render, redirect
from datetime import date
from .forms import CandidateCheckinForm
from .models import Recruit, Task, Event, Position
from django.http import HttpResponse, HttpResponseRedirect


def checkin(request, event_name):
    context = {}
    event = None

    # Get the linked event from the URL
    if event_name is not None:
        event = Event.objects.filter(name=event_name).first()
        if event is None:
            # TODO: Handle invalid event gracefully
            return HttpResponse("Invalid event")

    # create object of form
    form = CandidateCheckinForm(event=event, data=request.POST or None, files=request.FILES or None)
    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        name = request.POST.get("name")
        email = request.POST.get("email")
        (student, student_created) = Recruit.objects.get_or_create(email=email)
        position_id = request.POST.get("desired_position")

        student.name = name
        student.save()

        position = Position.objects.filter(id=position_id).first()
        if position is not None:
            position.recruits.add(student)
            position.save()

        # Add student to the event if there is an event with the name in the URL
        if event is not None:
            event.students.add(student)
            event.save()
        
        if student_created:
            tasks = [
                "Initial Email",
                "Resume",
                "Schedule Assessment",
                "Assessment Completed",
                "Assessment Feedback",
                "Schedule Interview",
                "Interview Completed",
                "Interview Feedback"
            ]

            for task in tasks:
                t = Task.objects.create(
                    name=task,
                    status=Task.INCOMPLETE,
                    student=student,
                    start_date=date.today(),
                    update_date=date.today(),
                )
                t.save()
        
            return HttpResponseRedirect(request.path_info)

    context['form'] = form
    return render(request, "recruit/checkin.html", context)
