import json
from django.core.management.base import BaseCommand
from trackers.models import MP, ParliamentTerm


class Command(BaseCommand):
    help = 'Import MPs from a JSON file. Use --term <id> to assign MPs to a parliament term (e.g. when adding a new parliament).'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_file',
            type=str,
            help='Path to the JSON file containing MPs data'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing MPs before importing'
        )
        parser.add_argument(
            '--term',
            type=int,
            metavar='ID',
            help='Parliament term ID to assign imported MPs to. If omitted, uses the current parliament term.'
        )

    def handle(self, *args, **options):
        json_file = options['json_file']
        term_id = options.get('term')

        parliament_term = None
        if term_id:
            try:
                parliament_term = ParliamentTerm.objects.get(pk=term_id)
                self.stdout.write(f'Assigning MPs to term: {parliament_term}')
            except ParliamentTerm.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Parliament term with id={term_id} not found.'))
                return
        else:
            parliament_term = ParliamentTerm.objects.filter(is_current=True).first()
            if parliament_term:
                self.stdout.write(f'Using current term: {parliament_term}')

        # Clear existing MPs if requested
        if options['clear']:
            count = MP.objects.count()
            MP.objects.all().delete()
            self.stdout.write(
                self.style.WARNING(f'Deleted {count} existing MPs')
            )

        # Read JSON file
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                mps_data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'File not found: {json_file}')
            )
            return
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR('Invalid JSON format')
            )
            return

        created_count = 0
        updated_count = 0
        skipped_count = 0
        errors = []

        for mp_data in mps_data:
            try:
                # Get party name directly (no mapping needed)
                party = mp_data.get('party', 'Unknown').strip() or 'Unknown'

                # Prepare MP data
                mp_fields = {
                    'first_name': mp_data.get('first_name', '').strip() or 'Unknown',
                    'middle_name': mp_data.get('middle_name', '').strip(),
                    'last_name': mp_data.get('last_name', '').strip() or 'Unknown',
                    'name': mp_data.get('name', '').strip(),
                    'party': party,
                    'constituency': mp_data.get('constituency', 'N/A').strip(),
                    'district': mp_data.get('district', 'N/A').strip(),
                    'phone_no': mp_data.get('phone_no', '').strip(),
                    'email': mp_data.get('email', '').strip(),
                    'bio': mp_data.get('bio'),
                }
                if parliament_term is not None:
                    mp_fields['parliament_term'] = parliament_term

                # Auto-generate name if not provided
                if not mp_fields['name']:
                    name_parts = [mp_fields['first_name']]
                    if mp_fields['middle_name']:
                        name_parts.append(mp_fields['middle_name'])
                    name_parts.append(mp_fields['last_name'])
                    mp_fields['name'] = ' '.join(name_parts)

                # Check if MP already exists (by name or email, within same term if term is set)
                existing_mp = None
                lookup = MP.objects.all()
                if parliament_term is not None:
                    lookup = lookup.filter(parliament_term=parliament_term)
                if mp_fields.get('email'):
                    existing_mp = lookup.filter(email=mp_fields['email']).first()
                if not existing_mp:
                    existing_mp = lookup.filter(name=mp_fields['name']).first()

                if existing_mp:
                    # Update existing MP
                    for field, value in mp_fields.items():
                        setattr(existing_mp, field, value)
                    existing_mp.save()
                    updated_count += 1
                    self.stdout.write(f'Updated: {mp_fields["name"]}')
                else:
                    # Create new MP
                    MP.objects.create(**mp_fields)
                    created_count += 1
                    self.stdout.write(f'Created: {mp_fields["name"]}')

            except Exception as e:
                skipped_count += 1
                error_msg = f'Error processing {mp_data.get("name", "Unknown")}: {str(e)}'
                errors.append(error_msg)
                self.stdout.write(self.style.ERROR(error_msg))

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('Import Summary:'))
        self.stdout.write(self.style.SUCCESS(f'  Created: {created_count}'))
        self.stdout.write(self.style.SUCCESS(f'  Updated: {updated_count}'))
        if skipped_count > 0:
            self.stdout.write(self.style.WARNING(f'  Skipped (errors): {skipped_count}'))
        self.stdout.write(self.style.SUCCESS(f'  Total MPs in database: {MP.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('='*60))

        if errors:
            self.stdout.write(self.style.WARNING('\nErrors encountered:'))
            for error in errors[:10]:  # Show first 10 errors
                self.stdout.write(self.style.WARNING(f'  - {error}'))
            if len(errors) > 10:
                self.stdout.write(self.style.WARNING(f'  ... and {len(errors) - 10} more errors'))