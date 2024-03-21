from django import forms
from .models import Document, Duty


class DocumentForm(forms.ModelForm):
    duties = forms.CharField(label='Обязательства', required=False, widget=forms.Textarea)
    signing_date = forms.DateField(label='Дата подписания', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='Дата завершения', widget=forms.DateInput(attrs={'type': 'date'}))
    notes = forms.CharField(label='Примечания', required=False, widget=forms.Textarea)

    class Meta:
        model = Document
        fields = '__all__'

    def save(self, commit=True):
        document = super().save(commit=False)
        duties_text = self.cleaned_data.get('duties')
        if duties_text:
            duties_list = [duty.strip() for duty in duties_text.split('\n') if duty.strip()]
            document.save()

            document.duty_set.all().delete()

            for duty_text in duties_list:
                Duty.objects.create(title=duty_text, document=document)
        else:
            document.save()
        return document
