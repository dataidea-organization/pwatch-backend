from django.core.management.base import BaseCommand
from trackers.models import Bill


class Command(BaseCommand):
    help = 'Add a YouTube video URL to a bill'

    def add_arguments(self, parser):
        parser.add_argument('bill_id', type=int, help='The ID of the bill')
        parser.add_argument('video_url', type=str, help='The YouTube video URL (e.g., https://www.youtube.com/embed/VIDEO_ID)')

    def handle(self, *args, **kwargs):
        bill_id = kwargs['bill_id']
        video_url = kwargs['video_url']

        try:
            bill = Bill.objects.get(id=bill_id)
            bill.video_url = video_url
            bill.save()

            self.stdout.write(self.style.SUCCESS(
                f'Successfully added video URL to bill: {bill.title}'
            ))
            self.stdout.write(f'Video URL: {bill.video_url}')

        except Bill.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                f'Bill with ID {bill_id} does not exist'
            ))
