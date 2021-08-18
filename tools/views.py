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

def findOPosPage(request):

	if request.method == "POST":

		# get data from input text (seq)
		seq = request.POST.get('seq')

		result = tool_funcs.findPotentialOPos(seq)
		resp = HttpResponse(result.getvalue(), content_type='application/force-download')
		resp['Content-Disposition'] = 'attachment; filename=OPosByST.xlsx'

		return resp

	else:
		return render(request, 'findOPos.html', {})

def GlycamToPDBPage(request):

	if request.method == "POST":

		# get data and name it as file for convenience 
		file = request.FILES["myFile"]

		result = tool_funcs.GlycamToPDB(file)
		resp = HttpResponse(result.getvalue(), content_type='application/force-download')
		resp['Content-Disposition'] = 'attachment; filename=GlycamToPDB.pdb'

		return resp

	else:
		return render(request, 'GlycamToPDB.html', {})

