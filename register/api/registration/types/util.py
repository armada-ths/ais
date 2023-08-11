from rest_framework.fields import empty

from register.api.registration.types.cr import (
    CRRegistrationSerializer,
    CRSignedRegistrationSerializer,
)

from register.api.registration.types.registration import RegistrationType

from register.api.registration.util import (
    UserPermission,
)

def get_serializer(registration, data=empty, context={}):
	user = context["user"]
	if user != None:
		permission = UserPermission(user)

	if registration.type == RegistrationType.CompleteRegistration:
		Serializer = CRRegistrationSerializer
	elif registration.type == RegistrationType.CompleteRegistrationSigned:
		# If user is sales, they may change anything he likes
		if permission != None and permission == UserPermission.SALES:
			Serializer = CRRegistrationSerializer
		else:
			Serializer = CRSignedRegistrationSerializer

	return Serializer(
		registration,
		data=data,
		partial=True,
		context=context,
	)