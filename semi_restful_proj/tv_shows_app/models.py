from django.db import models
from datetime import datetime, date

class ShowManager(models.Manager):
	def basic_validator(self, postData):
		errors = {}
		if len(postData['title']) < 2:
			errors["title"] = "Title must be at least 2 characters"
		if len(postData['network']) < 3:
			errors['network'] = "Network must be at least 3 characters"
		try:
			if datetime.strptime(postData['release_date'], "%Y-%m-%d").date() < date(1928, 7, 2):
				errors['release_date'] = "Release date must be after July 1st, 1928"
			elif datetime.strptime(postData['release_date'], "%Y-%m-%d").date() > date.today():
				errors['release_date'] = "Release date must be in the past"
		except:
			errors['release_date'] = "Enter a valid date (ex: 07/02/1928)"
		if postData['description'] and len(postData['description']) < 10:
			errors['description'] = "Description is optional but must be at least 10 characters if included"
		return errors

class Show(models.Model):
	# id = models.IntegerField() - primary key
	title = models.CharField(max_length=100)
	network = models.CharField(max_length=50)
	release_date = models.DateField()
	description = models.TextField(blank=True, default='')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = ShowManager()
