# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.utils.timezone import utc


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'City'
        db.create_table('apartments_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal('apartments', ['City'])

        # Adding model 'Area'
        db.create_table('apartments_area', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apartments.City'])),
        ))
        db.send_create_signal('apartments', ['Area'])

        # Adding unique constraint on 'Area', fields ['name', 'city']
        db.create_unique('apartments_area', ['name', 'city_id'])

        # Adding model 'Apartment'
        db.create_table('apartments_apartment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apartments.Area'])),
            ('tenant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('added_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('available_from', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('available_to', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('is_shared', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('floor', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('lift', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('num_floors', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sauna', self.gf('django.db.models.fields.IntegerField')()),
            ('rent_pcm', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('size', self.gf('django.db.models.fields.FloatField')()),
            ('garden_size', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('cable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('broadband', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('satellite', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('balcony', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('parking', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('garage', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('bike_storage', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('extra_storage', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('gym', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('laundry', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('kitchen_amenities', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('furniture', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('heating', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('other_amenities', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('apartments', ['Apartment'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Area', fields ['name', 'city']
        db.delete_unique('apartments_area', ['name', 'city_id'])

        # Deleting model 'City'
        db.delete_table('apartments_city')

        # Deleting model 'Area'
        db.delete_table('apartments_area')

        # Deleting model 'Apartment'
        db.delete_table('apartments_apartment')


    models = {
        'apartments.apartment': {
            'Meta': {'object_name': 'Apartment'},
            'added_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apartments.Area']"}),
            'available_from': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'available_to': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'balcony': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bike_storage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'broadband': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extra_storage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'floor': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'furniture': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'garage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'garden_size': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gym': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'heating': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_shared': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'kitchen_amenities': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'laundry': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lift': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'num_floors': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'other_amenities': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'parking': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'rent_pcm': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'satellite': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sauna': ('django.db.models.fields.IntegerField', [], {}),
            'size': ('django.db.models.fields.FloatField', [], {}),
            'tenant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'apartments.area': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('name', 'city'),)", 'object_name': 'Area'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apartments.City']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'apartments.city': {
            'Meta': {'object_name': 'City'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 2, 19, 21, 12, 5, 516903, tzinfo=utc)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 2, 19, 21, 12, 5, 516686, tzinfo=utc)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['apartments']
