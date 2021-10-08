"""The admin page model for polls app."""
from django.contrib import admin
from .models import Choice, Question


class ChoiceInLine(admin.TabularInline):
    """Admin table of choice model."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Question admin model."""

    fieldsets = [
        (None, {"fields": ['question_text']}),
        ('Date Information', {"fields": ['pub_date', 'end_date']})
    ]
    inlines = [ChoiceInLine]
    list_display = ('question_text', 'pub_date', 'is_published',
                    'can_vote', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
