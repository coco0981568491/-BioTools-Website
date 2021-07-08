from django.shortcuts import render, HttpResponse
from . import tool_funcs

# Create your views here.
def home(request):

	return render(request, 'home.html', {})
	
def findNPosPage(request):

	if request.method == "POST":

		# get data from input text (seq)
		seq = request.POST.get('seq')

		result = tool_funcs.findNPosBySequon(seq)
		resp = HttpResponse(result.getvalue(), content_type='application/force-download')
		resp['Content-Disposition'] = 'attachment; filename=NPosBySequon.xlsx'

		return resp

	else:
		return render(request, 'findNPos.html', {})


def aLPCutterPage(request):

	if request.method == "POST":

		# get data from input text (seq)
		seq = request.POST.get('seq')

		result = tool_funcs.alp_cutter(seq)
		resp = HttpResponse(result.getvalue(), content_type='application/force-download')
		resp['Content-Disposition'] = 'attachment; filename=aLPCutter.xlsx'

		return resp

	else:
		return render(request, 'aLPCutter.html', {})