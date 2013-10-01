from django.contrib import admin
from thingstore.models import Thing, Metric

class MetricInline(admin.TabularInline):
	model = Metric
	extra = 2
	
class ThingAdmin(admin.ModelAdmin):
	inlines = [MetricInline]
	list_display = ('name','owner')

admin.site.register(Thing, ThingAdmin)
