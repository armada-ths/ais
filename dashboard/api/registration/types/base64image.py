import base64
import binascii
import io
import uuid
import filetype

from rest_framework.fields import ImageField, empty

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile


class Base64FieldMixin:
    EMPTY_VALUES = (None, "", [], (), {})

    @property
    def ALLOWED_TYPES(self):
        raise NotImplementedError

    @property
    def INVALID_FILE_MESSAGE(self):
        raise NotImplementedError

    @property
    def INVALID_TYPE_MESSAGE(self):
        raise NotImplementedError

    def __init__(self, *args, **kwargs):
        self.trust_provided_content_type = kwargs.pop(
            "trust_provided_content_type", False
        )
        self.represent_in_base64 = kwargs.pop("represent_in_base64", False)
        super().__init__(*args, **kwargs)

    def to_internal_value(self, base64_data):
        # Check if this is a base64 string
        if base64_data in self.EMPTY_VALUES:
            return None

        if isinstance(base64_data, SimpleUploadedFile):
            return super().to_internal_value(base64_data)

        if isinstance(base64_data, str):
            file_mime_type = None

            # Strip base64 header, get mime_type from base64 header.
            if ";base64," in base64_data:
                header, base64_data = base64_data.split(";base64,")
                if self.trust_provided_content_type:
                    file_mime_type = header.replace("data:", "")

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(base64_data)
            except (TypeError, binascii.Error, ValueError):
                # Currently the frontend will send back the
                # url of the image, which is not a base64.
                # Instead of raising a ValidationError,
                # simply don't set the image if the image is invalid.

                # raise ValidationError(self.INVALID_FILE_MESSAGE)
                return empty

            # Generate file name:
            file_name = self.get_file_name(decoded_file)

            # Get the file name extension:
            try:
                file_extension = self.get_file_extension(file_name, decoded_file)
            except ValidationError:
                return empty

            if file_extension not in self.ALLOWED_TYPES:
                raise ValidationError(self.INVALID_TYPE_MESSAGE)

            complete_file_name = file_name + "." + file_extension
            data = SimpleUploadedFile(
                name=complete_file_name,
                content=decoded_file,
                content_type=file_mime_type,
            )

            return super().to_internal_value(data)

        raise ValidationError(
            _(f"Invalid type. This is not an base64 string: {type(base64_data)}")
        )

    def get_file_extension(self, filename, decoded_file):
        raise NotImplementedError

    def get_file_name(self, decoded_file):
        return str(uuid.uuid4())

    def to_representation(self, file):
        if self.represent_in_base64:
            # If the underlying ImageField is blank, a ValueError would be
            # raised on `open`. When representing as base64, simply return an
            # empty base64 str rather than let the exception propagate unhandled
            # up into serializers.
            if not file:
                return ""

            try:
                with file.open() as f:
                    return base64.b64encode(f.read()).decode()
            except Exception:
                raise OSError("Error encoding file")
        else:
            return super().to_representation(file)


class Base64ImageField(Base64FieldMixin, ImageField):
    """
    A django-rest-framework field for handling image-uploads through raw post data.
    It uses base64 for en-/decoding the contents of the file.
    """

    ALLOWED_TYPES = ("jpeg", "jpg", "png", "gif", "webp")
    INVALID_FILE_MESSAGE = _("Please upload a valid image.")
    INVALID_TYPE_MESSAGE = _("The type of the image couldn't be determined.")

    def get_file_extension(self, filename, decoded_file):
        extension = filetype.guess_extension(decoded_file)
        if extension is None:
            try:
                # Try with PIL as fallback if format not detected
                # with `filetype` module
                from PIL import Image

                image = Image.open(io.BytesIO(decoded_file))
            except (ImportError, OSError):
                raise ValidationError(self.INVALID_FILE_MESSAGE)
            else:
                extension = image.format.lower()

        return "jpg" if extension == "jpeg" else extension
