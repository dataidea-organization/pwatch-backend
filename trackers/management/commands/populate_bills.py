from django.core.management.base import BaseCommand
from trackers.models import Bill, BillReading
from datetime import datetime


class Command(BaseCommand):
    help = 'Populate database with sample bills and readings'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample bills...')

        # Clear existing data
        Bill.objects.all().delete()
        BillReading.objects.all().delete()

        # Create Bill 1
        bill1 = Bill.objects.create(
            title='Forensic and Scientific Analytical Services Bill, 2025',
            bill_type='government',
            year_introduced=datetime(2025, 7, 16).date(),
            mover='Major General Kahinda Otafiire',
            assigned_to='Committee on Defence and Internal Affairs',
            status='1st_reading',
            description='The Forensic and Scientific Analytical Services Bill, 2025 seeks to regulate forensic and scientific analytical services, establish and designate',
            video_url='https://example.com/video1'
        )

        # Create readings for Bill 1
        BillReading.objects.create(
            bill=bill1,
            stage='1st_reading',
            date=datetime(2025, 7, 16).date(),
            details='The Forensic and Scientific Analytical Services Bill, 2025 seeks to regulate forensic and scientific analytical services, establish and designate'
        )

        BillReading.objects.create(
            bill=bill1,
            stage='2nd_reading',
            date=datetime(2025, 8, 15).date(),
            details='The Forensic and Scientific Analytical Services Bill, 2025 seeks to regulate forensic and scientific analytical services, establish and designate'
        )

        # Create Bill 2
        bill2 = Bill.objects.create(
            title='Public Finance Management Amendment Bill, 2025',
            bill_type='private_member',
            year_introduced=datetime(2025, 6, 10).date(),
            mover='Hon. John Doe',
            assigned_to='Committee on Budget',
            status='2nd_reading',
            description='Amendment to the Public Finance Management Act to improve accountability',
            video_url='https://example.com/video2'
        )

        # Create readings for Bill 2
        BillReading.objects.create(
            bill=bill2,
            stage='1st_reading',
            date=datetime(2025, 6, 10).date(),
            details='First reading of the Public Finance Management Amendment Bill'
        )

        BillReading.objects.create(
            bill=bill2,
            stage='2nd_reading',
            date=datetime(2025, 7, 5).date(),
            details='Second reading with committee recommendations'
        )

        # Create Bill 3
        bill3 = Bill.objects.create(
            title='Education Standards and Quality Assurance Bill, 2024',
            bill_type='government',
            year_introduced=datetime(2024, 3, 15).date(),
            mover='Hon. Minister of Education',
            assigned_to='Committee on Education',
            status='assented',
            description='Bill to establish standards for quality education across Uganda',
            video_url='https://example.com/video3'
        )

        # Create readings for Bill 3
        BillReading.objects.create(
            bill=bill3,
            stage='1st_reading',
            date=datetime(2024, 3, 15).date(),
            details='First reading of the Education Standards Bill'
        )

        BillReading.objects.create(
            bill=bill3,
            stage='2nd_reading',
            date=datetime(2024, 4, 20).date(),
            details='Second reading with amendments'
        )

        BillReading.objects.create(
            bill=bill3,
            stage='3rd_reading',
            date=datetime(2024, 5, 10).date(),
            details='Third reading and final passage'
        )

        self.stdout.write(self.style.SUCCESS('Successfully created 3 sample bills with readings'))