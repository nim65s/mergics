from django.conf import settings
from django.db import models

import requests
from autoslug import AutoSlugField  # type: ignore
from icalendar import Calendar
from ndh.models import Links


class ICSInput(Links, models.Model):
    absolute_url_detail = False
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    url = models.URLField()

    class Meta:
        unique_together = ["user", "url"]

    def __str__(self) -> str:
        """Show the url of this input."""
        return self.url

    def from_ical(self) -> Calendar:
        """Downloads and parse url."""
        content = requests.get(self.url).content.decode()
        return Calendar.from_ical(content)


class ICSOutput(Links, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from="name")
    inputs = models.ManyToManyField(ICSInput)
    filtre = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ["user", "slug"]

    def __str__(self) -> str:
        """Get the name of the instance."""
        return self.name

    def to_cal(self) -> Calendar:
        """Create a Calendar merging the inputs."""
        cal = Calendar()
        cal.add(
            "prodid",
            f"-//{self.user} - {self.name}//{self.user.username}-{self.slug}.mergics//",
        )
        cal.add("version", "2.0")
        for calendar in self.inputs.all():
            for component in calendar.from_ical().walk():
                if component.name != "VCALENDAR" and (
                    self.filtre == ""
                    or "SUMMARY" not in component
                    or self.filtre in component["SUMMARY"].to_ical().decode()
                ):
                    cal.add_component(component)
        return cal

    def to_ical(self) -> str:
        """Format the generated Calendar as a string."""
        return self.to_cal().to_ical()
