from django.db import models

class Show(models.Model):
	# id = models.IntegerField() - primary key
	title = models.CharField(max_length=100)
	network = models.CharField(max_length=50)
	release_date = models.DateField()
	description = models.TextField(blank=True, default='')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)