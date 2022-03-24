from ast import Return
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import os
# from functions import *


# Create your views here.
def index(request):
    # return HttpResponse("this is home Page...!!!")
    return render(request, 'index.html')

def user_register(request):
    if request.method=='POST':
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if pass1 != pass2:
            messages.warning(request, 'Password does not match...!')
            return redirect('register')

        elif User.objects.filter(username=uname).exists():
            messages.warning(request, 'This username already exists')
            return redirect('register')

        elif User.objects.filter(email=email).exists():
            messages.warning(request, 'This email already exists')
            return redirect('register')
        
        else:
            #print(fname,lname,uname,email,pass1,pass2)
            user = User.objects.create_user(first_name=fname, last_name=lname, username=uname, email=email, password=pass1)
            user.save()
            messages.success(request,'User has been registered succssfully')
            return redirect('login')
    return render(request,'register.html')

def user_login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('social')
        else:
            messages.warning(request, 'invalid value! Please register first or try again...')
            return redirect('login')
    return render(request,'login.html')

def user_logout(request):
    logout(request)
    return redirect('/')

@login_required
def social(request):
    return render(request, 'social.html')

@login_required
def facebook_search (request):
    def fun():
        try:
            print("Yay! I still got executed, even though my function has already returned!.... facebook")
        finally:

            

            #defines what happens when there is a POST request
            if request.method == "POST":
                title = request.POST.get("q")
                print(title)
                url ='http://103.96.106.250:5000/facebook_posts/' + title

                # df = Facebook_Posts(title)
                # url = df.to_html()
                #return HttpResponseRedirect(url)
                return render(request,'result.html', { 'url' : url })


            #defines what happens when there is a GET request
            else:
                return render(request,'fb_search.html')

    return fun()

@login_required
def facbook_dowload(request):
    url = 'http://103.96.106.250:5000/facebook_posts/download'
    return HttpResponseRedirect(url)


@login_required
def twitter_search (request):
    def fun():
        try:
            print("Yay! I still got executed, even though my function has already returned!...  twitter")
        finally:

            

            #defines what happens when there is a POST request
            if request.method == "POST":
                title = request.POST.get("q")
                print(title)
                url ='http://103.96.106.250:5000/twitter/' + title
                #return HttpResponseRedirect(url)
                # df = Twitter(title)
                # url = df.to_html()
                # print(url)
                return render(request,'result.html', { 'url' : url })


            #defines what happens when there is a GET request
            else:
                return render(request,'tw_search.html')

    return fun()

@login_required
def twitter_dowload(request):
    url = 'http://103.96.106.250:5000/twitter/download'
    return HttpResponseRedirect(url)


@login_required
def youtube_search (request):
    def fun():
        try:
            print("Yay! I still got executed, even though my function has already returned!...  youtube")
        finally:

            

            #defines what happens when there is a POST request
            if request.method == "POST":
                title = request.POST.get("q")
                print(title)
                url ='http://103.96.106.250:5000/youtube/' + title
                #return HttpResponseRedirect(url)
                return render(request,'result.html', { 'url' : url })


            #defines what happens when there is a GET request
            else:
                return render(request,'yt_search.html')

    return fun()

@login_required
def youtube_dowload(request):
    url = 'http://103.96.106.250:5000/youtube/download'
    return HttpResponseRedirect(url)

@login_required
def google_search (request):
    def fun():
        try:
            print("Yay! I still got executed, even though my function has already returned!... google")
        finally:

            

            #defines what happens when there is a POST request
            if request.method == "POST":
                title = request.POST.get("q")
                print(title)
                url ='http://103.96.106.250:5000/google/' + title
                #return HttpResponseRedirect(url)
                return render(request,'result.html', { 'url' : url })


            #defines what happens when there is a GET request
            else:
                return render(request,'gl_search.html')

    return fun()

@login_required
def google_dowload(request):
    url = 'http://103.96.106.250:5000/youtube/download'
    return HttpResponseRedirect(url)

def upload_file(request):
    
    if request.method == 'POST':

        uploaded_file = request.FILES['document']
        print(uploaded_file)

        if uploaded_file.name.endswith('.csv'):
            
            savefile = FileSystemStorage()
            #we need to save the file somewhere in the project, MEDIA
            #now lets do the savings
            uploaded_file_name = "facebook_post.csv"
            if os.path.exists('media/facebook_post.csv'):
                print ("File exist")
                os.remove('media/facebook_post.csv')
                print('Existing File Removed!')
            name = savefile.save(uploaded_file_name, uploaded_file) #gets the name of the file
            print(name)

            d = os.getcwd() # how we get the current dorectory
            file_directory = d+'\media\\'+name #saving the file in the media directory
            print(file_directory)  
            messages.success(request, 'your file is uploaded succssfully!')

        else:
            messages.success(request, 'your file is not uploaded!')


    else:
        pass
        #messages.warning(request, 'File was not uploaded. Please use .csv file extension!')


    return render(request, 'upload_file.html')


    
