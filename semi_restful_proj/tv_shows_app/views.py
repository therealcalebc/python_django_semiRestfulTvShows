from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
#from django.contrib.messages import constants as messages
from datetime import datetime, date
from .models import Show

# MESSAGE_TAGS = {
# 	messages.ERROR: 'danger'
# }

title = 'Semi-RESTful TV Shows'
networks = ('ABC', 'CBS', 'FOX', 'NBC')

#=============================
# -- Processing/Redirects --
#=============================
def index(request):
	return redirect('/shows')

def create_show(request):
	errors = Show.objects.basic_validator(request.POST)
	if errors:
		for key, value in errors.items():
			messages.error(request, value, extra_tags="alert-danger")
		request.session['repopnew'] = {
			'title': request.POST['title'],
			'network': request.POST['network'],
			'release_date': request.POST['release_date'],
			'description': request.POST['description']
		}
		return redirect("/shows/new")
	if Show.objects.filter(title=request.POST['title']):
		messages.error(request, "Title must be unique", extra_tags="alert-danger")
		request.session['repopnew'] = {
			'title': request.POST['title'],
			'network': request.POST['network'],
			'release_date': request.POST['release_date'],
			'description': request.POST['description']
		}
		return redirect("/shows/new")
	s = Show.objects.create(title=request.POST['title'], network=request.POST['network'], release_date=datetime.strptime(request.POST['release_date'], "%Y-%m-%d").date(), description=request.POST['description'])
	messages.success(request, "New show successfully created", extra_tags="alert-success")
	return redirect(f"/shows/{s.id}")

def update_show(request, id):
	errors = Show.objects.basic_validator(request.POST)
	if errors:
		for key, value in errors.items():
			messages.error(request, value, extra_tags="alert-danger")
		return redirect(f"/shows/{id}/edit")
	s = Show.objects.get(id=id)
	s.title = request.POST['title']
	s.network = request.POST['network']
	s.release_date = datetime.strptime(request.POST['release_date'], "%Y-%m-%d").date()
	s.description = request.POST['description']
	s.save()
	messages.success(request, "Show info successfully updated", extra_tags="alert-success")
	return redirect(f"/shows/{s.id}")

def delete_show(request, id):
	s = Show.objects.get(id=id)
	s.delete()
	return redirect("/shows")

#=============================
# -- Rendering --
#=============================
def new_show(request):
	context = { 'title': title, 'default_networks': networks }
	if 'repopnew' in request.session:
		context['repopnew'] = request.session['repopnew']
		del request.session['repopnew']
	return render(request, 'create.html', context)


def view_shows_list(request):
	shows = Show.objects.all()
	return render(request, 'index.html', {'title': title, 'shows': shows})


def view_show(request, id):
	s = Show.objects.get(id=id)
	return render(request, 'read.html', {'title': title, 'show': s})


def edit_show(request, id):
	s = Show.objects.get(id=id)
	return render(request, 'update.html', {'title': title, 'show': s, 'default_networks': networks})
