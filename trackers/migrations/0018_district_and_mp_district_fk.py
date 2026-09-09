from django.db import migrations, models
import django.db.models.deletion


def normalize_district_name(name):
    collapsed = ' '.join((name or '').split())
    return collapsed.title() if collapsed else 'N/A'


def forwards(apps, schema_editor):
    from collections import defaultdict

    MP = apps.get_model('trackers', 'MP')
    District = apps.get_model('trackers', 'District')

    normalized_names = {
        normalize_district_name(raw)
        for raw in MP.objects.values_list('district_name', flat=True).iterator()
    }

    existing = {district.name.casefold(): district for district in District.objects.all()}
    District.objects.bulk_create([
        District(name=name)
        for name in normalized_names
        if name.casefold() not in existing
    ])

    districts = {district.name.casefold(): district for district in District.objects.all()}
    mp_ids_by_district = defaultdict(list)
    for mp_id, raw in MP.objects.values_list('id', 'district_name').iterator():
        district = districts[normalize_district_name(raw).casefold()]
        mp_ids_by_district[district.id].append(mp_id)

    for district_id, mp_ids in mp_ids_by_district.items():
        MP.objects.filter(id__in=mp_ids).update(district_id=district_id)


def backwards(apps, schema_editor):
    MP = apps.get_model('trackers', 'MP')
    for mp in MP.objects.select_related('district').iterator():
        mp.district_name = mp.district.name if mp.district_id else 'N/A'
        mp.save(update_fields=['district_name'])


class Migration(migrations.Migration):

    dependencies = [
        ('trackers', '0017_committee_chairperson_deputy_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'District',
                'verbose_name_plural': 'Districts',
                'ordering': ['name'],
            },
        ),
        migrations.RenameField(
            model_name='mp',
            old_name='district',
            new_name='district_name',
        ),
        migrations.AddField(
            model_name='mp',
            name='district',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='mps',
                to='trackers.district',
                help_text='Select an existing district, or add a new one if it is not listed.',
            ),
        ),
        migrations.RunPython(forwards, backwards),
        migrations.AlterField(
            model_name='mp',
            name='district',
            field=models.ForeignKey(
                help_text='Select an existing district, or add a new one if it is not listed.',
                on_delete=django.db.models.deletion.PROTECT,
                related_name='mps',
                to='trackers.district',
            ),
        ),
        migrations.RemoveField(
            model_name='mp',
            name='district_name',
        ),
    ]
