# Generated by Django 4.0.5 on 2022-06-05 20:48

from django.db import migrations, models
import django.db.models.deletion
import home.blocks
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0024_index_image_file_hash'),
        ('wagtailcore', '0069_log_entry_jsonfield'),
        ('home', '0003_homepage_banner_tittle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='banner_tittle',
        ),
        migrations.AddField(
            model_name='homepage',
            name='sub_title',
            field=models.CharField(default='Default Title', help_text='Overwrites the default title', max_length=100),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='BlogDetailPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('blog_title', models.CharField(help_text='Change the default title', max_length=100)),
                ('content', wagtail.fields.StreamField([('title_and_text', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='Add your title', required=True)), ('text', wagtail.blocks.TextBlock(help_text='Add additional text', required=True))])), ('full_richtext', home.blocks.RichtextBlock())], blank=True, null=True, use_json_field=None)),
                ('blog_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]