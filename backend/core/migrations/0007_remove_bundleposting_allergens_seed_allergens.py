from django.db import migrations

UK_ALLERGENS = [
    "Celery",
    "Cereals containing gluten",
    "Crustaceans",
    "Eggs",
    "Fish",
    "Lupin",
    "Milk",
    "Molluscs",
    "Mustard",
    "Peanuts",
    "Sesame",
    "Soybeans",
    "Sulphur dioxide and sulphites",
    "Tree nuts",
]


def seed_allergens(apps, schema_editor):
    Allergen = apps.get_model("core", "Allergen")
    for name in UK_ALLERGENS:
        Allergen.objects.get_or_create(name=name)


def unseed_allergens(apps, schema_editor):
    Allergen = apps.get_model("core", "Allergen")
    Allergen.objects.filter(name__in=UK_ALLERGENS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_allergen_consumerreport_consumerreview_sellerreport_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bundleposting",
            name="allergens",
        ),
        migrations.RunPython(seed_allergens, unseed_allergens),
    ]
