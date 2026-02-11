# Generated manually for Publication model

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0003_partnerpublication_date_received_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('type', models.CharField(choices=[('Policy Brief', 'Policy Brief'), ('Policy Paper', 'Policy Paper'), ('Research Report', 'Research Report'), ('Analysis', 'Analysis')], max_length=100)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('description', models.TextField()),
                ('category', models.CharField(max_length=100)),
                ('url', models.URLField(blank=True, null=True)),
                ('pdf', models.FileField(blank=True, null=True, upload_to='publications/documents')),
                ('image', models.ImageField(blank=True, null=True, upload_to='publications/images')),
                ('featured', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Publication',
                'verbose_name_plural': 'Publications',
                'ordering': ['-created_at'],
            },
        ),
    ]
