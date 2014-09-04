from django import forms
from contratest.models import Move, Dance, expected_values
from fields import EmptyChoiceField

def __init__(self, *args, **kwargs):
    super(CircuitForm, self).__init__(*args, **kwargs)

    for key in self.fields:
        self.fields[key].required = False

class MoveForm(forms.Form):
    # move attributes
    movename = forms.ChoiceField(required=False, widget=forms.Select, choices=Move.MOVENAME_CHOICES)
    # who = EmptyChoiceField(required=False, widget=forms.Select, choices=Move.WHO_CHOICES)
    # hand = EmptyChoiceField(required=False, widget=forms.Select, choices=Move.HAND_CHOICES)
    # dir = EmptyChoiceField(required=False, widget=forms.Select, choices=Move.DIR_CHOICES)
    # dist = forms.DecimalField(max_digits=3, decimal_places=2, initial=None)
    # bal = EmptyChoiceField(required=False, widget=forms.Select, choices=[(1, True), (0, False)])

class DanceForm(forms.Form):
    formation = forms.ChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=Dance.FORMATION_CHOICES)
    progression = forms.ChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=[("1", "single"), ("2", "double"), ("3", "triple"), ("4", "quadruple")])

class testForm(forms.Form):
    movename = EmptyChoiceField(required=False, widget=forms.Select, choices=Move.MOVENAME_CHOICES)

class individualizedForm(forms.Form):
    def __init__(self, move):

        super(individualizedForm, self).__init__()

        if len(expected_values[move])>0:
            for attr in expected_values[move]:
                if attr == "dir":
                    if move in ["circle"]:
                        self.fields[attr] = EmptyChoiceField(required=False, widget=forms.Select, choices=Move.dir_ring_choices)
                    else:
                        self.fields[attr] = EmptyChoiceField(required=False, widget=forms.Select, choices=Move.dir_set_choices)
                elif attr == "dist":
                    if move in ["circle", "star"]:
                        self.fields[attr] = EmptyChoiceField(required=False, widget=forms.Select, choices=Move.dist_whole_choices)
                    else:
                        self.fields[attr] = EmptyChoiceField(required=False, widget=forms.Select, choices=Move.dist_dec_choices)
                elif attr == "moreinfo":
                    pass
                else:
                    self.fields[attr] = EmptyChoiceField(required=False, widget=forms.Select, choices=get_choices(attr))

def get_choices(attr):
    return Move._meta.get_field_by_name(attr)[0].choices

# to-do:
# search dance attributes (formation, progression, etc.)
    # --> DO I WANT TITLE/AUTHOR/TAG FILTERS ON SEARCH PG,
    # when DataTables does this so much better than i do??
# logic about which forms/choices appear where
# make addl choices for sect: A1, A2, B1, B2, A, B
