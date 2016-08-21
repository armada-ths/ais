from django.contrib.auth.models import User
from people.models import Profile
from lib.KTH_Catalog import lookup_user

def callback(tree):
    kth_id = tree[0][0].text
    KTH_user = lookup_user(kth_id)
    user = User.objects.filter(username=kth_id).first()
    if not user:
        user = User.objects.filter(email=KTH_user['email']).first()
        if not user:
            user = User.objects.create(
                username=kth_id,
                email=KTH_user['email'])
        user.username = kth_id
        user.first_name = KTH_user['first_name']
        user.last_name = KTH_user['last_name']
        user.save()