from django.db import models
from django.utils.html import format_html


class Recruit(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=50, unique=True)
    notes = models.CharField(max_length=200, blank=True, null=True)
    email_sent = models.BooleanField(default=False)
    received_reply = models.BooleanField(default=False)
    assessment_scheduled = models.BooleanField(default=False)
    assessment_graded = models.BooleanField(default=False)
    schedule_interview = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def desired_positions(self):
        position_names = []
        for position in Position.objects.filter(recruits=self.id):
            position_names.append(position.name)
        return position_names

    def attended_events(self):
        attended = []
        for event in Event.objects.filter(students=self.id):
            attended.append(event.name)
        return attended

    def incomplete_tasks(self):
        tasks = []
        for task in Task.objects.filter(student=self.id):
            if task.status is not Task.COMPLETED:
                tasks.append(task.name)
        return tasks


class Position(models.Model):
    name = models.CharField(max_length=48)
    url = models.CharField(max_length=200)
    available = models.BooleanField(default=True)
    recruits = models.ManyToManyField(Recruit, null=True, blank=True)

    def __str__(self):
        return self.name

    def recruit_applicants(self):
        applicants = []
        for recruit in self.recruits.all():
            applicants.append(recruit.name)
        return applicants

    def admin_url(self):
        return format_html("<a href='/admin/recruit/position/{}/change'>{}</a>", self.id, self.name)


class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    notes = models.CharField(max_length=200, blank=True, null=True)
    students = models.ManyToManyField(Recruit, null=True, blank=True)
    positions = models.ManyToManyField(Position, null=True, blank=True)

    def __str__(self):
        return self.name

    def available_positions(self):
        available = []
        for position in self.positions.all():
            available.append(position.name)
        return available

    def form_url(self):
        return format_html(
            "<a href='/recruit/checkin/{}' target='_blank'>Open Check-In</a>",
            self.name.replace(' ', '%20')
        )


class Task(models.Model):
    INCOMPLETE = 'INCOMPLETE'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    STATUS_CHOICES = [
        (INCOMPLETE, 'Incomplete'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed')
    ]
    name = models.CharField(max_length=200)
    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default=INCOMPLETE
    )
    start_date = models.DateField()
    update_date = models.DateField()
    student = models.ForeignKey(Recruit, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def is_completed(self):
        return self.status == self.COMPLETED
