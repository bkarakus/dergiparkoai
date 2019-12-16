# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models import Q

from .models import BatchImport, Makale


class BatchImportAddForm(forms.ModelForm):
    class Meta:
        model = BatchImport
        fields = ('dergi',)


class BatchImportForm(forms.ModelForm):
    class Meta:
        model = BatchImport
        exclude = ('olusturma_tarihi', )

    makaleler = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Makale.objects.filter(batchimport=None),
        widget=FilteredSelectMultiple("Makaleler", is_stacked=False)
    )

    def __init__(self, *args, **kwargs):
        super(BatchImportForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['makaleler'].initial = self.instance.makale_set.all()
            self.fields['makaleler'].queryset = Makale.objects.filter(
                Q(dergi=self.instance.dergi),
                Q(batchimport=None) | Q(batchimport=self.instance)
            )
            print self.fields['makaleler'].queryset.count()

    def save(self, *args, **kwargs):
        instance = super(BatchImportForm, self).save(commit=False)
        instance.makaleler = None
        instance.save()
        self.fields['makaleler'].initial.update(batchimport=None)
        self.cleaned_data['makaleler'].update(batchimport=instance)
        return instance
