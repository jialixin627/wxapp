from django import forms
from django.forms import inlineformset_factory
from voting.apps.vote.models import Subject, Choice

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('question', 'subtitle', 'deadline')


class ChioceForm(forms.ModelForm):

    class Meta:
        model = Choice
        fields = ('choice_text',)

ChioceFormSet = inlineformset_factory(
    Subject, Choice,
    form=ChioceForm,
    min_num=2, validate_min=False,
    can_delete=True, extra=0)


class VoteForm(forms.Form):
    choice = forms.TypedChoiceField(choices=[], required=False, widget=forms.RadioSelect)

    def __init__(self, subject, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['choice'].choices = [(choice[0], choice[1]) for choice in subject.choice_set.all().values_list('id', 'choice_text')]
