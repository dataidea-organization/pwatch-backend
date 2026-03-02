# Generated migration to add 'debt' page slug choice for National Debt Tracker

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0003_footerdocuments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageheroimage',
            name='page_slug',
            field=models.CharField(
                choices=[
                    ('about', 'About Us'),
                    ('contact', 'Contact Us'),
                    ('bills', 'Bills Tracker'),
                    ('mps', 'MPs Tracker'),
                    ('loans', 'Loans Tracker'),
                    ('budgets', 'Budgets Tracker'),
                    ('hansards', 'Hansards Tracker'),
                    ('order-paper', 'Order Paper Tracker'),
                    ('committees', 'Committees'),
                    ('statements', 'Statements'),
                    ('reports-briefs', 'Reports & Briefs'),
                    ('podcast', 'Podcast'),
                    ('gallery', 'Gallery'),
                    ('x-spaces', 'X Spaces'),
                    ('citizens-voice', 'Citizens Voice'),
                    ('debt', 'National Debt Tracker'),
                ],
                help_text='The page this hero image is for',
                max_length=50,
                unique=True,
            ),
        ),
    ]