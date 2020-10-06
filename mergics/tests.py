from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from . import models

URLS = [
    'https://www.mozilla.org/media/caldata/FrenchHolidays.ics',
    'http://cache.media.education.gouv.fr/ics/Calendrier_Scolaire_Zone_C.ics'
]


class MergICSTests(TestCase):
    def test_nothing(self):
        self.assertTrue(True)

    def test_models(self):
        # Create user & output
        user = User.objects.create_user(username='testm', password='testm')
        out = models.ICSOutput(user=user, name='holidays')
        out.save()

        components = 0

        # Add inputs
        for url in URLS:
            ics_input = models.ICSInput(user=user, url=url)
            ics_input.save()
            out.inputs.add(ics_input)
            components += len(list(c for c in ics_input.from_ical().walk() if c.name != 'VCALENDAR'))

        # Check the inputs have been added
        self.assertEqual(models.ICSOutput.objects.first().inputs.count(), 2)
        # Check the output has the right number of components (ignore the "vcalendar" component)
        self.assertEqual(len(models.ICSOutput.objects.first().to_cal().walk()) - 1, components)

    def test_views(self):
        User.objects.create_user(username='testv', password='testv')

        # ##########
        # Input ICS

        # Check user gets redirected to login page with a "next" parameter
        r = self.client.get(reverse('mergics:icsinputs'))
        self.assertEqual(r.status_code, 302)
        self.assertIn('accounts/login', r.url)
        self.assertIn('next=', r.url)

        # After login, the list should return 200 OK
        self.client.login(username='testv', password='testv')
        r = self.client.get(reverse('mergics:icsinputs'))
        self.assertEqual(r.status_code, 200)

        # It shouldn't contain any URL yet
        self.assertNotIn(URLS[0], r.content.decode())

        # Check user can add ICSInput objects
        count = models.ICSInput.objects.count()
        self.client.post(reverse('mergics:icsinput-add'), {'url': URLS[0]})
        self.assertEqual(models.ICSInput.objects.count(), count + 1)

        # The added url should appear on the list
        r = self.client.get(reverse('mergics:icsinputs'))
        self.assertIn(URLS[0], r.content.decode())

        # ##########
        # Output ICS

        # Check user can add ICSOutput objects
        count = models.ICSOutput.objects.count()
        self.client.post(reverse('mergics:icsoutput-add'), {'name': 'Toto', 'inputs': [1]})
        self.assertEqual(models.ICSOutput.objects.count(), count + 1)

        # The slug of the added object should appear on the list
        r = self.client.get(reverse('mergics:icsoutputs'))
        self.assertIn('toto', r.content.decode())

        # And the url on the detail
        r = self.client.get(reverse('mergics:icsoutput', kwargs={'slug': 'toto'}))
        self.assertIn(URLS[0], r.content.decode())

        # Check the holiday are available in the generated ICS
        r = self.client.get(reverse('mergics:ics', kwargs={'username': 'testv', 'slug': 'toto'}))
        self.assertIn('SUMMARY:Ascension', r.content.decode())

        # ############
        # Second User

        User.objects.create_user(username='testw', password='testw')
        self.client.login(username='testw', password='testw')

        # Check the input of the first user is not visible
        r = self.client.get(reverse('mergics:icsinputs'))
        self.assertNotIn(URLS[0], r.content.decode())

        r = self.client.get(reverse('mergics:icsoutput-add'))
        self.assertNotIn(URLS[0], r.content.decode())
