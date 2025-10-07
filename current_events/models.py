from django.db import models


class CurrentEvent(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    category = models.CharField(max_length=200, blank=True)
    date = models.DateField()
    scraped_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField()

    class Meta:
        ordering = ['-date', '-scraped_at']

    def __str__(self):
        return f"{self.date} - {self.title[:50]}"
