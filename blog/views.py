from petugas.models import Radiasi, Prediksi
from django.http import HttpResponse
from django.contrib import messages
from django.core import serializers
from django.shortcuts import render, redirect
from django.utils.html import format_html
from django.views.generic import TemplateView
import datetime
import json
from decimal import Decimal
import decimal

from os.path import join as os_join
from keras.models import load_model
from srfapp.settings import BASE_DIR
import numpy
import pandas
from joblib import load
from sklearn.metrics import mean_squared_error

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

# Create your views here.
def home(request):

    return render(request, 'blog/peramalan.html')

def apiForecasts(request):
    start = datetime.datetime(2017, 1, 1)
    end = datetime.datetime(2019, 12, 31)
    radiasi = Radiasi.objects.filter(tanggal__range=(start, end)).order_by('tanggal')
    prediksi = Prediksi.objects.filter(prediksitanggal__range=(start, end)).order_by('prediksitanggal')
    
    y_true, y_pred = [], []
    list_prediksi = []
    list_aktual = []
    field = {}
    for i in range(len(prediksi)):
        field={'tanggal':prediksi[i].prediksitanggal.strftime("%d-%m-%Y"), 'radiasi': prediksi[i].prediksiradiasi}
        list_prediksi.append(field)
        y_pred.append(prediksi[i].prediksiradiasi)
    for i in range(len(radiasi)):
        field={'tanggal':radiasi[i].tanggal.strftime("%d-%m-%Y"), 'radiasi': radiasi[i].radiasi}
        list_aktual.append(field)
        y_true.append(radiasi[i].radiasi)
    
    y_true = numpy.array(y_true).astype(numpy.float32)
    y_pred = numpy.array(y_pred).astype(numpy.float32)
    rmse = mean_squared_error(y_true, y_pred, squared=False)
    converted_rmse = getattr(rmse, "tolist", lambda: rmse)()

    res = {
        'rmse': converted_rmse,
        'data_actual': list_aktual,
        'data_prediction': list_prediksi,
    }
    return HttpResponse(json.dumps(res, cls=DecimalEncoder), content_type='application/json;charset=utf-8')

def apiForecastsFilter(request):
    request_tanggal = request.GET['tanggal']
    split_tanggal = request_tanggal.split(' s/d ')
    start = datetime.datetime.strptime(split_tanggal[0], "%d-%m-%Y")
    end = datetime.datetime.strptime(split_tanggal[1], "%d-%m-%Y")
    radiasi = Radiasi.objects.filter(tanggal__range=(start, end)).order_by('tanggal')
    prediksi = Prediksi.objects.filter(prediksitanggal__range=(start, end)).order_by('prediksitanggal')
    
    y_true, y_pred = [], []
    list_prediksi = []
    list_aktual = []
    field = {}
    for i in range(len(prediksi)):
        field={'tanggal':prediksi[i].prediksitanggal.strftime("%d-%m-%Y"), 'radiasi': prediksi[i].prediksiradiasi}
        list_prediksi.append(field)
        y_pred.append(prediksi[i].prediksiradiasi)
    for i in range(len(radiasi)):
        field={'tanggal':radiasi[i].tanggal.strftime("%d-%m-%Y"), 'radiasi': radiasi[i].radiasi}
        list_aktual.append(field)
        y_true.append(radiasi[i].radiasi)
    
    y_true = numpy.array(y_true).astype(numpy.float32)
    y_pred = numpy.array(y_pred).astype(numpy.float32)
    rmse = mean_squared_error(y_true, y_pred, squared=False)
    converted_rmse = getattr(rmse, "tolist", lambda: rmse)()

    res = {
        'rmse': converted_rmse,
        'data_actual': list_aktual,
        'data_prediction': list_prediksi,
    }

    return HttpResponse(json.dumps(res, cls=DecimalEncoder), content_type='application/json;charset=utf-8')

def dump_prediksi(request):
    scaler = load(os_join(BASE_DIR, "staticfiles/scaler.gz"))
    md19 = load_model(os_join(BASE_DIR, "staticfiles/MD19.h5"))
    radiasi = Radiasi.objects.filter(tanggal__range=('2016-12-16', '2019-12-31')).order_by('tanggal')

    list_radiasi = []
    list_tanggal = []
    for i in range(len(radiasi)):
        list_radiasi.append(radiasi[i].radiasi)
        if(i>15):
            list_tanggal.append(radiasi[i].tanggal)
    # flatten data
    
    data = numpy.array(list_radiasi).astype(numpy.float32)
    data = data.reshape(1, -1)
    data = scaler.transform(data)

    X, y = to_supervised(data[0], n_in=16, n_out=1)
    
    Y = md19.predict(X)
    
    Y = scaler.inverse_transform(Y)
    print(Y)
    converted_value = getattr(Y, "tolist", lambda: Y)()
    print(converted_value[0])
    round_converted_value = [ round(value[0], 2) for value in converted_value ]

    for i in range(len(list_tanggal)):
        Prediksi.objects.update_or_create(prediksitanggal=list_tanggal[i], defaults={'prediksiradiasi':round_converted_value[i]})

    return HttpResponse("halo")

def to_supervised(data, n_in, n_out):
    n_vars = 1
    df = pandas.DataFrame(data)
    cols, names = list(), list()
    # urutan waktu input ke t- (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
        
    # urutan waktu output ke t+ (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]          
    # concat
    agg = pandas.concat(cols, axis=1)
    agg.columns = names
    # drop baris yang bernilai Nan
    agg.dropna(inplace=True)
    val = agg.values
    X, y = val[:, 0:n_in], val[:, n_in:]
    #reshape(sample, timestep, feature/input)
    X = X.reshape((X.shape[0], 1, n_in))
    return X, y