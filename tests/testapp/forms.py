# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from django_select2.forms import (
    HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
    ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
    Select2Widget
)
from tests.testapp import models
from tests.testapp.models import Album


class TitleSearchFieldMixin(object):
    search_fields = [
        'title__icontains',
        'pk__startswith'
    ]


class TitleModelSelect2Widget(TitleSearchFieldMixin, ModelSelect2Widget):
    pass


class TitleModelSelect2MultipleWidget(TitleSearchFieldMixin, ModelSelect2MultipleWidget):
    pass


class GenreSelect2TagWidget(TitleSearchFieldMixin, ModelSelect2TagWidget):
    model = models.Genre

    def create_value(self, value):
        self.get_queryset().create(title=value)


class AlbumSelect2WidgetForm(forms.ModelForm):
    class Meta:
        model = models.Album
        fields = (
            'artist',
            'primary_genre',
        )
        widgets = {
            'artist': Select2Widget,
            'primary_genre': Select2Widget,

        }


class AlbumSelect2MultipleWidgetForm(forms.ModelForm):
    class Meta:
        model = models.Album
        fields = (
            'genres',
            'featured_artists',
        )
        widgets = {
            'genres': Select2MultipleWidget,
            'featured_artists': Select2MultipleWidget,
        }


class AlbumModelSelect2WidgetForm(forms.ModelForm):
    class Meta:
        model = models.Album
        fields = (
            'artist',
            'primary_genre',
        )
        widgets = {
            'artist': ModelSelect2Widget(
                model=models.Artist,
                search_fields=['title__icontains']
            ),
            'primary_genre': ModelSelect2Widget(
                model=models.Genre,
                search_fields=['title__icontains']
            ),
        }


class AlbumModelSelect2MultipleWidgetRequiredForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = (
            'genres',
            'featured_artists',
        )
        widgets = {
            'genres': TitleModelSelect2MultipleWidget,
            'featured_artists': TitleModelSelect2MultipleWidget,
        }


class ArtistModelSelect2MultipleWidgetForm(forms.Form):
    title = forms.CharField(max_length=50)
    genres = forms.ModelMultipleChoiceField(widget=ModelSelect2MultipleWidget(
        queryset=models.Genre.objects.all(),
        search_fields=['title__icontains'],
    ), queryset=models.Genre.objects.all(), required=False)

NUMBER_CHOICES = [
    (1, 'One'),
    (2, 'Two'),
    (3, 'Three'),
    (4, 'Four'),
]


class Select2WidgetForm(forms.Form):
    number = forms.ChoiceField(widget=Select2Widget, choices=NUMBER_CHOICES, required=False)


class HeavySelect2WidgetForm(forms.Form):
    artist = forms.ChoiceField(
        widget=HeavySelect2Widget(data_view='heavy_data_1', choices=NUMBER_CHOICES)
    )
    primary_genre = forms.ChoiceField(
        widget=HeavySelect2Widget(data_view='heavy_data_2', choices=NUMBER_CHOICES),
        required=False
    )


class HeavySelect2MultipleWidgetForm(forms.Form):
    genres = forms.MultipleChoiceField(
        widget=HeavySelect2MultipleWidget(data_view='heavy_data_1', choices=NUMBER_CHOICES)
    )
    featured_artists = forms.MultipleChoiceField(
        widget=HeavySelect2MultipleWidget(data_view='heavy_data_2', choices=NUMBER_CHOICES),
        required=False
    )


class ModelSelect2TagWidgetForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['genres']
        widgets = {
            'genres': GenreSelect2TagWidget
        }
