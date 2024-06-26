# Generated by Django 5.0.4 on 2024-05-22 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appointments", "0004_rename_user_id_consultas_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="Medicos",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("medico", models.CharField(max_length=100)),
                ("hora", models.IntegerField()),
                ("data_appointment", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "medicos",
            },
        ),
    ]
