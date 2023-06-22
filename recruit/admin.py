from django.contrib import admin
from django.utils.html import format_html
from .models import Recruit, Event, Task, Position


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0


class EventRecruitsInline(admin.TabularInline):
    model = Event.students.through
    extra = 0


class EventPositionsInline(admin.TabularInline):
    model = Event.positions.through
    extra = 0


class PositionRecruitInline(admin.TabularInline):
    model = Position.recruits.through
    extra = 0


class StudentAdmin(admin.ModelAdmin):
    inlines = [
        PositionRecruitInline,
        EventRecruitsInline,
        TaskInline
    ]
    exclude = (
        "email_sent",
        "received_reply",
        "assessment_scheduled",
        "assessment_graded",
        "schedule_interview",
    )


class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'form_url']
    inlines = [
        EventPositionsInline,
        EventRecruitsInline,
    ]
    exclude = ("positions", "students",)


class PositionAdmin(admin.ModelAdmin):
    inlines = [
        PositionRecruitInline
    ]
    exclude = ("recruits",)


# Register your models here.
admin.site.register(Recruit, StudentAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Position, PositionAdmin)
