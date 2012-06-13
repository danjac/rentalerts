# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.utils.timezone import utc

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Search'
        db.create_table('alerts_search', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('email', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('num_rooms', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sauna', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('rent_pcm', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('size', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('non_shared', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('broadband', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('balcony', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('parking', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('laundry', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('alerts', ['Search'])

        # Adding M2M table for field areas on 'Search'
        db.create_table('alerts_search_areas', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('search', models.ForeignKey(orm['alerts.search'], null=False)),
            ('area', models.ForeignKey(orm['apartments.area'], null=False))
        ))
        db.create_unique('alerts_search_areas', ['search_id', 'area_id'])

        # Adding model 'Alert'
        db.create_table('alerts_alert', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('apartment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apartments.Apartment'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('alerts', ['Alert'])


    def backwards(self, orm):
        
        # Deleting model 'Search'
        db.delete_table('alerts_search')

        # Removing M2M table for field areas on 'Search'
        db.delete_table('alerts_search_areas')

        # Deleting model 'Alert'
        db.delete_table('alerts_alert')


    models = {
        'alerts.alert': {
            'Meta': {'object_name': 'Alert'},
            'apartment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apartments.Apartment']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'alerts.search': {
            'Meta': {'object_name': 'Search'},
            'areas': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['apartments.Area']", 'symmetrical': 'False', 'blank': 'True'}),
            'balcony': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'broadband': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'laundry': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'non_shared': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'num_rooms': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parking': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rent_pcm': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'sauna': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
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
            'deposit': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extra_storage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'floor': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'furniture': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'garage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'garden_size': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gym': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'heating': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_shared': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'kitchen_amenities': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 2, 22, 18, 57, 58, 46919, tzinfo=utc)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 2, 22, 18, 57, 58, 46704, tzinfo=utc)'}),
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

    complete_apps = ['alerts']
