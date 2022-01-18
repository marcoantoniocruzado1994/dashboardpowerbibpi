from typing import Text
from django.shortcuts import render
from datetime import date
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

import random as rd
import pandas as pd
import psycopg2


con = psycopg2.connect(
        host="bpi-rpa-latam.cdw1gc4aj2db.us-east-1.rds.amazonaws.com",
        database="dashboard",
        user="postgres",
        password="IT0kYg53L56Mk3HYTZ4m",
        port="5432"
)

# HomePage
def home(request):
    return render(request,"upload/upload.html")


# Create your views here.
def loginPage(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            context = {'user':user}
            return render(request, 'upload/upload.html',context )
        else:
            messages.info(request, 'Username or Password is incorrect')
    return render(request, 'upload/index.html', context)

# Listar Sesiones
def sesiones(request):
    
    context = {}
    dia_actual = 0
    code = 0
   
    try:
        today = date.today()
        dia_actual = today.day-1
        mes_actual = today.month
        anio_actual = today.year
        if dia_actual < 10:
            dia_actual = '0'+str(dia_actual)
        else:
            dia_actual = dia_actual

        fecha_actual = str(anio_actual) + '-'+ str(mes_actual)+'-'+str(dia_actual)+' %'
        fecha_head = str(dia_actual) + '/'+ str(mes_actual)+'/'+str(anio_actual)

        cur = con.cursor()
        cur.execute("SELECT DISTINCT session_id FROM dashboard_bpi WHERE created_at like '{}' ".format(fecha_actual))
        sesiones = cur.fetchall()
        if len(sesiones) > 0:
            message = 'Lista de sesiones del '+fecha_head
            code = 1
            context = {'message':message,'sesiones':sesiones,'code':code,'fecha':fecha_head}

        else:
            message = 'No hay sesiones para el '+fecha_head
            code = 0
            context = {'message':message,'code':code}
    except:
        message = 'No hay sesiones'
        code = 0
        context = {'message':message,'code':code}
    return render(request,"upload/sessiones.html",context)

# lista de sesiones RANDOM
def sesiones_random(request):
   
    data = {}
    dia_actual = 0
    code = 0
  

    try:
        today = date.today()
        dia_actual = today.day - 2
        mes_actual = today.month
        anio_actual = today.year
        if dia_actual < 10:
            dia_actual = '0'+str(dia_actual)
        else:
            dia_actual = today.day - 1

        fecha_actual = str(anio_actual) + '-'+ str(mes_actual)+'-'+str(dia_actual)+' %'

        cur = con.cursor()
        cur.execute("SELECT DISTINCT session_id FROM dashboard_bpi WHERE created_at like '{}' ".format(fecha_actual))
        final_result = [i[0] for i in cur.fetchall()]

        sesiones_random = rd.sample(final_result, k = 8)
        
        data['sesiones'] = sesiones_random
        #envio de correo
        
    except:
        message = 'No hay sesiones'
        code = 0
        data = {'message':message,'code':code}
    return JsonResponse(data, safe=False)


# Subir archivo CSV
def upload(request):
    message = ''
    code = 0
    fs = FileSystemStorage()
    try:
        if request.method == "POST":
            upload_file = request.FILES['file']

            fs.save(upload_file.name,upload_file)

            name_file = str(upload_file)

            df = pd.read_csv(r'media/' + name_file, encoding='latin-1',sep=';')
            df = df.fillna('')
            df = df.to_numpy().tolist()
            lista = list (df)

            tuplaa = tuple(lista)

            cur = con.cursor()

            cur.executemany('''INSERT INTO dashboard_powerbi 
            (id,created_at,name_one,name_platform,text_in,text_out,intent_name,session_id,
            client_phone,phone,name_two,user_name,name_treee,last_name,metadata) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',tuplaa)
            
            if cur.rowcount > 0:
                fs.delete(upload_file.name)
                con.commit()
                message = 'Carga de archivo exitosa!!'
                code = 1
            else:
                fs.delete(upload_file.name)
                message = 'Carga de archivo erronea!!'
                code = 0
        else:
            message = 'No se reconoce parametros en el metodo POST'
            code = 0

    except:
        fs.delete(upload_file.name)
        message = 'El archivo no tiene el formato correcto o la ubicación raíz es diferente!!'
        code = 0

    return render(request, "upload/result.html", {'message': message,'code':code})

