from .forms import RadiasiForm
from .models import Radiasi
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.views.generic import TemplateView
import datetime
import json

# Create your views here.
class HomeView(TemplateView):

    template_name = 'petugas/beranda.html'
    context = {
        'title': 'Beranda',
        'radiasiForm': RadiasiForm(),
        'updateRadiasiForm': RadiasiForm(prefix='update'),
        'dateNow': datetime.date.today().strftime('%Y-%m-%d'),
    }

    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template_name, self.context)  

class LoginView(TemplateView):
    
    template_name = 'petugas/login.html'
    context = {
        'title': 'Log In',
    } 

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('petugas-home')
        return render(request, self.template_name, self.context)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('petugas-home')
            messages.error(request,'akun tidak aktif, hubungi staf IT')    
            return redirect('login')
        else:
            messages.error(request,'username/password salah')
            return redirect('login')

@login_required(redirect_field_name='petugas-home')
def logout(request):
    context = {
        'title': 'Log Out',
    }

    django_logout(request)

    return render(request, 'petugas/logout.html', context) 


def getDataRadiasi(request):
    object_list = Radiasi.objects.all().order_by('-idradiasi')
    serialized_objects  = serializers.serialize('json', object_list)
    json_objects = json.loads(serialized_objects)
    list_objects = []   
    for index in range(len(json_objects)):
        field = json_objects[index]['fields']
        field['pk'] = (json_objects[index]['pk'])
        list_objects.append(field)
    res = {
        'data': list_objects,
    }
    return HttpResponse(json.dumps(res), content_type='application/json;charset=utf-8')

def getDataRadiasiId(request):
    object_list = Radiasi.objects.filter(idradiasi=request.GET['pk'])
    serialized_objects  = serializers.serialize('json', object_list)
    json_objects = json.loads(serialized_objects)
    list_objects = []   
    for index in range(len(json_objects)):
        field = json_objects[index]['fields']
        field['pk'] = (json_objects[index]['pk'])
        list_objects.append(field)
    res = {
        'data': list_objects,
    }
    return HttpResponse(json.dumps(res), content_type='application/json;charset=utf-8')

def insertRadiasiBaru(request):
    if request.POST:
        tanggal = datetime.datetime.strptime(request.POST['tanggal'], "%d-%m-%Y")
        if(tanggal>datetime.datetime.now()):
            messages.error(request, 'Tanggal tidak diizinkan', extra_tags="danger")
            return redirect('petugas-home')
        tanggal = tanggal.strftime("%Y-%m-%d")
        isExist = Radiasi.objects.filter(tanggal=tanggal).first()
        if isExist:
            message = format_html("<span>{} {} {} </span><a id='messagedjango' href='javascript:void(0)' class='btn btn-info btn-sm item_edit' data-pk='{}' data-toggle='modal' data-target='#Modal_Edit'>{}</a>",
                      "Gagal! data tanggal", 
                      request.POST['tanggal'],
                      "sudah ada di database.",
                      isExist.pk,
                      "Edit?")
            messages.error(request, message, extra_tags="danger")
            return redirect("petugas-home")
        else:
            radiasiPost = None if request.POST['radiasi'] == '' else request.POST['radiasi']
            radiasi = Radiasi.objects.create(radiasi=radiasiPost, tanggal=tanggal)
            messages.success(request,"Berhasil! Data Radiasi tersimpan.", extra_tags="success")
            return redirect("petugas-home")
    return redirect('petugas-home')

def updateRadiasi(request):
    if request.POST:
        tanggal = datetime.datetime.strptime(request.POST['update-tanggal'], "%d-%m-%Y").strftime("%Y-%m-%d")
        isExist = Radiasi.objects.filter(tanggal=tanggal).first()
        if isExist:
            radiasiPost = None if request.POST['update-radiasi'] == '' else request.POST['update-radiasi']

            radiasi = Radiasi.objects.filter(idradiasi=request.POST['update-pk']).update(radiasi=radiasiPost)
            
            messages.success(request,"Berhasil! Data Radiasi diperbarui.", extra_tags="success")
            return redirect("petugas-home")
        else:
            message = format_html("<span>{} {} {} </span><a href='javascript:void(0)' class='btn btn-success btn-sm' data-toggle='modal' data-target='#Modal_Tambah'>{}</a>",
                      "Gagal! data tanggal", 
                      request.POST['update-tanggal'],
                      "tidak ada di database.",
                      "Tambah Baru?")
            messages.error(request, message, extra_tags="danger")
            return redirect("petugas-home")
    return redirect('petugas-home')