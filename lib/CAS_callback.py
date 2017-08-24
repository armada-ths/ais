from django.contrib.auth.models import User
from people.models import Profile
from lib.KTH_Catalog import lookup_user
import logging
from django.http import HttpResponseRedirect

def callback(tree):
    kth_id = tree[0][0].text
    logging.info("KTH-ID: %s trying to login" %kth_id)
    user, user_created = User.objects.get_or_create(username=kth_id)
    if user_created:
        try:
            KTH_user=lookup_user(kth_id)
            user.first_name=KTH_user['first_name']
            user.last_name=KTH_user['last_name']
            user.email=KTH_user['email']
            logging.info("Ldap success")
            # Disable password auth, we auth with CAS
            user.set_unusable_password()
            user.save()
            logging.info("User saved")
            person = None
            try:
                person = Profile(user=user)
                person.save()
            except:
                logging.error("Profile creation failed")
                if person:
                    person.delete()
        except:
            logging.error("User creation failed")
            user.delete()
            logging.error("Redirecting to temporary google form at https://goo.gl/forms/kD9mCF3YccFN7XwV2")
            return(HttpResponseRedirect("https://goo.gl/forms/kD9mCF3YccFN7XwV2"))
