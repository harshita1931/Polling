from django.shortcuts import render
from .models import PreferenceTable, OrganizationTable, FoodItemTable, UserExtraDetails
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.template import RequestContext
from poll.forms import UserForm, UserOrganizationForm
from django.contrib.auth import logout
from django.contrib.auth.models import User
import ast
from django.db import transaction

# Create your views here.


#view for displaying the food options in menu
@login_required
def display(request):
	foods = FoodItemTable.objects.all().values('foodName')

	foods_list = []
	for food in range(0, len(foods)):
		foods_list.append(foods[food]['foodName'])
		

	return render(request, 'poll/displayform.html', {'foods_list':foods_list})


#view for extrating food choices of the user
@login_required
def dummy(request):
	user_ID1 = request.user.id
	user_name1 = request.user.username
	selectedfoods = request.POST.getlist('food',False)
	
	temp = []
	for food in selectedfoods:
		temp.append(str(food))

	selectedfoods = temp
	selectedfoods_size = len(selectedfoods)
	if PreferenceTable.objects.all().filter(userID=request.user.id).count() > 0:
			PreferenceTable.objects.filter(userID=request.user.id).delete()
			
	for i in range(0, selectedfoods_size):
		food_ID = FoodItemTable.objects.all().filter(foodName=selectedfoods[i]).values('id')
		PreferenceTable_insertobj = PreferenceTable.objects.create(userID_id=user_ID1, foodID_id=food_ID[0]['id'])


	url = "/thanks/"
	return HttpResponseRedirect(url)	



#view for thanks 
@login_required
def thanks(request):
	return render(request, 'poll/thanks.html', {})



#view for displaying results
@login_required
def results(request):
	foodPollOrdered_dict = {}		#dictionary with foodID as key and count as value
	
	pollresult = PreferenceTable.objects.all().values('foodID').annotate(count1 = Count('foodID')).order_by('-count1')
	
	temp_list = []

	pollresult_size = len(pollresult)
	for i in range(0, pollresult_size):
		temp_dict = {}
		temp_dict['count'] = pollresult[i]['count1']
		nameOFfood = FoodItemTable.objects.all().filter(id=pollresult[i]['foodID']).values('foodName')  
		temp_dict['name_food'] = nameOFfood[0]['foodName']		
		temp_list.append(temp_dict)

	results = []
	results = temp_list
	return render(request, 'poll/results1.html', {'results':results})

	
#view to register a user
def register(request):
	context = RequestContext(request)
	registered = False
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		
		if user_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			registered = True
		else:
			print user_form.errors
	else:
		user_form = UserForm()
	return render_to_response(
			'poll/register.html',
			{'user_form': user_form, 'registered': registered},
			context)


#view for login
def user_login(request):
	context = RequestContext(request)
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				if UserExtraDetails.objects.all().filter(userID=request.user.id).count() == 0:
					return HttpResponseRedirect("/org_entering/")
				else:
					return HttpResponseRedirect("/")
			else:
				return HttpResponse("Your polling account is disabled.")
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")
	else:
		return render_to_response('poll/login.html', {}, context)


#view for logout
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


#view for printing form for filling organization name after first login
def user_orgName_form(request):
	org_names = OrganizationTable.objects.all().values('organizationName')
	org_names_size = len(org_names)
	temp = []
	for i in range(0, org_names_size):
		temp.append(org_names[i]['organizationName'])

	org_list = []
	org_list = temp
	return render(request, 'poll/register_organization.html', {'organizationNames_list': org_list})


#view to enter organization name by the user after sign-up
@transaction.atomic
def user_orgName(request):
	if request.method == 'POST':
		org_form = UserExtraDetails(organizationName=request.POST['organization_name'], userID= request.user)
		org_form.save()
	else:
		org_form = UserOrganizationForm()
	return HttpResponseRedirect('/')		
