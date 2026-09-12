
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

from .models import Course, Lesson, Question, Choice, Submission


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    show_change_link = True


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Submission)

admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)