# Generated by Django 4.2.4 on 2023-11-01 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evoting', '0002_choice_question_delete_election_choice_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]