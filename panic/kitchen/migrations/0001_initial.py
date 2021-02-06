# Generated by Django 3.0.8 on 2020-07-06 18:03

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import kitchen.models.item
import kitchen.models.transaction
import naturalsortfield.fields
import spa_security.fields


class Migration(migrations.Migration):

  initial = True

  dependencies = [
      migrations.swappable_dependency(settings.AUTH_USER_MODEL),
  ]

  operations = [
      migrations.CreateModel(
          name='Item',
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
                  'index',
                  naturalsortfield.fields.NaturalSortField(
                      'name', db_index=True, editable=False, max_length=255
                  )
              ),
              ('name', spa_security.fields.BlondeCharField(max_length=255)),
              ('price', models.DecimalField(decimal_places=2, max_digits=10)),
              (
                  'quantity',
                  models.IntegerField(
                      default=0,
                      validators=[
                          django.core.validators.MinValueValidator(0),
                          django.core.validators.MaxValueValidator(10000)
                      ]
                  )
              ),
              (
                  'shelf_life',
                  models.IntegerField(
                      default=7,
                      validators=[
                          django.core.validators.MinValueValidator(1),
                          django.core.validators.MaxValueValidator(1095)
                      ]
                  )
              ),
              (
                  'next_expiry_date',
                  models.DateField(default=kitchen.models.item.default_expiry)
              ),
              (
                  'next_expiry_quantity',
                  models.IntegerField(
                      default=0,
                      validators=[
                          django.core.validators.MinValueValidator(0),
                          django.core.validators.MaxValueValidator(10000)
                      ]
                  )
              ),
              (
                  'expired',
                  models.IntegerField(
                      default=0,
                      validators=[
                          django.core.validators.MinValueValidator(0),
                          django.core.validators.MaxValueValidator(10000)
                      ]
                  )
              ),
          ],
      ),
      migrations.CreateModel(
          name='SuggestedItem',
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
                  'name',
                  spa_security.fields.BlondeCharField(
                      max_length=255, unique=True
                  )
              ),
          ],
      ),
      migrations.CreateModel(
          name='Transaction',
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
                  'datetime',
                  models.DateTimeField(default=django.utils.timezone.now)
              ),
              (
                  'quantity',
                  models.IntegerField(
                      validators=[
                          kitchen.models.validators.transaction.
                          TransactionQuantityValidator(10000)
                      ]
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
                  'user',
                  models.ForeignKey(
                      on_delete=django.db.models.deletion.CASCADE,
                      to=settings.AUTH_USER_MODEL
                  )
              ),
          ],
      ),
      migrations.CreateModel(
          name='Store',
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
                  'index',
                  naturalsortfield.fields.NaturalSortField(
                      'name', db_index=True, editable=False, max_length=255
                  )
              ),
              ('name', spa_security.fields.BlondeCharField(max_length=255)),
              (
                  'user',
                  models.ForeignKey(
                      on_delete=django.db.models.deletion.CASCADE,
                      to=settings.AUTH_USER_MODEL
                  )
              ),
          ],
      ),
      migrations.CreateModel(
          name='Shelf',
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
                  'index',
                  naturalsortfield.fields.NaturalSortField(
                      'name', db_index=True, editable=False, max_length=255
                  )
              ),
              ('name', spa_security.fields.BlondeCharField(max_length=255)),
              (
                  'user',
                  models.ForeignKey(
                      on_delete=django.db.models.deletion.CASCADE,
                      to=settings.AUTH_USER_MODEL
                  )
              ),
          ],
      ),
      migrations.AddField(
          model_name='item',
          name='preferred_stores',
          field=models.ManyToManyField(to='kitchen.Store'),
      ),
      migrations.AddField(
          model_name='item',
          name='shelf',
          field=models.ForeignKey(
              on_delete=django.db.models.deletion.CASCADE, to='kitchen.Shelf'
          ),
      ),
      migrations.AddField(
          model_name='item',
          name='user',
          field=models.ForeignKey(
              on_delete=django.db.models.deletion.CASCADE,
              to=settings.AUTH_USER_MODEL
          ),
      ),
      migrations.AddIndex(
          model_name='transaction',
          index=models.Index(
              fields=['datetime'], name='kitchen_tra_datetim_c7fc0f_idx'
          ),
      ),
      migrations.AddIndex(
          model_name='store',
          index=models.Index(
              fields=['index'], name='kitchen_sto_index_3262d6_idx'
          ),
      ),
      migrations.AddConstraint(
          model_name='store',
          constraint=models.UniqueConstraint(
              fields=('user', 'name'), name='store per user'
          ),
      ),
      migrations.AddIndex(
          model_name='shelf',
          index=models.Index(
              fields=['index'], name='kitchen_she_index_ff871c_idx'
          ),
      ),
      migrations.AddConstraint(
          model_name='shelf',
          constraint=models.UniqueConstraint(
              fields=('user', 'name'), name='shelf per user'
          ),
      ),
      migrations.AddIndex(
          model_name='item',
          index=models.Index(
              fields=['index'], name='kitchen_ite_index_51a552_idx'
          ),
      ),
      migrations.AddConstraint(
          model_name='item',
          constraint=models.UniqueConstraint(
              fields=('user', 'name'), name='item per user'
          ),
      ),
  ]
