from django import forms
from web import models
from django_select2.forms import Select2MultipleWidget, HeavySelect2Widget


NUMBER_CHOICES = [
    (1, 'One'),
    (2, 'Two'),
    (3, 'Three'),
    (4, 'Four'),
]


class NoValidationChoiceField(forms.ChoiceField):

    def validate(self, value):
        pass


class NoValidationMultipleChoiceField(forms.MultipleChoiceField):

    def validate(self, values):
        pass

class MessageForm(forms.ModelForm):

    def __init__(self, destination_choices, coursesections_choices, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['destination'].choices = destination_choices
        self.fields['coursesections'].choices = coursesections_choices

    destination = forms.ChoiceField(choices=[], label='Enviar Para:', required=True)
    #title = forms.CharField(required=True, label='Titulo', max_length=50)
    message = forms.CharField(required=True, label='Mensagem', max_length=300, widget=forms.Textarea)
    coursesections = forms.ChoiceField(choices=[], label='Turmas:', required=True)
    class Meta:
        model = models.WallMessages
        fields = ('message',)
