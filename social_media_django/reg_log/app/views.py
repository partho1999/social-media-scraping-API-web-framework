from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from reg_log import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str

from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate
import requests
from django.http import HttpResponseRedirect
# Create your views here.
def index(request):
    # return HttpResponse("this is home Page...!!!")
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!!")
        

       

        return redirect('login')

    #return HttpResponse("this is register Page...!!!")
    return render(request, 'register.html')

def Login(request):
    
    if request.method == 'POST':
        username = request.POST.get('Username')
        pass1 = request.POST.get('pass1')
        #print(username)
        #print(pass1)
        user = authenticate(username=username, password=pass1)
        #print(user)
        try:
            p = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "invalid username or passowrd")
            return redirect('login')
            #raise user.ValidationError("User not exist.")
        return redirect('search')
        # if user is not None:
        #     login(request, user)
        #     messages.success(request, "Logged In Sucessfully!!")
        #     return render(request, "index.html")
        # else:
        #     messages.error(request, "Bad Credentials!!")
        #     return redirect('home')
    
    return render(request, "login.html")


def search (request):
    #defines what happens when there is a POST request
    if request.method == "POST":
        title = request.POST.get("q")
        print(title)
        url ='http://103.96.106.250:5000/facebook_posts/' + title

        #return HttpResponseRedirect(url)


        # data = requests.get('https://w3schools.com')
        # print(data)
        

        messages.info(request, "Scraping...!!!")
        return render(request,'result.html', { 'url' : url })


    #defines what happens when there is a GET request
    else:
        return render(request,'search.html')
    


# def result(request):


#     return HttpResponse('this is search...!!!')
