import os

from django.core.files import File
from django.core.management import BaseCommand, CommandError
from django.db import transaction

from exhibitors.models import CatalogInfo


class Command(BaseCommand):
    help = """
    Takes a folder of map images and updates the catalogue.
    Specify the path to the folder in the form e.g. ../../path_to_images
    """

    def add_arguments(self, parser):
        parser.add_argument('folder')

    def handle(self, *args, **options):
        folder = options['folder']
        if not folder:
            raise CommandError('[ERROR] Please specify a folder with the images')
        files = os.listdir(folder)
        self.stdout.write("[INFO] Uploading {} map images".format(len(files)))
        for image in files:
            filename = image.lower().split(".")[0]
            self.stdout.write("[INFO] Now processing {}".format(image))
            with transaction.atomic():
                catalogue_info = CatalogInfo.objects.filter(slug=filename).first()
                if not catalogue_info:
                    raise Exception("[ERROR] Catalog info does not exists for {}".format(filename))
                file = File(open("{}{}".format(folder, image), "rb"))
                catalogue_info.location_at_fair_original.save("{}-map.png".format(filename), file, save=True)
                self.stdout.write("[SUCCESS] Saved map for {}".format(filename))
        self.stdout.write("[INFO] Import finished.")
