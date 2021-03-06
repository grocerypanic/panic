# Generated by Django 3.0.13 on 2021-03-09 19:49

from django.db import migrations, models
import django.db.models.deletion
import kitchen.models.mixins


class Migration(migrations.Migration):

  dependencies = [
      ('kitchen', '0008_rename_index_20210301_1629'),
  ]

  operations = [
      migrations.AlterField(
          model_name='item',
          name='shelf',
          field=models.ForeignKey(
              null=True,
              on_delete=django.db.models.deletion.SET_NULL,
              to='kitchen.Shelf'
          ),
      ),
      migrations.SeparateDatabaseAndState(
          database_operations=[
              migrations.RunSQL(
                  sql=
                  'ALTER TABLE kitchen_item_preferred_stores RENAME TO kitchen_preferredstore',
                  reverse_sql=
                  'ALTER TABLE kitchen_preferredstore RENAME TO kitchen_item_preferred_stores',
              ),
          ],
          state_operations=[
              migrations.CreateModel(
                  name='PreferredStore',
                  fields=[
                      (
                          'id',
                          models.AutoField(
                              auto_created=True,
                              primary_key=True,
                              serialize=False,
                              verbose_name='ID'
                          )
                      ),
                      (
                          'item',
                          models.ForeignKey(
                              on_delete=django.db.models.deletion.CASCADE,
                              to='kitchen.Item'
                          )
                      ),
                      (
                          'store',
                          models.ForeignKey(
                              on_delete=django.db.models.deletion.CASCADE,
                              to='kitchen.Store'
                          )
                      ),
                  ],
              ),
              migrations.AlterField(
                  model_name='item',
                  name='preferred_stores',
                  field=models.ManyToManyField(
                      through='kitchen.PreferredStore', to='kitchen.Store'
                  ),
              ),
          ]
      )
  ]
