from django import forms
from contratest.models import Move

class MoveForm(forms.Form):
    movename = forms.ChoiceField(required=False, widget=forms.Select, choices=Move.MOVENAME_CHOICES)
    # who = forms.ChoiceField(required=False, widget=forms.Select, choices=Move.WHO_CHOICES, initial=None)
    hand = forms.ChoiceField(required=False, widget=forms.Select, choices=Move.HAND_CHOICES, initial=None)
    # dir = forms.ChoiceField(required=False, widget=forms.Select, choices=Move.DIR_CHOICES, initial=None)
    # dist = forms.DecimalField(max_digits=3, decimal_places=2, initial=None)
    # bal = forms.NullBooleanField(initial=None)