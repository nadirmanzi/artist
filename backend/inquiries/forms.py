from django import forms

from inquiries.models import ArtworkInquiry, ContactInquiry


class ContactInquiryAdminForm(forms.ModelForm):
    """Admin form — all fields read-only except is_read."""

    class Meta:
        model = ContactInquiry
        fields = (
            "name",
            "email",
            "phone_number",
            "message",
            "is_read",
        )
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4, "readonly": True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        readonly = [
            "name",
            "email",
            "phone_number",
            "message",
        ]
        for field_name in readonly:
            if field_name in self.fields:
                self.fields[field_name].disabled = True


class ArtworkInquiryAdminForm(forms.ModelForm):
    """Admin form — all fields read-only except is_read."""

    class Meta:
        model = ArtworkInquiry
        fields = (
            "catalog",
            "name",
            "email",
            "phone_number",
            "message",
            "is_read",
        )
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4, "readonly": True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        readonly = [
            "catalog",
            "name",
            "email",
            "phone_number",
            "message",
        ]
        for field_name in readonly:
            if field_name in self.fields:
                self.fields[field_name].disabled = True
