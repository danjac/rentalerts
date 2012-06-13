# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.utils.timezone import utc

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Apartment.landlord'
        db.add_column('apartments_apartment', 'landlord', self.gf('django.db.models.fields.IntegerField')(default=2), keep_default=False)

        # Adding field 'Apartment.agency'
        db.add_column('apartments_apartment', 'agency', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'Apartment.agency_website'
        db.add_column('apartments_apartment', 'agency_website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True), keep_default=False)

        # Adding field 'Apartment.furnished'
        db.add_column('apartments_apartment', 'furnished', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Apartment.landlord'
        db.delete_column('apartments_apartment', 'landlord')

        # Deleting field 'Apartment.agency'
        db.delete_column('apartments_apartment', 'agency')

        # Deleting field 'Apartment.agency_website'
        db.delete_column('apartments_apartment', 'agency_website')

        # Deleting field 'Apartment.furnished'
        db.delete_column('apartments_apartment', 'furnished')


    models = {
        'apartments.apartment': {
            'Meta': {'object_name': 'Apartment'},
            'added_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'agency': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'agency_website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apartments.Area']"}),
            'available_from': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'available_to': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'balcony': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bike_storage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'broadband': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deposit': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extra_storage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'floor': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'furnished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'furniture': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'garage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'garden_size': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gym': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'heating': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_shared': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'kitchen_amenities': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'landlord': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'laundry': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lift': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'num_floors': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_rooms': ('django.db.models.fields.IntegerField', [], {}),
            'other_amenities': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'parking': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'rent_pcm': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'satellite': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sauna': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
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
            'Meta': {'ordering': "('name',)", 'object_name': 'City'},
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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 2, 23, 7, 51, 0, 78594, tzinfo=utc)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 2, 23, 7, 51, 0, 78392, tzinfo=utc)'}),
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
