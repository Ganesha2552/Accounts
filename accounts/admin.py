from django.contrib import admin
from accounts.models import *

class User_DetailsAdmin(admin.ModelAdmin):
    list_filter = ['Profile_Id','User_Id','Gender']
    
admin.site.register(User)
admin.site.register(User_Details,User_DetailsAdmin)
admin.site.register(Session_Details)
admin.site.register(Registered_Domain)
admin.site.register(Security_Question)