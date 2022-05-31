import re
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
import requests, json
from django.contrib import messages
from regex import D
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .models import Record
from datetime import datetime
from django.views.decorators.cache import cache_control
from django.contrib.auth import authenticate,login,logout

# Create your views here.


def register(request):
    if request.method == 'POST': #if signup hit
        form = RegisterForm(request.POST) #check data
        if form.is_valid(): #info is valid or not
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'welcome {username} to login page')
            return redirect('login')
    else: #new user
        form = RegisterForm()
    return render(request, 'foodList/users.html', {'form':form}) #new user directed to this reg page\

@login_required
def user(request):
    if not request.user.is_authenticated:
        return render(request, '/')
    foodName = None
    if 'search' in request.POST:
        foodName = request.POST.get('Fname')
        url = 'https://trackapi.nutritionix.com/v2/search/instant?query='+foodName
        headers = {'content-type':'application/json', 'x-app-id':'f24a35c0', 
        'x-app-key':'3d52f634f2f88030d7743e9f92373ec5','x-remote-user-id': '0'}
        response = requests.get(url, headers=headers)
        dic = response.json()
        try:
            food = dic['common'][0]['food_name']
        except:
            msg = 'sorry'
            return render(request, 'foodList/index.html', {'msg':msg})
        #/natural/nutrients 
        url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'

        # data to be sent to api
        data = {"query":food,
        "timezone": "US/Eastern"}
        # sending post request and saving response as response object
        r = requests.post(url = url, headers = headers, data=json.dumps(data))
        food_info = json.loads(r.text)
        nutri = food_info['foods'][0]
        f_name = nutri['food_name']
        quantity = nutri['serving_qty']
        unit = nutri['serving_unit']
        wght = nutri['serving_weight_grams']
        cal = nutri['nf_calories']
        carbs = nutri['nf_total_carbohydrate']
        prot = nutri['nf_protein']
        fats = nutri['nf_total_fat']
        return render(request, 'foodList/index.html', {'f_name':f_name, 'quantity':quantity,'unit':unit, 'wght':wght, 'cal':cal,'carbs':carbs, 'prot':prot, 'fats':fats})
        
    if 'add' in request.POST:
        uname = request.POST.get('uname')
        fname = request.POST.get('fname')
        cals = request.POST.get('cals')
        carbs = request.POST.get('carbs')
        prots = request.POST.get('prots')
        fats = request.POST.get('fats')
        units = request.POST.get('units')
        wghts = request.POST.get('wghts')
        quants = request.POST.get('quants')
        datetime_ = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%fZ')

        # flist = None
        # flist = {'lname':uname, 'lfname':fname, 'lcarbs':carbs, 'lprotien':prots, 'lfats':fats, 
        # 'lcalories':cals, 'lunits':units, 'lweight':wghts, 'lquantity':quants, 'ltime':datetime_}
        record = Record(uname=uname, fname=fname, carbs=carbs, protien=prots, fats=fats, 
        calories=cals, units=units, weight=wghts, quantity=quants, time=datetime_)
        record.save()
    
    flist = None
    flist = Record.objects.filter(uname = request.user.username)
         
    return render(request, 'foodList/index.html', {'flist':flist})

@login_required
def analysis(request):
    if not request.user.is_authenticated:
        return render(request, '/')
    return render(request,'foodList/breakpart.html')

@login_required
def deleteRecord(request, id):
    if not request.user.is_authenticated:
        return render(request, '/')
    consumed_food = Record.objects.get(id=id)
    consumed_food.delete()
    flist = None
    flist = Record.objects.filter(uname = request.user.username)
    return redirect('/user')


#Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

# def user_login(request):
#     return render(request, 'foodList/login.html')
