import xml.etree.ElementTree as ET
from datetime import datetime

def id_creator(tag,id): #Se encarga de crear y asignar los ID a las notas
    tag.set('id',str(id))

def personal_creator(cat1): #Crea las notas de la categoría Personales
    categoria = ET.SubElement(cat1, 'personal')
    if len(cat1) == 0:  #Este condicional se asegura de que nunca se cree un ID que ya existe
        identificador = 0
    else:
        identificador = len(cat1)
    id_creator(categoria,identificador)
    titulo = ET.SubElement(categoria, 'titulo')
    titulo.text = input("Introduce el título de la nota: ") 
    contenido = ET.SubElement(categoria, 'contenido')
    contenido.text = input("Ya puedes comenzar a escribir tu nota!! \n")
    fecha = ET.SubElement(categoria,'fecha')
    fecha.text = datetime.today().strftime('%d/%m/%Y') #Esta variable tiene como valor la fecha actual del sistema
    favorito = ET.SubElement(categoria,'favoritos')
    favorito.text = "false"

def profesional_creator(cat2): #Crea las notas de la categoría Profesional
    categoria = ET.SubElement(cat2, 'profesional')
    if len(cat2) == 0: #Este condicional se asegura de que nunca se cree un ID que ya existe
        identificador = 0
    else:
        identificador = len(cat2)
    id_creator(categoria,identificador)
    proyecto = ET.SubElement(categoria, 'proyecto')
    proyecto.text = input("Introduce el nombre del proyecto: ")
    departamento = ET.SubElement(categoria, 'departamento')
    departamento.text = input('Introduce el nombre del departamento: ')
    empresa = ET.SubElement(categoria, 'empresa')
    empresa.text = input('Introduce el nombre de la empresa: ')
    entrega = ET.SubElement(categoria, 'fechaentrega')
    fecha = input('Introduce la fecha de entrega en el siguiente formato dd/mm/AAAA: ')
    if datetime.strptime(fecha, '%d/%m/%Y'): #Este condicional comprueba que la fecha introducida es del formato correcto, en caso de no serlo lanza la exepción
        entrega.text = fecha

def domestica_creator(cat3): #Crea las notas de la categoría Tareas Domésticas
    categoria = ET.SubElement(cat3, 'tareadomestica')
    if len(cat3) == 0: #Este condicional se asegura de que nunca se cree un ID que ya existe
        identificador = 0
    else:
        identificador = len(cat3)
    id_creator(categoria,identificador)
    tituloTarea = ET.SubElement(categoria, 'titulotarea')
    tituloTarea.text = input('Introduce el titulo de la tarea: ')
    check = ET.SubElement(categoria, 'check')
    check.text = 'false'
    prioridad = ET.SubElement(categoria, 'prioridad')
    prior = input('Introduce una de las siguientes prioridades:\n Alta\n Media\n Baja \n').lower() #Reduciendo toda la string a minúscula evito posibles errores
    if prior != 'alta' and prior != 'baja' and prior != 'media': #Este condicional comprueba que ha introducido una de las tres opciones
        raise ValueError
    prioridad.text = prior.capitalize()

def new_note(cat1,cat2,cat3): #Esta función es la encargada de permitir al usuario crear una nueva nota de la categoría que quiera
    print('Personal: Introduce 1 \n Profesional: Introduce 2 \n Tarea Doméstica: Introduce 3')
    categoria = int(input("Introduce la categoría de la nueva nota: "))
    if categoria == 1:
        personal_creator(cat1)
    elif categoria == 2:
        profesional_creator(cat2)
    elif categoria == 3:
        domestica_creator(cat3)
    else:
        raise ValueError



def show_all(archivo): #Esta función es la encarga de mostrar todas las notas guardadas
    for categoria in archivo:
        print('\nNotas ' +categoria.tag + ':')
        for nota in categoria: #Según la categoria, el nombre de las etiquetas serán unas u otras
            if categoria.tag == 'personales':
                print('\nID: '+ nota.attrib['id'])
                print('Título: '+ nota[0].text)
                print('Fecha: '+nota[2].text)
                print('Contenido: '+nota[1].text)
                if nota[3].text == 'false':
                    print('☆')
                else:
                    print('★')
            if categoria.tag == 'profesionales':
                print('\nID: '+ nota.attrib['id'])
                print('Proyecto: '+nota[0].text)
                print('Departamento: '+nota[1].text)
                print('Empresa: '+nota[2].text)
                print('Fecha de Entrega: '+nota[3].text)
            if categoria.tag == 'tareasdomesticas':
                print('\nID: '+ nota.attrib['id'])
                print('Titulo de la Tarea: '+nota[0].text)
                if nota[1].text == 'false':
                    print('□')
                else:
                    print('☑')
                print('Prioridad: '+nota[2].text)

def modify(categoria, identificador): #Esta función se encarga de permitir modificar notas guardadas al usuario mediante la categoría y el id de la nota a modificar
    contador = 0
    for nota in categoria:
        if nota.attrib['id'] == identificador:
            print('Para modificar los siguientes campos introduce los números que se indican')
            for elemento in nota:
                print(elemento.tag +' -> '+ str(contador))
                if elemento.tag == 'favoritos' or elemento.tag == 'check':
                    print('Los campos Favoritos y Check solo pueden tener el valor: true o false')
                contador+=1
            accion = int(input())
            if accion>contador:
                raise ValueError
            else:
                if nota[accion].tag == 'favoritos' or nota[accion].tag == 'check':
                    valor = input('En este campo solo puedes introducir: true o false \n')
                    if valor != 'false' and valor != 'true':
                        raise ValueError
                    else:
                        nota[accion].text = valor
                elif nota[accion].tag == 'fecha' or nota[accion].tag == 'fechaentrega':
                    fecha = input('En este campo solo se admiten fechas con el siguiente formato DD/MM/AAAA: ')
                    if datetime.strptime(fecha, '%d/%m/%Y'):
                        nota[accion].text = fecha
                else:
                    nota[accion].text = input('El contenido del campo seleccionado ha sido borrado, introduzca el nuevo contenido \n')

def comprobar_ID(categoria, identificador): #Esta función se encarga de comprobar que el id introducido pertenece a una nota guardada
    if int(identificador) > len(categoria):
        print('Has introducido un ID que no corresponde a ninguna nota')
        return False
    else:
        return True        

def search(archivo): #Esta función es la encargada de buscar el contenido introducido en las notas guardadas
    busqueda = input('Introduce la palabra o frase que buscas: ')
    encontrada = False
    for categoria in archivo:
        for nota in categoria:
            for elemento in nota:
                if busqueda in elemento.text:
                    encontrada = True
                    print('La palabra o frase buscada se encuenta en la siguiente nota:')
                    print('Categoria: '+ categoria.tag)
                    if categoria.tag == 'personales':
                        print('ID: '+ nota.attrib['id'])
                        print('Título: '+ nota[0].text)
                        print('Fecha: '+nota[2].text)
                        print('Contenido: '+nota[1].text)
                        if nota[3].text == 'false':
                            print('☆')
                        else:
                            print('★')
                    if categoria.tag == 'profesionales':
                        print('ID: '+ nota.attrib['id'])
                        print('Proyecto: '+nota[0].text)
                        print('Departamento: '+nota[1].text)
                        print('Empresa: '+nota[2].text)
                        print('Fecha de Entrega: '+nota[3].text)
                    if categoria.tag == 'tareasdomesticas':
                        print('ID: '+ nota.attrib['id'])
                        print('Titulo de la Tarea: '+nota[0].text)
                        if nota[1].text == 'false':
                            print('□')
                        else:
                            print('☑')
                        print('Prioridad: '+nota[2].text)
    if encontrada == False:
        print('La palabra o frase introducida no se ha encontrado en ninguna de las notas guardadas')




if __name__ == "__main__":
    try:
        tree = ET.parse('notes.xml') #Lee el archivo xml
        raiz = tree.getroot() #Obtiene la raíz del archivo xml gracias a la cual vamos a recorrerlo sin problemas
        personales = raiz[0]
        profesionales = raiz[1]
        tareasDomesticas = raiz[2]
        print('Bienvenido/a a la app de notas \n Introduce uno de los siguientes números según lo que quieras hacer: \n Para mostrar todas las notas: 0 \n Para crear una nueva nota: 1 \n Para modificar una nota ya existente: 2 \n Para buscar una frase o palabra entre las notas guardadas: 3')
        accion = int(input())
        if accion == 0:
            show_all(raiz)
        if accion == 1:
            new_note(personales,profesionales,tareasDomesticas)
        if accion == 2:
            categoria = int(input('Introduce el número correspondiente a la categoría a la que pertenece la nota que desea modificar: \n Personal -> 0 \n Profesional -> 1 \n Tarea Doméstica -> 2\n'))
            identificador = input('Introduce el ID de la nota que desea modificar: ')
            if categoria == 0:
                if comprobar_ID(personales,identificador):
                    modify(personales, identificador)
            elif categoria == 1:
                if comprobar_ID(profesionales,identificador):
                    modify(profesionales,identificador)
            elif categoria == 2:
                if comprobar_ID(profesionales,identificador):
                    modify(tareasDomesticas,identificador)
            else:
                raise ValueError
        if accion == 3:
            search(raiz)

        mydata = ET.tostring(raiz, encoding='unicode') #Pasa todo el árbol xml a string para sobreescribirlo
        myfile = open("notes.xml", "w") #Abre el archivo XML
        myfile.write(str(mydata)) #Sobreescribe el archivo XML
        myfile.close #Cierra el archivo XML
    except ValueError:
        print("Has introducido un valor no válido")