from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from config.utils import get_token
from django.contrib.auth.hashers import (
    check_password
)

from users.models import User
from wordgame.models import Room


class MakeRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('title', 'is_hide', 'mode', 'how_to_win')

    def save(self, commit=False):
        room = super(MakeRoomForm, self).save(commit=False)

        if commit:
            room.save()

        return room
