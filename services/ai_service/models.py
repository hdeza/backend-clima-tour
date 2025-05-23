from django.db import models

# Create your models here.

class GeminiResponse(models.Model):
    prompt = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to: {self.prompt[:50]}..."
