from django import forms


class ClassBookingForm(forms.Form):
    program_id = forms.UUIDField()
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20, required=False)
