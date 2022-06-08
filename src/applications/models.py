from django.db import models



# Create your models here.
class Application(models.Model):
    app_name = models.CharField(max_length = 255)
    app_description = models.TextField(blank=True)
    app_is_active = models.BooleanField(default=False)



    def __str__(self):
        return self.app_name
