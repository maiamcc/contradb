from django import forms
from contratest.models import Move
from fields import EmptyChoiceField

def __init__(self, *args, **kwargs):
    super(CircuitForm, self).__init__(*args, **kwargs)

    for key in self.fields:
        self.fields[key].required = False

class MoveForm(forms.Form):
    movename = forms.ChoiceField(required=False, widget=forms.Select, choices=Move.MOVENAME_CHOICES)
    who = EmptyChoiceField(required=False, widget=forms.Select, choices=Move.WHO_CHOICES)
    hand = EmptyChoiceField(required=False, widget=forms.Select, choices=Move.HAND_CHOICES)
    dir = EmptyChoiceField(required=False, widget=forms.Select, choices=Move.DIR_CHOICES)
    dist = forms.DecimalField(max_digits=3, decimal_places=2, initial=None)
    bal = EmptyChoiceField(required=False, widget=forms.Select, choices=[(1, True), (0, False)])

# to-do:
# logic about which forms/choices appear where
# make addl choices for sect: A1, A2, B1, B2, A, B