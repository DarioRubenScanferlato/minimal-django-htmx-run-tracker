from django.db import models
from datetime import timedelta

# Create your models here.
class Run(models.Model):
    date = models.DateField()
    distance = models.FloatField(help_text="Distance in kilometers")
    time = models.IntegerField(help_text="Time taken for the run in seconds")
    note = models.TextField(blank=True, null=True)
    
    average_pace = models.FloatField(editable=False, null=True, help_text="Average pace in minutes per kilometer")
    
    @property
    def formatted_average_pace(self):
        if self.average_pace is not None:
            minutes = int(self.average_pace)
            seconds = int((self.average_pace - minutes) * 60)
            return f"{minutes:02d}m {seconds:02d}s"
        return None

    @property
    def formatted_time(self):
        if self.time is not None:
            time_delta = timedelta(seconds=self.time)
            hours, remainder = divmod(time_delta.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            if hours > 0:
                return f"{hours:02d}h {minutes:02d}m {seconds:02d}s"
            else:
                return f"{minutes:02d}m {seconds:02d}s"
        return None

    def save(self, *args, **kwargs):
        if self.distance <= 0:
            raise ValueError("Distance must be greater than 0.")
        
        if self.time <= 0:
            raise ValueError("Time must be greater than 0.")
        if isinstance(self.time, str):
            time_parts = self.time.split(':')
            if len(time_parts) == 3:
                hours, minutes, seconds = map(int, time_parts)
                self.time = hours * 3600 + minutes * 60 + seconds
            elif len(time_parts) == 2:
                minutes, seconds = map(int, time_parts)
                self.time = minutes * 60 + seconds
            else:
                raise ValueError("Invalid time format. Use 'HH:MM:SS' or 'MM:SS'.")
        if self.distance and self.time:
            self.average_pace = round(self.time / 60 / self.distance, 2)
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        formatted_pace = self.formatted_average_pace or "N/A"
        formatted_time = self.formatted_time or "N/A"
        return f"Run on {self.date} - {self.distance}km in {formatted_time} (Pace: {formatted_pace}/km)"
