from django import forms


class MessageForm(forms.Form):
    message = forms.CharField()


class MessageUpdateForm(forms.Form):
    message = forms.Textarea()