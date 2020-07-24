from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .forms import CreateUserForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username or Password incorrect')

		context={}
		return render(request, 'login.html', context)

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()

		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				messages.success(request, 'Account created for ' + form.cleaned_data.get('username'))

				return redirect('login')

		context={'form' : form}
		return render(request, 'register.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def home(request):
	
	import requests
	import json
	import pandas as pd
	sorted_df = []
	try:
		

		url ="https://query1.finance.yahoo.com/v7/finance/quote?symbols=ADANIPORTS.NS,ADANIPORTS.BO,ASIANPAINT.NS,500820.BO,AXISBANK.NS,532215.BO,BAJAJ-AUTO.NS,BAJAJ-AUTO.BO,BAJFINANCE.NS,BAJFINANCE.BO,BAJAJFINSV.NS,BAJAJFINSV.BO,BHARTIARTL.NS,BHARTIARTL.BO,INFRATEL.NS,INFRATEL.BO,BPCL.NS,BPCL.BO,BRITANNIA.NS,BRITANNIA.BO,CIPLA.NS,500087.BO,COALINDIA.NS,COALINDIA.BO,DRREDDY.NS,DRREDDY.BO,EICHERMOT.NS,EICHERMOT.BO,GAIL.NS,532155.BO,GRASIM.NS,GRASIM.BO,HCLTECH.NS,HCLTECH.BO,HDFC.NS,HDFC.BO,HDFCBANK.NS,HDFCBANK.BO,HEROMOTOCO.NS,HEROMOTOCO.BO,HINDALCO.NS,HINDALCO.BO,HINDUNILVR.NS,HINDUNILVR.BO,ICICIBANK.NS,532174.BO,INDUSINDBK.NS,532187.BO,INFY.NS,500209.BO"
		response = json.loads((requests.request("GET", url)).content)
		url2 ="https://query1.finance.yahoo.com/v7/finance/quote?symbols=IOC.NS%2CIOC.BO%2CITC.NS%2CITC.BO%2CJSWSTEEL.NS%2CJSWSTEEL.BO%2CKOTAKBANK.NS%2CKOTAKBANK.BO%2CLT.NS%2CLT.BO%2CM%26M.NS%2CM%26M.BO%2CMARUTI.NS%2CMARUTI.BO%2CNESTLEIND.NS%2CNESTLEIND.BO%2CNTPC.NS%2CNTPC.BO%2CONGC.NS%2CONGC.BO%2CPOWERGRID.NS%2CPOWERGRID.BO%2CRELIANCE.NS%2CRELIANCE.BO%2CSBIN.NS%2CSBIN.BO%2CSHREECEM.NS%2CSHREECEM.BO%2CSUNPHARMA.NS%2CSUNPHARMA.BO%2CTATAMOTORS.NS%2CTATAMOTORS.BO%2CTATASTEEL.NS%2CTATASTEEL.BO%2CTCS.NS%2CTCS.BO%2CTECHM.NS%2CTECHM.BO%2CTITAN.NS%2CTITAN.BO%2CULTRACEMCO.NS%2CULTRACEMCO.BO%2CUPL.NS%2CUPL.BO%2CVEDL.NS%2CVEDL.BO%2CWIPRO.NS%2CWIPRO.BO%2CZEEL.NS%2CZEEL.BO"
		response1 = json.loads((requests.request("GET", url2)).content)
		name =[]
		bse_ask =[]
		nse_ask =[]
		bse_bid =[]
		nse_bid =[]
		cost =[]

		for i in range(48):
		    if(i%2==0):
		        nse_ask.append(response['quoteResponse']['result'][i]['ask'])
		        nse_bid.append(response['quoteResponse']['result'][i]['bid'])
		    else:
		        bse_ask.append(response['quoteResponse']['result'][i]['ask'])
		        bse_bid.append(response['quoteResponse']['result'][i]['bid'])
		        name.append(response['quoteResponse']['result'][i]['shortName'])
		    
		for i in range(48):
		    if(i%2==0):
		        nse_ask.append(response1['quoteResponse']['result'][i]['ask'])
		        nse_bid.append(response1['quoteResponse']['result'][i]['bid'])
		    else:
		        bse_ask.append(response1['quoteResponse']['result'][i]['ask'])
		        bse_bid.append(response1['quoteResponse']['result'][i]['bid'])
		        name.append(response1['quoteResponse']['result'][i]['shortName'])

		diff =[]
		arbitrage =[]

		for i in range(48):
		    if(nse_bid[i]<=bse_bid[i]):
		        if(nse_bid[i]<=bse_ask[i]):
		            diff.append(bse_ask[i]-nse_bid[i])
		            cost.append((bse_ask[i]*0.0001)+(nse_bid[i]*0.0001))
		            
		        else:
		            diff.append(-99)
		            cost.append(99)
		    else:
		        if(bse_bid[i]<=nse_ask[i]):
		            diff.append(nse_ask[i]-bse_bid[i])
		            cost.append((bse_bid[i]*0.0001)+(nse_ask[i]*0.0001))
		        else:
		            diff.append(-99)
		            cost.append(-99)
		    arbitrage.append(diff[i] - cost[i])

		

		df = pd.DataFrame({'Name':name,
		'NSE BID':nse_bid,
		'BSE BID':bse_bid,
		'NSE ASK':nse_ask,
		'BSE ASK':bse_ask,
		'DIFF':diff,
		'Arbitrage':arbitrage})

		sorted_df = df.sort_values(by='Arbitrage',kind='mergesort',ascending=False)

		l1 = ['Name','NSE BID','BSE BID','NSE ASK','BSE ASK','Diff','Arbitrage']
		ans = sorted_df.values.tolist()
		df2 ={}
		for i in range(len(ans)):
		    df2[i] = dict(zip(l1,ans[i]))



	except Exception as e:
		response="Error"



	return render(request,'home.html',{'api': df2})
	
	#return render(request,'home.html',{})

@login_required(login_url='login')
def searchPage(request):
	#import json
	#import requests

	#query = request.GET.get('search')
	#return HttpResponse(query)
	#if request.method == 'POST':
		#ticker = request.POST['ticker']
		#url ="https://query1.finance.yahoo.com/v7/finance/quote?symbols="+ ticker
		#response = json.loads((requests.request("GET", url)).content)
		#return render(request, 'search_stock.html',{'ticker' : response})

	#else:
		#return render(request, 'search_stock.html',{'ticker' : "enter proper"})
	return render(request, 'search_stock.html', {})

	

@login_required(login_url='login')
def about(request):
	return render(request,'about.html',{})


