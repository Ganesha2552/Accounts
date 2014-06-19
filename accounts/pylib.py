import re
import os
from zu_account.settings import PROFILE_DIR
userfilepath=PROFILE_DIR

def handle_uploaded_file(f,name):
    upload_dir=createUpload(name)
    filename=os.path.join(upload_dir,f.name.split('.')[0]+".jpg")
    with open(filename, 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return '/static/accounts/profile/'+name+'/'+f.name.split('.')[0]+'.jpg'

def usernamevalidate(username):
    if not re.search('[^a-z0-9._]{6,30}',username):
        if (len(username)>6 and len(username)<31):
            return True
        return False
    return False

def passwdvalidate(passwd):
    if len(passwd) > 5:
        cap = re.search('[A-Z]',passwd)
        no = re.search('[0-9]',passwd)
        sp = re.search('[^a-zA-Z0-9]',passwd)
        if not cap:
            return False
        elif not no:
            return False
        elif not sp:
            return False
        else:
            return True
    else:
        return False
        
def createUpload(user):
    list=os.listdir(userfilepath)
    contacts=userfilepath+user
    if not contacts in list:
        if not os.path.exists(contacts):
            os.makedirs(contacts)
    return contacts
