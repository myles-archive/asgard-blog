from django import forms
from django.utils.translation import ugettext_lazy as _

class BlogSearchForm(forms.Form):
	q = forms.CharField(label=u"Search")