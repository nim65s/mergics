from django.contrib.auth.models import User
from django.test import TestCase

from . import models

URLS = [
    'https://www.mozilla.org/media/caldata/FrenchHolidays.ics',
    'http://cache.media.education.gouv.fr/ics/Calendrier_Scolaire_Zone_C.ics'
]


class MergICSTests(TestCase):
    def test_nothing(self):
        self.assertTrue(True)

    def test_models(self):
        user = User.objects.create_user(username='test', password='test')
        out = models.ICSOutput(user=user, name='holidays')
        out.save()

        components = 0

        for url in URLS:
            ics_input = models.ICSInput(user=user, url=url)
            ics_input.save()
            out.inputs.add(ics_input)
            components += len(list(c for c in ics_input.from_ical().walk() if c.name != 'VCALENDAR'))

        self.assertEqual(models.ICSOutput.objects.first().inputs.count(), 2)
        self.assertEqual(len(models.ICSOutput.objects.first().to_cal().walk()) - 1, components)
