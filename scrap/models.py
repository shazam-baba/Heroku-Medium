from django.db import models

# Create your models here.


class Front(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=2000)
    img = models.URLField()
    link = models.URLField()
    text = models.TextField(null=True)
    details = models.CharField(max_length=200,default=0)

    
    def __str__(self):
        return self.author

    
