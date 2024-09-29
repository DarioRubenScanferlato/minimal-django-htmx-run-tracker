from django.test import TestCase
from django.urls import reverse
from datetime import date
from .models import Run

class RunModelTests(TestCase):
    def test_run_creation(self):
        run = Run.objects.create(
            date=date(2023, 4, 15),
            distance=5.0,
            time=1800,  # 30 minutes in seconds
            note="Test run"
        )
        self.assertEqual(run.date, date(2023, 4, 15))
        self.assertEqual(run.distance, 5.0)
        self.assertEqual(run.time, 1800)
        self.assertEqual(run.note, "Test run")
        self.assertAlmostEqual(run.average_pace, 6.0, places=2)

    def test_formatted_average_pace(self):
        run = Run.objects.create(
            date=date(2023, 4, 15),
            distance=5.0,
            time=1500,  # 25 minutes in seconds
        )
        self.assertEqual(run.formatted_average_pace, "05m 00s")

    def test_formatted_time(self):
        run = Run.objects.create(
            date=date(2023, 4, 15),
            distance=10.0,
            time=3600,  # 1 hour in seconds
        )
        self.assertEqual(run.formatted_time, "01h 00m 00s")

    def test_str_representation(self):
        run = Run.objects.create(
            date=date(2023, 4, 15),
            distance=5.0,
            time=1800,  # 30 minutes in seconds
        )
        expected_str = "Run on 2023-04-15 - 5.0km in 30m 00s (Pace: 06m 00s/km)"
        self.assertEqual(str(run), expected_str)

class RunViewTests(TestCase):
    def setUp(self):
        self.run = Run.objects.create(
            date=date(2023, 4, 15),
            distance=5.0,
            time=1800,  # 30 minutes in seconds
            note="Test run"
        )

    def test_run_list_view(self):
        response = self.client.get(reverse('run_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "April 15, 2023")
        self.assertContains(response, "5.0")

