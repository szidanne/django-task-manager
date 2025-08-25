from django import forms
from .models import Task, Status

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "status", "due_date"]
        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "e.g., Finish literature review",
                "class": "input input-bordered w-full",
                "autocomplete": "off",
            }),
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Optional notes, links, acceptance criteria…",
                "class": "textarea textarea-bordered w-full",
            }),
            "status": forms.Select(choices=Status.choices, attrs={
                "class": "select select-bordered w-full",
            }),
            # HTML5 date picker
            "due_date": forms.DateInput(attrs={
                "type": "date",                  # <— key line
                "class": "input input-bordered w-full",
            }),
        }

    # Optional: prevent past dates
    def clean_due_date(self):
        from datetime import date
        d = self.cleaned_data["due_date"]
        # allow today; reject strictly past
        if d < date.today():
            raise forms.ValidationError("Due date cannot be in the past.")
        return d
