# Generated by Django 4.0.3 on 2022-03-25 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_remove_answer_profile_remove_question_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionstags',
            name='question_id',
        ),
        migrations.RemoveField(
            model_name='questionstags',
            name='tag_id',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='emiter_profile',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='question',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='recever_profile',
        ),
        migrations.DeleteModel(
            name='Friendship',
        ),
        migrations.DeleteModel(
            name='QuestionsTags',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
    ]
