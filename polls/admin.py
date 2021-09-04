from django.contrib import admin
from .models import Choice, Question


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ['question_text']}),
        ('Date Information', {"fields": ['pub_date']})
    ]

    inlines = [ChoiceInLine]


admin.site.register(Question, QuestionAdmin)
