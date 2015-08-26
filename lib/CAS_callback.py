from django.contrib.auth.models import User
from lib.KTH_Catalog import lookup_user

def callback(tree):
    kth_id = tree[0][0].text
    user, user_created = User.objects.get_or_create(username=kth_id)
    if user_created:
        KTH_user=lookup_user(kth_id)
        user.first_name=KTH_user['first_name']
        user.last_name=KTH_user['last_name']
        user.email=KTH_user['email']
        user.save()        
