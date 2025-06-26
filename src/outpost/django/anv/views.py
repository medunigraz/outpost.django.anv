import logging

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Field,
    Fieldset,
    Layout,
)
from django.http import (
    Http404,
    HttpResponseRedirect,
)
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy as reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.generic import UpdateView
from outpost.django.base.layout import IconButton

from . import models

logger = logging.getLogger(__name__)


class StationView(UpdateView):
    model = models.Station
    fields = (
        "system",
        "number",
        "room",
    )

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        url = self.object.url()
        if url:
            return HttpResponseRedirect(url)
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj, created = queryset.get_or_create(pk=pk)
        if created:
            logger.info(f"Created new station {obj}")
        return obj

    def get_success_url(self):
        return self.object.url()

    def get_context_data(self, **kwargs):
        helper = FormHelper()
        helper.layout = Layout(
            Field("system"),
            Field("number"),
            Field("room"),
            FormActions(
                IconButton(
                    "fa fa-arrow-circle-right",
                    _("Save changes"),
                    type="submit",
                    css_class="btn-success btn-block",
                ),
            ),
        )
        kwargs["helper"] = helper
        return super().get_context_data(**kwargs)
