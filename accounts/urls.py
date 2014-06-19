from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'accounts.views.home', name='home'),
    url(r'test/$','accounts.views.test',name='test'),
    url(r'emailapi/$','accounts.views.emailapi',name='api'),
    url(r'set/$','accounts.views.set',name='set'),
    #url(r'return/((?P<url>\S+)$)','accounts.views.intreface',name='interface'),
    url(r'login/$','accounts.views.login',name='login'),
    url(r'account/logout/$','accounts.views.logout',name='logout'),
    url(r'create/$','accounts.views.signup',name='signup'),
    url(r'recovery/','accounts.views.forgotpassword',name='forgotpassword'),
    url(r'password/recovery/$','accounts.views.forgotchangepass',name='forgotpass'),
    url(r'profile/create/$','accounts.views.profiledetails',name='profiledetails'),
    url(r'security/create/$','accounts.views.securitydetails',name='securitydetails'),
    url(r'profile/picture/$','accounts.views.picture',name='picture'),
    url(r'change/password/$','accounts.views.changepass',name='changepass'),
    url(r'change/password/form/$','accounts.views.chpaform',name='changepasswordform'),
    url(r'change/mail/$','accounts.views.changemail',name='changemail'),
    url(r'change/mail/form/$','accounts.views.chemform',name='changeemailform'),
    url(r'change/security/$','accounts.views.changesecurityquestion',name='changesecurityquestion'),
    url(r'change/security/form/$','accounts.views.chqaform',name='changesecurityform'),
    url(r'return/getsession/$','accounts.views.getsession',name='getsession'),
    url(r'return/url/','accounts.views.returnurlhome',name='returnurlhome')
    #url(r'signup','accounts.views.signup',name='signup'),
    #url(r'forgotpass','accounts.views.forgotpass',name='forgotpass'),
    #url(r'home','accounts.views.home',name='home'),
    # url(r'^account/', include('account.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
