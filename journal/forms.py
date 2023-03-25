from django import forms


class TokenForm(forms.Form):
    action = forms.ChoiceField(
        choices=[("REMOVE", "Remove link"), ("RENEW", "Create new link")],
        widget=forms.Select,
        required=True,
    )
