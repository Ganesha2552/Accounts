# Create your views here.

from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.http import *
from django.contrib.sessions.backends.db import SessionStore
from accounts.models import *
from django.shortcuts import render_to_response,render
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth import authenticate
from django.utils import timezone
from django.core.exceptions import *
from django.views.decorators.csrf import csrf_protect
from django.db import *
from pylib import *
import json

@csrf_protect
def signup(request):
    uname=request.POST['username']
    emailid=request.POST['email']
    passwd=request.POST['password']
    confpasswd=request.POST['conformpassword']
    returnurl=request.POST['return']
    if usernamevalidate(uname):
        if passwdvalidate(passwd) and confpasswd==passwd:
            try:
                user=User.objects.create_user(username=uname,emailid=emailid,password=passwd)
                user.save()
                #uid=User.objects.get_by_natural_key(uname)
                #ques=Security_Question(User_Id=uid,Question=qu,Answer=ans)
                #ques.save()
                return render_to_response('profiledetails.html',{'username':uname,'return':returnurl},context_instance=RequestContext(request))
            except IntegrityError as e:
                return HttpResponse('Username or Email ID is already exits')
                #return render_to_response('temp.html',{'return':'Username or Email ID is already exits'},context_instance=RequestContext(request))
        return HttpResponse('Password must be have both upper,lower case letters, at least one number and special character')
        #return render_to_response('temp.html',{'return':'Password must be have both upper,lower case letters, at least one number and special character'},context_instance=RequestContext(request))
    return HttpResponse('User name must be small letter and allowed _,. and numbers')
    #return render_to_response('temp.html',{'return':'User name must be small letter and allowed _,. and numbers'},context_instance=RequestContext(request))

def profiledetails(request):
    returnurl=request.POST['return']
    uname,uid,fname,gender,lang,coun,time,phone=defaultprofile(request)
    ud=User_Details(User_Id=uid,Nick_Name=fname,Gender=gender,Language=lang,Country=coun,Time_Zone=time,phone_no=phone)
    ud.save()
    return render_to_response('securitydetails.html',{'username':uname,'return':returnurl},context_instance=RequestContext(request))

def defaultprofile(request):
    uname=request.POST['username']
    uid=User.objects.get_by_natural_key(uname)
    fname=request.POST['fname']
    gender=request.POST['gender']
    lang=request.POST['lang']
    coun=request.POST['coun']
    time=request.POST['time']
    phone=request.POST['phone']
    return uname,uid,fname,gender,lang,coun,time,phone

def updateprofile(request):
    uname,uid,fname,gender,lang,coun,time,phone=defaultprofile(request)
    userip=request.META['REMOTE_ADDR']
    browser=request.META['HTTP_USER_AGENT']
    sess=Session_Details.objects.get(User_IP_Address=userip,Browser_Name=browser,Logout=None)
    userobj=User.objects.get(username=sess.User_Id)
    ud=User_Details.objects.filter(User_Id=userobj.username).update(Nick_Name=fname,Gender=gender,Language=lang,Country=coun,Time_Zone=time,phone_no=phone)
    return render_to_response()

def picture(request):
    userip=request.META['REMOTE_ADDR']
    browser=request.META['HTTP_USER_AGENT']
    sess=Session_Details.objects.get(User_IP_Address=userip,Browser_Name=browser,Logout=None)
    userobj=User.objects.get(username=sess.User_Id)
    if request.method == 'POST':
        filepath=handle_uploaded_file(request.FILES['upload'],userobj.username)
        up=User_Details.objects.filter(User_Id=sess.User_Id).update(Profile_Picture=filepath)
        return HttpResponseRedirect('/accounts/')
    return render_to_response('upload.html', {'form': form})

def securitydetails(request):
    uname=request.POST['username']
    uid=User.objects.get_by_natural_key(uname)
    #user=User.objects.get(username=uname)
    ques=request.POST['question']
    ans=request.POST['answer']
    returnurl=request.POST['return']
    qa=Security_Question(User_Id=uid,Question=ques,Answer=ans)
    qa.save()
    #auth.login(request , user)
    createsession(request,uname)
    if returnurl=="":
        return render_to_response('acchome.html',{'username':uname},context_instance=RequestContext(request))
    return HttpResponse(returnurl)

def home(request):
    userip=request.META['REMOTE_ADDR']
    browser=request.META['HTTP_USER_AGENT']
    try:
        sess=Session_Details.objects.get(User_IP_Address=userip,Browser_Name=browser,Logout=None)
        file=User_Details.objects.get(User_Id=sess.User_Id)
        active=Session_Details.objects.filter(User_Id=sess.User_Id,Logout=None)
        return render_to_response('acchome.html',{'username':sess.User_Id,'file':file.Profile_Picture,'activities':active},context_instance=RequestContext(request))
    except Session_Details.DoesNotExist:
        return render_to_response('logbase.html',{},context_instance=RequestContext(request))

def returnurlhome(request):
    returnurl=request.GET['returnurl']
    return render_to_response('logbase.html',{'return':returnurl},context_instance=RequestContext(request))

def test(request):
    name='mei'
    active=Session_Details.objects.filter(User_Id=User.objects.get(username=name),Logout=None)
    return render_to_response('temp.html',{'username':name,'activities':active},context_instance=RequestContext(request))

def set(request):
    return render_to_response('settings.html',{},context_instance=RequestContext(request))

def login(request):
    name=request.POST['username']
    passwd=request.POST['password']
    returnurl=request.POST['return']
    if name.find('@')>-1 and User.objects.filter(emailid=name).exists():
        uname=User.objects.get(emailid=name)
        name=uname.username
    user = authenticate(username=name, password=passwd)
    if user is not None:
        # the password verified for the user
        if user.is_active:
            auth.login(request , user)
            createsession(request,name)
            if returnurl=="":
                return render_to_response('acchome.html',{'username':name},context_instance=RequestContext(request))
            return HttpResponse(returnurl)
        else:
            return HttpResponse("The password is valid, but the account has been disabled!")
    else:
        # the authentication system was unable to verify the username and password
        return HttpResponse("The username and password were incorrect.")
        
def logout(request):
    da=timezone.now()
    userip=request.META['REMOTE_ADDR']
    browser=request.META['HTTP_USER_AGENT']
    sess=Session_Details.objects.get(User_IP_Address=userip,Browser_Name=browser,Logout=None)
    setattr(sess,"Logout",da)
    sess.save()
    auth.logout(request)
    return HttpResponseRedirect('/accounts/')
    #return render_to_response('signup.html',{},context_instance=RequestContext(request))

def forgotpassword(request):
    email=request.POST['email']
    returnurl=request.POST['return']
    if User.objects.filter(emailid=email).exists():
        userobj=User.objects.get(emailid=email)
        sec=Security_Question.objects.get(User_Id=userobj.id)
        return render_to_response('forgotpassword.html',{'email':email,'ques':sec.Question,'return':returnurl},context_instance=RequestContext(request))
    return HttpResponse("Invalid email id")

def chpaform(request):
    return render_to_response('chpaform.html',{},context_instance=RequestContext(request))

def changepass(request):
    uname=request.user
    oldpass=request.POST['oldpass']
    user = authenticate(username=uname, password=oldpass)
    if user is not None:
        defaultchangepass(request,user)
        return HttpResponseRedirect('/accounts/change/password/form/')
    return HttpResponse('Invalid password')

def forgotchangepass(request):
    email=request.POST['email']
    ques=request.POST['question']
    ans=request.POST['answer']
    returnurl=request.POST['return']
    userobj=User.objects.get(emailid=email)
    if Security_Question.objects.filter(User_Id=userobj.id,Question=ques,Answer=ans).exists():
        user=User.objects.get(id=userobj.id)
        defaultchangepass(request,user)
        if returnurl=="":
            return HttpResponse('/accounts/')
        return HttpResponse('/accounts/return/url/?returnurl='+returnurl)
        #return render_to_response('logbase.html',{'return':returnurl},context_instance=RequestContext(request))
    return HttpResponse('Invalid answer')
   
def defaultchangepass(request,user):
    newpass=request.POST['newpass']
    confpass=request.POST['confpass']
    if confpass==newpass:
        user.set_password(newpass)
        user.save()
        
def chemform(request):
    return render_to_response('chemform.html',{},context_instance=RequestContext(request))

def changemail(request):
    uname=request.user
    passwd=request.POST['password']
    newmail=request.POST['newmail']
    user = authenticate(username=uname, password=passwd)
    if user is not None:
        try:
            user.emailid=newmail
            user.save()
            return HttpResponse("success")
        except IntegrityError as e:
            return HttpResponse("Mail id already exists. Please enter another mail id.")
    return HttpResponse('Invalid password')

def chqaform(request):
    return render_to_response('chqaform.html',{},context_instance=RequestContext(request))
    
def changesecurityquestion(request):
    uname=request.user
    passwd=request.POST['password']
    ques=request.POST['question']
    ans=request.POST['answer']
    user = authenticate(username=uname, password=passwd)
    if user is not None:
        sec=Security_Question.objects.filter(User_Id=user).update(Question=ques,Answer=ans)
        return HttpResponse("success")
    return HttpResponse('Invalid password')

def createsession(request,name):
    s = SessionStore()
    s['uname']=name
    s.save()
    sessionid=s.session_key
    domain=request.META['SERVER_NAME']
    userip=request.META['REMOTE_ADDR']
    browser=request.META['HTTP_USER_AGENT']
    da=timezone.now()
    sess=Session_Details(Session_Id=Session.objects.get(pk=sessionid),User_Id=User.objects.get(username=name),Domain_Id=Registered_Domain.objects.get(Server_Name=domain),User_IP_Address=userip,Browser_Name=browser,Login_Time=da)
    sess.save()
    
#@require_http_methods(["POST","GET"])
def getsession(request):
    #domain=request.META['SERVER_NAME']
    domain=request.META['REMOTE_ADDR']
    userip=request.GET['ipadd']
    browser=request.GET['browser'].replace('$$',';').replace('%20',' ')
    if isregistered(domain):
        if Session_Details.objects.filter(User_IP_Address=userip,Browser_Name=browser,Logout=None).exists():
            sess=Session_Details.objects.get(User_IP_Address=userip,Browser_Name=browser,Logout=None)
            userobj=User.objects.get(username=sess.User_Id)
            #profilepicture=User_Details.objects.get(User_Id=sess.User_Id).Profile_Picture
            return HttpResponse('True,'+userobj.username+','+userobj.emailid)
            #return HttpResponse(sess.User_Id)
        return HttpResponse('False,User does not exists')
    return HttpResponse('False,domain not registered'+domain)
    
def isregistered(domain):
    if Registered_Domain.objects.filter(Domain_IP_Address=domain).exists():
        return True
    return False



def emailapi(request):
    domain=request.META['REMOTE_ADDR']
    browser=request.META['HTTP_USER_AGENT']
    if browser.find('urllib')>-1:
        if isregistered(domain):
            li=str(request.GET['list'])
            lis=list(li.split(','))
            queryset=User.objects.all()
            eid=[li for li in queryset]
            #email=User.objects.filter(username__in=li)
            dic={}
            for mail in eid:
                for l in lis:
                    if mail.username==l.strip("'"):
                        dic[mail.username]=mail.emailid
            return HttpResponse(json.dumps(dic))
        return HttpResponse('domain not registered')
    return HttpResponse("Bad Request")
