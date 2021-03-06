# Generated by Django 3.2.7 on 2022-06-02 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('document', models.FileField(upload_to='./')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=150, unique=True)),
                ('domain', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=150, unique=True)),
                ('project_description', models.TextField(blank=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('logs_start_date', models.DateField(blank=True, null=True)),
                ('logs_end_date', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_shared', models.BooleanField(default=False)),
                ('no_rows', models.IntegerField(blank=True, null=True)),
                ('no_cols', models.IntegerField(blank=True, null=True)),
                ('app_id', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='applications.application')),
                ('domain', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='logana.domain')),
            ],
        ),
    ]
