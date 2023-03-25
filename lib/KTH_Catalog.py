import subprocess, base64

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from people.models import Profile


def lookup_user(kth_id):
    """
    Lookup a user by KTH-ID. First, an attempt to connect to KTH directory using LDAP protocol is made.
    If the first attempt fails, a second attempt is made using KTH Profiles API.

    Params:
            `kth_id`: User's KTH-ID (username)

    Returns:
            `user_info`: User information containing the email, first name and last name if available.
    """

    # Try ldap protocol to get user details
    user_dict = lookup_user_with_ldap(kth_id)

    # If ldap does not succeed, try  api
    if user_dict is None:
        user_dict = lookup_user_with_api(kth_id)

    return user_dict


def lookup_user_with_ldap(kth_id):
    try:
        raw = (
            subprocess.check_output(
                [
                    "ssh",
                    "armada@cloud.armada.nu",
                    "ldapsearch -x -h ldap.kth.se -s sub -b 'ou=Addressbook,dc=kth,dc=se' 'ugKthid="
                    + kth_id
                    + "'",
                ],
                timeout=3,
            )
            .decode("utf-8")
            .split("\n")
        )
    except:
        print("failed to connect to LDAP")
        return None

    user_info = dict(email=None, first_name=None, last_name=None)

    for line in raw:
        if line.startswith("mail: "):
            user_info["email"] = line[6:].strip()

        if line.startswith("givenName: "):
            user_info["first_name"] = line[11:].strip()

        if line.startswith("givenName:: "):
            user_info["first_name"] = base64.b64decode(line[12:].strip())

        if line.startswith("sn: "):
            user_info["last_name"] = line[4:].strip()

        if line.startswith("sn:: "):
            user_info["last_name"] = base64.b64decode(line[5:].strip())

    return user_info


def lookup_user_with_api(kth_id):
    # KTH Profiles API - Swagger: https://api.kth.se/api/profile/swagger/?url=/api/profile/swagger.json#/v1.1/getPublicProfile_v11
    # At this moment, not all the users are found due to an issue in the Profile API. We use kottnet API in the meantime.
    # base_uri = "https://api.kth.se/api/profile/1.1/"
    base_uri = "https://api.kottnet.net/kth/"

    uri = base_uri + kth_id

    retry_strategy = Retry(
        total=2, status_forcelist=[429, 500, 502, 503, 504], method_whitelist=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    sess = requests.Session()
    sess.mount("https://", adapter)

    try:
        response = sess.get(uri)
        json = response.json()

        if response.status_code == 404:
            print("student not found")
            return None

        if response.status_code // 100 != 2 or len(response.content) == 0:
            print("failed to connect to KTH Profiles API")
            return None
    except:
        return None

    email = json.get("username")
    if email is not None:
        email += "@kth.se"

    full_name = json.get("name")
    first_name = None
    last_name = None
    if full_name is not None:
        full_name = full_name.split(" ", 1)
        first_name = full_name[0]
        last_name = full_name[1]

    return dict(email=email, first_name=first_name, last_name=last_name)


def merge_user_info(user, info):
    """
    Merge user personal details with information retrieved from their KTH account and returns a confirmation of the operation.
    """
    if (
        info is not None
        and Profile.objects.filter(user=user, kth_synchronize=False).count() == 0
    ):
        if info["first_name"] is not None:
            user.first_name = info["first_name"]

        if info["last_name"] is not None:
            user.last_name = info["last_name"]

        if info["email"] is not None and (
            user.email is None or len(user.email) == 0 or user.email.endswith("@kth.se")
        ):
            user.email = info["email"]

        return True

    return False
