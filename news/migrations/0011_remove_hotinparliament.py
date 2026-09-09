# Generated manually

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_alter_news_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HotInParliamentComment',
        ),
        migrations.DeleteModel(
            name='HotInParliament',
        ),
    ]
