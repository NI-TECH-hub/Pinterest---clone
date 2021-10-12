from django.contrib.auth import authenticate, logout
from django.contrib.messages.api import error
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404,render
from .models import AddPost,profile,comment
from django.contrib.auth import login,logout
from .forms import usersignform,userloginform,profileform,userchange,post,commentform,passwordchange
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from datetime import date
from django.contrib.auth import update_session_auth_hash
from .models import profile
from django.contrib.auth.forms import PasswordChangeForm

# **********************************************************************************************************************************
''' Normal funtions to '''


def home(request):
    form = AddPost.objects.all()

    context = {
        'form':form,
    }
    return render(request,'home.html',context)



def sortby(request):
    today = date.today()
    form = AddPost.objects.filter(published__year=today.year, published__month=today.month, published__day=today.day)
    context = {
        'form':form,
    }
    return render(request,'home.html',context)



def search(request):
    query = request.GET['query']
    
    if query :
        result = AddPost.objects.filter(title__icontains=query)
        context = {
            'value':result,
        } 
        message = f"Search results for \t {query}"
        messages.success(request,message)
        return render(request,'search.html',context)
    else :
        return HttpResponseRedirect('/')



# function to like and dislike in  post 
# 1 -- > like and 2 --> dislike 
def like(request,id):
    if request.user.is_authenticated:
        post = get_object_or_404(AddPost,id=request.POST.get('post_id'))
        if id == 1:
            post.likes.add(request.user)
            post.dislikes.remove(request.user)
            message = "Post liked "
            
        else :
            post.likes.remove(request.user)
            post.dislikes.add(request.user)
            message = "Post Diliked"
        messages.success(request,message)
        return HttpResponseRedirect('/')
    else :
        messages.error(request,"you must login to like/Dislike  a post ")
        return HttpResponseRedirect('/login')
    # return home(request)

def deletepost(request,id):
    if request.method == 'POST':
        data = AddPost.objects.get(pk=id)
        data.delete()
        messages.success(request,"Post Deleted")
        return HttpResponseRedirect ('/profile')
def contact(request):

    return HttpResponseRedirect("/")

# ***********************************************************************************************************************************
''' User Specific actions to be performed by user '''



# fetch user data from profile table requested by user 
def userprofile(request):
    userpost = AddPost.objects.filter(user=request.user)
    try:
        data1 = profile.objects.get(pk=request.user)
    except :
        data1 = None
    # print(data1)
    likes = 0
    dislikes =0
    
    for i in userpost:
        likes+=i.total_likes()
        dislikes+=i.total_dislikes()

    context = {
        'form':data1,
        'userdata':userpost,
        'totalpost':len(userpost),
        'likes':likes,
        'dislikes':dislikes,
    }
    return render(request,'profile.html',context)

def editprofile(request):
    if request.method == 'POST':
        f1=userchange(request.POST,instance=request.user)
        p1 = profile.objects.get(pk=request.user)
        f2=profileform(request.POST,request.FILES,instance=p1)
        print('ehh')
        if f1.is_valid() and f2.is_valid():
            print('hh')
            f1.save()
            f2.save()
            messages.success(request,"Profile updated successfully !!")
            return HttpResponseRedirect('/profile')
        else :
            messages.error(request,'pls enter details correclty ')
            return HttpResponseRedirect('/editprofile')
    else:
        f1=userchange(instance=request.user)
        p1 = profile.objects.get(pk=request.user)
        f2=profileform(instance=p1)

    context = {
        'form1':f1,
        'form2':f2,
    }
    # print(context)
    return render(request,'editprofile.html',context)



def addpost(request):
    if request.method == 'POST':
        form=post(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request,'Poted successfully !!')
            return HttpResponseRedirect('/')
        else :
            messages.error(request,'Enter valid data !!! ')
    else :
        form=post()

    context = {
        'form':form,
    }            
    return render(request,'addpost.html',context)


def viewimage(request,id):
    form = AddPost.objects.get(pk=id)
    comments = comment.objects.filter(post = form)
    
    if request.method == 'POST' :
        if request.user.is_authenticated:
            comment_form = commentform(request.POST or None)
            if comment_form.is_valid():
                content = request.POST.get('content')
                com = comment.objects.create(post=form ,user = request.user,content=content)
                com.save()
        else :
            return HttpResponseRedirect('/login')

    else:
        comment_form = commentform()
    
    context = {
        'form':form,
        'comments':comments,
        'commentform':comment_form,
    }

    return render(request,'view.html',context)





# ****************************************************************************************************************************

''' Authentication functions for user starts here '''
def userlogin(request):
    if request.method == 'POST':
        form = userloginform(request=request,data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password']
            user = authenticate(username=uname,password=upass)
            if user is not None:
                login(request,user)
                # user = AddPost.objects.create(user=request.user)
                messages.success(request,f"Welcome to pinterest  {uname}")
                return HttpResponseRedirect('/')
        else :
            messages.error(request,"Enter a valid username / password ")
            return HttpResponseRedirect('/login')
    else :
        form=userloginform()

    context = {
        'form':form,
        'name':'login Form',
        'val':1,
    }
    return render(request,'login.html',context)


def usersignup(request):
    if request.method == 'POST':
        form = usersignform(request.POST)
        if form.is_valid():
            form.save()
            # usermail = form.cleaned_data['email']
            # username = form.cleaned_data['username']
            # password = form.cleaned_data['password1']
            # message = f"Welcome {username} to pinterest .\n  We are sending these mail so to give you data if you forget .\n \t Username - {username} \n \t password - {password}.\n Thank you for joining pinterest . "
            # send_mail("Pinterest Login details ",message,settings.EMAIL_HOST_USER,[usermail,])
            
            messages.success(request,'Account Created ! Please Login ')
            return HttpResponseRedirect('/login')
        else:
            messages.error(request,'')
    else :
        form =usersignform()
    
    context = {
        'form':form,
        'name':'Signup Form',
    }
    return render(request,'login.html',context)

def changepassword(request):
    if request.method == 'POST':
        form  = passwordchange(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request,"Password change successfully !")
            return HttpResponseRedirect('/profile')
    else :
        form = passwordchange(request.user)

    context = {

        'form':form,
        'name':'Change Password Form',
    }
    return render(request,'login.html',context)
    


def userlogout(request):
    logout(request)
    messages.error(request,"You logged out ! Login Again ")
    return HttpResponseRedirect('/login')

''' Authentication functions for Ends   here '''

