'''
def login(request):
    context = {}
    template = ''
    lista = []
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
    
        cur = con.cursor()
        cur.execute("SELECT * FROM usuario WHERE username=%s and clave=%s ",(username,password))
        result = cur.fetchone()

        if result is not None:
            lista = list(result)

            message = 'Felicitaciones, Bienvenido a Dashboard APP'
            code = 1
            name = lista[4]
            template = 'upload/upload.html'
            context = {'message':message, 'code':code, 'name': name }
            print(context)
        else:
            message = 'Usuario no registrado'
            code = 2
            template = 'upload/index.html'
            context = {'message':message, 'code':code }
    else:
        message = 'Parametros no encontrados'
        code = 0
        template = 'upload/index.html'
        context = {'message':message, 'code':code }

    return render(request,template,context)
'''+

'''
print(name_file)
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            print(BASE_DIR)
            print(os.path.join(os.path.dirname(__file__)))
            print('dirname:     ', os.path.dirname(__file__))
            print('basename:    ', os.path.abspath(__file__))
            print(os.chdir(os.path.dirname(os.path.abspath(__file__))))
            print(pathlib.Path(__file__).parent.absolute())
'''