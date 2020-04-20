from django.shortcuts import render

def home(request):
	'''
	Write this code from rapidapi 
	for your own  url and header after subscribing to the api
	'''

	except Exception as e:
		response="Error"

	return render(request,'home.html',{'api': response})
	# return render(request,'home.html',{})

def about(request):
	return render(request,'about.html',{})


