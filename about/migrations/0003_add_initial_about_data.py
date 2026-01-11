# Generated manually to add initial about data

from django.db import migrations


def add_initial_data(apps, schema_editor):
    WhoWeAre = apps.get_model('about', 'WhoWeAre')
    OurStory = apps.get_model('about', 'OurStory')
    WhatSetsUsApart = apps.get_model('about', 'WhatSetsUsApart')
    Partner = apps.get_model('about', 'Partner')

    # Add Who We Are content
    WhoWeAre.objects.create(
        title='Who We Are',
        content='''
        <p>Parliament Watch Uganda is a Parliament monitoring initiative of the Centre for Policy Analysis (CEPA) that began in 2013 with the goal of bridging the gap between Parliament and citizens and to make the legislature more transparent, open and accessible.</p>
        <p>Today, we're the leading non-governmental source of legislative information, analysis and critical research on parliament and informed public policy and legislative action in Uganda.</p>
        <p>Our mission is to enhance transparency, accountability, and citizen engagement in the parliamentary process through comprehensive monitoring, analysis, and public education.</p>
        ''',
        is_active=True
    )

    # Add Our Story content
    OurStory.objects.create(
        title='Our Story',
        content='''
        <p>Parliament Watch Uganda was established in 2013 as an initiative of the Centre for Policy Analysis (CEPA) to address the critical need for greater transparency and citizen engagement in Uganda's parliamentary processes.</p>
        <p>Since our inception, we have been dedicated to monitoring parliamentary activities, analyzing legislative processes, and providing accessible information to citizens, civil society organizations, and policymakers.</p>
        <p>Over the years, we have grown from a small monitoring initiative to a comprehensive platform that tracks bills, parliamentary proceedings, budget allocations, and provides critical analysis on governance and accountability issues.</p>
        <p>Our commitment to transparency and accountability drives everything we do, and we continue to work towards a more informed and engaged citizenry in Uganda's democratic processes.</p>
        ''',
        is_active=True
    )

    # Add What Sets Us Apart items
    WhatSetsUsApart.objects.create(
        title='Comprehensive Monitoring',
        description='We provide real-time tracking and analysis of all parliamentary activities, including bills, debates, committee work, and budget processes.',
        order=1,
        is_active=True
    )

    WhatSetsUsApart.objects.create(
        title='Data-Driven Analysis',
        description='Our research and analysis are grounded in comprehensive data collection and rigorous methodology, ensuring accurate and reliable information.',
        order=2,
        is_active=True
    )

    WhatSetsUsApart.objects.create(
        title='Citizen Engagement',
        description='We bridge the gap between Parliament and citizens by making complex legislative information accessible and understandable to the general public.',
        order=3,
        is_active=True
    )

    WhatSetsUsApart.objects.create(
        title='Independent Research',
        description='As a non-governmental organization, we provide unbiased, independent analysis and research on parliamentary and governance issues.',
        order=4,
        is_active=True
    )

    WhatSetsUsApart.objects.create(
        title='Transparency Advocacy',
        description='We advocate for greater transparency and accountability in parliamentary processes and work to strengthen democratic institutions.',
        order=5,
        is_active=True
    )

    WhatSetsUsApart.objects.create(
        title='Capacity Building',
        description='We provide training and resources to civil society organizations, media, and citizens to enhance their understanding of parliamentary processes.',
        order=6,
        is_active=True
    )

    # Add sample Partners
    Partner.objects.create(
        name='Centre for Policy Analysis (CEPA)',
        description='Our parent organization dedicated to policy research and analysis.',
        website_url='https://cepa.org.ug',
        order=1,
        is_active=True
    )

    Partner.objects.create(
        name='Uganda Parliament',
        description='The legislative arm of the Government of Uganda.',
        website_url='https://www.parliament.go.ug',
        order=2,
        is_active=True
    )

    Partner.objects.create(
        name='Civil Society Organizations',
        description='Various CSOs working on governance, transparency, and accountability in Uganda.',
        order=3,
        is_active=True
    )

    Partner.objects.create(
        name='Development Partners',
        description='International organizations supporting democratic governance and transparency initiatives.',
        order=4,
        is_active=True
    )


def remove_initial_data(apps, schema_editor):
    WhoWeAre = apps.get_model('about', 'WhoWeAre')
    OurStory = apps.get_model('about', 'OurStory')
    WhatSetsUsApart = apps.get_model('about', 'WhatSetsUsApart')
    Partner = apps.get_model('about', 'Partner')

    # Remove all initial data
    WhoWeAre.objects.all().delete()
    OurStory.objects.all().delete()
    WhatSetsUsApart.objects.all().delete()
    Partner.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0002_ourstory_partner_whatsetsusapart_whoweare'),
    ]

    operations = [
        migrations.RunPython(add_initial_data, remove_initial_data),
    ]
