from django import forms

class EmptyChoiceField(forms.ChoiceField):
    '''Subclass that adds an empty choice to the top of any dropdown choice menu.'''
    def __init__(self, choices=(), empty_label="---", required=True, widget=None, label=None,
                 initial=None, help_text=None, *args, **kwargs):

        # prepend an empty label if it exists (and field is not required!)
        if not required and empty_label is not None:
            choices = tuple([(u'', empty_label)] + list(choices))

        super(EmptyChoiceField, self).__init__(choices=choices, required=required, widget=widget, label=label,
                                        initial=initial, help_text=help_text, *args, **kwargs)

# SRC: https://gist.github.com/davidbgk/651080