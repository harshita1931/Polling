from django.shortcuts import render
from .models import MainTable, PreferenceTable, OrganizationTable, FoodItemTable
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.template import RequestContext
from poll.forms import UserForm
from django.contrib.auth import logout
from django.contrib.auth.models import User


# Create your views here.
@login_required
def display(request):
	organizationNames = OrganizationTable.objects.all().values('organizationName')
	organizationNames_list = []
	for i in range(0, len(organizationNames)):
		organizationNames_list.append(organizationNames[i]['organizationName'])

	foods = FoodItemTable.objects.all().values('foodName')

	foods_list = []
	for food in range(0, len(foods)):
		foods_list.append(foods[food]['foodName'])
		

	return render(request, 'poll/displayform.html', {'organizationNames_list': organizationNames_list, 'foods_list':foods_list})

@login_required
def dummy(request):
	org_name = request.POST.get('organization_name', False)
	org_ID1 = OrganizationTable.objects.all().filter(organizationName=org_name).values('id')
	
	print ("org ID is : "+str(org_ID1[0]['id']))

	user_ID1 = request.user.id
	user_name1 = request.user.username
	MainTable_insertobj = MainTable.objects.create(userID_id=user_ID1, username=user_name1, organizationID=org_ID1[0]['id'])

	selectedfoods = request.POST.getlist('food',False)
	
	temp = []
	for food in selectedfoods:
		temp.append(str(food))

	selectedfoods = temp
	print selectedfoods
	selectedfoods_size = len(selectedfoods)
	for i in range(0, selectedfoods_size):
		food_ID = FoodItemTable.objects.all().filter(foodName=selectedfoods[i]).values('id')
		print (food_ID)
		PreferenceTable_insertobj = PreferenceTable.objects.create(userID_id=user_ID1, foodID_id=food_ID[0]['id'])


	url = "/thanks/"
	return HttpResponseRedirect(url)	


@login_required
def thanks(request):
	return render(request, 'poll/thanks.html', {})

@login_required
def results(request):
	foodPollOrdered_dict = {}		#dictionary with foodID as key and count as value
	
	pollresult = PreferenceTable.objects.all().values('foodID').annotate(count1 = Count('foodID')).order_by('-count1')
	
	temp_list = []

	pollresult_size = len(pollresult)
	print pollresult_size
	for i in range(0, pollresult_size):
		print(pollresult[i])
		temp_dict = {}
		temp_dict['count'] = pollresult[i]['count1']
		nameOFfood = FoodItemTable.objects.all().filter(id=pollresult[i]['foodID']).values('foodName')  
		temp_dict['name_food'] = nameOFfood[0]['foodName']		
		temp_list.append(temp_dict)

	results = []
	results = temp_list
	print results
	return render(request, 'poll/results1.html', {'results':results})
	

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

def user_login(request):
	context = RequestContext(request)
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/')
			else:
				return HttpResponse("Your polling account is disabled.")
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")
	else:
		return render_to_response('poll/login.html', {}, context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')