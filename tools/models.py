from django.db import models
from django.db.models import Model

# Create your models here.
class InputSeq(Model):
    input_seq = models.TextField()