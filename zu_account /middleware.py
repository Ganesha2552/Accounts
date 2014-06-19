from django.contrib.auth.models import User
from django.contrib.auth import __init__
from django.http import HttpResponse,HttpResponseRedirect
from zu_account.settings import EXEMPT_URLS
from accountsapi import *

class CustomloginBackend:
    
    def authenticate(self,**kwargs):
        try:
            resp=getSessionFromAccounts(kwargs['request'])
            res=resp.split(',')
            if res[0]==False or res[0]=='False':
                accountsurl="http://tzu-lin02.tsi.zohocorpin.com:8002/accounts/return/url/?"
                returnurl="returnurl="
                return HttpResponseRedirect(accountsurl+returnurl)
            username=res[1]
            try:
                user=User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(username=username)
                user.save()
            return user
        except Exception as e:
            print e
            return None
    
    
    def get_user(self,user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class LoginRequired:
    
    def process_request(self,request):
        if request.path not in EXEMPT_URLS:
            if not request.user.is_authenticated():
                return HttpResponse("User needs to login to access this url")
            return None
        return None