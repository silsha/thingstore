from django.conf.urls import patterns, url
from django.http import HttpResponse
from django.views.generic.base import View
from django.shortcuts import get_object_or_404
import json, csv
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt

from thingstore.models import Thing

class APIView(View):
	filetype = "json"

	@csrf_exempt
	def dispatch(self, *args, **kwargs):
		return super(APIView, self).dispatch(*args, **kwargs)
	
	def getJSON(self, request, **kwargs):
		pass
	
	def getCSV(self, request, **kwargs):
		pass

	def get(self, request, **kwargs):
		if self.filetype == "json":
			data = self.getJSON(request, **kwargs)
			return HttpResponse(data, content_type="application/json")
		elif self.filetype == "csv":
			data = self.getCSV(request, **kwargs)
			return HttpResponse(data, content_type="text/plain")

	def putJSON(self, request, **kwargs):
		pass
	
	def putCSV(self, request, **kwargs):
		pass

	def put(self, request, **kwargs):
		if self.filetype == "json":
			data = self.putJson(request, **kwargs)
			return HttpResponse(data, content_type="application/json")
		elif self.filetype == "csv":
			data = self.putCSV(request, **kwargs)
			return HttpResponse(data, content_type="text/plain")

class ThingAPI(APIView):
	def getJSON(self, request, **kwargs):
		thing = get_object_or_404(Thing, pk=kwargs["thing_id"])
		
		data = model_to_dict(thing)
		
		data['metrics'] = {}
		metrics = thing.metrics.all()
		for metric in metrics:
			data['metrics'][metric.name] = model_to_dict(metric,fields=['name','unit'])
			data['metrics'][metric.name]['current_value'] = metric.current_value
			data['metrics'][metric.name]['current_value'] = metric.current_value
		return json.dumps(data)
	
	def getCSV(self, request, **kwargs):
		thing = get_object_or_404(Thing, pk=kwargs["thing_id"])
		metrics = thing.metrics.all()
		data = ""
		for metric in metrics:
			data = "%s%s,%s\n" % (data, metric.name, metric.current_value)
		return data
		
	def putCSV(self, request, **kwargs):
		body = request.body
		lines = body.split('\n')
		data = []
		for line in lines:
			line_data = line.split(',')
			if len(line_data) != 2:
				return "ERROR\n"
			data.append(line_data)
		print data
		return "troet\n"
		
def metric(request):
	
	pass

urls = patterns('',
	url(r'^thing/(?P<thing_id>\w+).json', ThingAPI.as_view(filetype="json")),
	url(r'^thing/(?P<thing_id>\w+).csv', ThingAPI.as_view(filetype="csv")),
)
