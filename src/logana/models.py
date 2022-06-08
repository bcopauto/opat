from django.db import models
#from applications.models import Application


class Domain(models.Model):
    url = models.CharField(max_length=150, unique=True)
    domain = models.CharField(max_length=150, unique=True)
    
    def __str__(self):
        return self.home_page

class Project(models.Model):

    project_name = models.CharField(max_length=150, unique=True)
    project_description = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    domain= models.ForeignKey(Domain, on_delete = models.CASCADE, default="")
    logs_start_date = models.DateField(null=True, blank=True)
    logs_end_date  = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)
    no_rows = models.IntegerField(null=True, blank=True)
    no_cols = models.IntegerField(null=True, blank=True)
    app_id = models.ForeignKey('applications.Application', on_delete = models.CASCADE, default="")
    
    
    def __str__(self):
        return self.project_name



class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='./')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
