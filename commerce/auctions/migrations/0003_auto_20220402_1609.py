# Generated by Django 3.0.14 on 2022-04-02 23:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bids_comments_listing'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bids',
            new_name='Bid',
        ),
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
    ]
