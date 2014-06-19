import urllib2
accounts_url="/accounts/return/getsession/"

def getUrl(request):
    url=accounts_url+"?"
    url=url+"ipadd="+request.META['REMOTE_ADDR']
    url=url+"&browser="+request.META['HTTP_USER_AGENT'].replace(';','$$').replace(' ','%20')
    return url
    
def getSession(url):
    try:
        req=urllib2.Request(url)
        resp=urllib2.urlopen(req)
        resp_str=resp.read()
        return resp_str
    except Exception as e:
        return 'False,'+e

def getSessionFromAccounts(request):
    url=getUrl(request)
    return getSession(url)
