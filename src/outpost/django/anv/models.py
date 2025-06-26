from django.contrib.gis.db import models
from django.utils.translation import gettext as _
from outpost.django.base.utils import Uuid4Upload


class System(models.Model):
    """
    A system that can serve registration stations.
    """

    name = models.CharField(
        max_length=256,
        verbose_name=_("Name"),
        help_text=_("The name under which this URL should be listed"),
    )
    logo = models.FileField(
        upload_to=Uuid4Upload,
        verbose_name=_("Logo"),
        help_text=_("A SVG file that is used as the logo for this system"),
    )
    url = models.URLField(
        verbose_name=_("URL"),
        help_text=_(
            "The URL template for this system, use {station.number} and {station.room} as placeholders"
        ),
    )

    class Meta:
        ordering = ("name",)
        verbose_name = _("System")
        verbose_name_plural = _("Systems")

    def __str__(self):
        return str(self.name)


class Station(models.Model):
    """
    A station used for registering attendants.
    """

    id = models.CharField(max_length=12, primary_key=True)
    system = models.ForeignKey(
        System,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("System"),
        help_text=_("The system that this station is currently assigned to"),
    )
    number = models.PositiveSmallIntegerField(
        null=True,
        verbose_name=_("Number"),
        help_text=_("The number for this station, positive integers only"),
    )
    room = models.CharField(
        max_length=4,
        null=True,
        verbose_name=_("Room"),
        help_text=_("The room identification where this station is located"),
    )

    class Meta:
        ordering = ("system", "number", "room")
        verbose_name = _("Station")
        verbose_name_plural = _("Stations")

    def __str__(self):
        return f"{self.number}: {self.room}"

    def url(self):
        if all((self.system, self.number, self.room)):
            return self.system.url.format(station=self)
