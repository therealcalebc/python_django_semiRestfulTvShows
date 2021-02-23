from django.shortcuts import render, redirect, HttpResponse
from datetime import datetime, date
from .models import Show

title = 'Semi-RESTful TV Shows'
networks = ('ABC', 'CBS', 'FOX', 'NBC')

def index(request):
	return redirect('/shows')

def view_shows_list(request):
	r = title + "<br><br>- All Shows -<br>"
	shows = Show.objects.all()
	for s in shows:
		r += "<br>- - " + str(s.id) + s.title + s.network + s.release_date.strftime("%Y-%m-%d")
	# return HttpResponse(r)
	return render(request, 'index.html', { 'title': title, 'shows': shows })

def new_show(request):
	r = title + "<br><br>- New Show -<br>"
	r += "<br><br> ...a form to enter info about new show to create..."
	# return HttpResponse(r)
	return render(request, 'create.html', { 'title': title, 'networks': networks })

def create_show(request):
	print(f"...creating new show {request.POST['title']}...")
	s = Show.objects.create(title=request.POST['title'], network=request.POST['network'], release_date=datetime.strptime(request.POST['release_date'], "%Y-%m-%d").date(), description=request.POST['description'])
	print(f"...created new show {s.id}: {s.title}...")
	return redirect(f"/shows/{s.id}")

def view_show(request, id):
	r = title + "<br><br>- TV Show -<br>" + str(id)
	s = Show.objects.get(id=id)
	r += "<br>- - " + str(s.id)
	r += "<br>- - " + s.title
	r += "<br>- - " + s.network
	r += "<br>- - " + s.release_date.strftime("%Y-%m-%d")
	# return HttpResponse(r)
	return render(request, 'read.html', { 'title': title, 'show': s })

def edit_show(request, id):
	r = title + "<br><br>- TV Show -<br>" + str(id)
	s = Show.objects.get(id=id)
	r += "<br>- - " + str(s.id)
	r += "<br>- - " + s.title
	r += "<br>- - " + s.network
	r += "<br>- - " + s.release_date.strftime("%Y-%m-%d")
	r += "<br><br> ...a form to enter info about new show to create..."
	# return HttpResponse(r)
	return render(request, 'update.html', { 'title': title, 'show': s, 'networks': networks })

def update_show(request, id):
	s = Show.objects.get(id=id)
	title = request.POST['title']
	network = request.POST['network']
	release_date = datetime.strptime(request.POST['release_date'], "%Y-%m-%d").date()
	description = request.POST['description']
	print(f"...updating show {id}: {title} {network} {release_date} {description}...")
	save_required = False
	if title and title != s.title:
		s.title = title
		save_required = True
	if network and network != s.network:
		s.network = network
		save_required = True
	if release_date and release_date != s.release_date:
		s.release_date = release_date
		save_required = True
	if description != s.description:
		s.description = description
		save_required = True
	if save_required:
		s.save()
	return redirect(f"/shows/{s.id}")

def delete_show(request, id):
	s = Show.objects.get(id=id)
	print(f"...destroying show {s.id}: {s.title}...")
	s.delete()
	return redirect("/shows")
