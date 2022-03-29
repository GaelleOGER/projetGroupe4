from django import forms

from .models import Answer, Question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['body']

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['body'] = forms.CharField(max_length=1500, required=True,
                                              widget=forms.Textarea(attrs={'class': 'form-control'}))


