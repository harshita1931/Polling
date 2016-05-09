from django.shortcuts import render
from .models import MainTable, PreferenceTable
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.

def display(request):
	return render(request, 'poll/displayform.html', {})

def dummy(request):
	user_ID1 = request.POST.get('user_ID', False)
	org_ID1 = request.POST.get('org_ID', False)
	foodentered = request.POST.get('food_ID', False)
	foods = foodentered.split(",")
	user_name1 = request.POST.get('user_name', False)
	print("hello1")
	MainTable_insertobj = MainTable.objects.create(userID=user_ID1, username=user_name1, organizationID=org_ID1)
	print("hello 1.5")
	size = len(foods)
	print(size)
	for i in range(0,size):
		PreferenceTable_insertobj = PreferenceTable.objects.create(userID_id=user_ID1, foodID=foods[i])  
		print("hello2", i)

	url = "/thanks/"
	return HttpResponseRedirect(url)	



def thanks(request):
	return render(request, 'poll/thanks.html', {})

def results(request):
	NoOfItems = 5		#this number is to be hardcoded; it is the number of food items present in the menu
	renderdict = {}		#dictionary with foodID as key and count as value
	for i in range(1, NoOfItems+1):
		renderdict[i] = 