from django.contrib.auth.models import Permission
from django.test import TestCase
import unittest
from random import randrange
from django.test import Client, TestCase
import Sprints
from GestionPermisos.forms import *
from Sprints.forms import *
from Sprints.models import Sprint
from gestionUsuario.forms import *
from proyectos.forms import *
from proyectos.models import Proyecto
from userStory.forms import *
from userStory.models import Historia


class TestForms(unittest.TestCase):

    def setUp(self):

        self.proyecto = Proyecto.objects.create(
            nombre='Primer Proyecto',
            descripcion='Proyecto de prueba',
            estado='PENDIENTE',
            fecha='2021-07-25',
            fecha_entrega='2021-07-26'
        )

        self.sprints = Sprint.objects.create(
            sprintNumber=5,
            fecha_inicio='2021-09-16',
            fecha_fin='2021-09-20'
        )

        self.historias = Historia.objects.create(
            nombre='Primer Proyecto',
            descripcion='Proyecto de prueba',
            prioridad='ALTA',
            fecha_creacion='2021-07-25',
            horasEstimadas=15,
            estados='pendiente',
            horas_dedicadas=24,
            comentarios='comentario de prueba',
        )

        self.estados=(
            (True,"Habilitar acceso al sistema"),
            (False,"Restringir acceso al sistema"),
        )

        self.OPTIONS = (
            ("add", "Agregar"),
            ("delete", "Borrar"),
            ("change","Modificar"),
            ("view","Ver"),
        )

        self.valid1 = 302

        self.proyecto1 = Proyecto.objects.create(
            nombre='Segundo Proyecto',
            descripcion='Proyecto de prueba 2',
            estado='PENDIENTE',
            fecha='2021-07-24',
            fecha_entrega='2021-07-29'
        )

        self.valid = 200

        self.invalid = 404

    def test_crearRolForm(self):

        form = crearRolForm(
         data={
            'RolName':'New rol',
        })

        self.assertTrue(form.is_valid())


    def test_asignarRolForm(self):

        c = Client()
        res = c.post('/asignarRol/2/', {'Usuario': 'Cristhian', 'Roles': 'Scrum Master'})

        self.assertEquals(res.status_code, self.valid1)


    def test_seleccionarRolForm(self):

        c = Client()
        res = c.post('/modificarRol/2/', {'Rol': 'Scrum Master'})

        self.assertEquals(res.status_code, self.valid1)


    def test_modificarRolForm(self):

        c = Client()
        res = c.post('/modificarRol/3/', {'RolName': 'Scrum Master'})

        self.assertEquals(res.status_code, self.valid1)


    def test_crearUsuarioForm(self):
        form = crearUsuarioForm(data={
            'Nombre':'Juan',
            'correo':'juan3@gmail.com'
        })

        self.assertTrue(form.is_valid())


    def test_registroDeUsuariosForm1(self):

        c = Client()
        res = c.get('/registrarUsuario/', {'Usuario':'Cristhian', 'Habilitado':'true'})

        self.assertEquals(res.status_code, self.valid1)


    def test_asignarcapacidadForm(self):

        c = Client()
        res = c.get('/registrarUsuario/', {'Usuario':'Cristhian', 'Habilitado':'true'})

        self.assertEquals(res.status_code, self.valid1)


    def test_asignarCapacidadForm(self):

        form = asignarcapacidadForm({
            'capacidad':14
        })

        self.assertTrue(form.is_valid())

    def test_crearproyectoForm(self):

        c = Client()
        res = c.get('/proyecto/nuevo/',
                    {'nombre':'Proyecto1',
                     'descripcion': 'Proyecto de prueba 1',
                     'estado': 'Pendiente',
                     'fecha': 2021/ 10/30,
                     'fecha_entrega': 2021/11/0o3,
                     'miembros': ('Edher', 'Cynthia'),
                    })

        self.assertEquals(res.status_code, self.valid1)


    def test_modificarproyectoForm(self):

        c = Client()
        res = c.get('/proyecto/1/modificar/',
                    {'id':1,
                     'nombre':'Proyecto1',
                     'descripcion': 'Proyecto de prueba 1',
                     'estado': 'Pendiente',
                     'fecha': 2021/ 10/30,
                     'fecha_entrega': 2021/11/0o3,
                     'miembros': ('Cynthia'),
                     'usuarios': ('Edher','Mady','Milena')
                    })

        self.assertEquals(res.status_code, self.valid1)

    def test_seleccionarproyectoForm(self):
        c = Client()
        res = c.get('/modificarRol/1/',
                    {'Proyecto': self.proyecto,
                     })

        self.assertEquals(res.status_code, self.valid1)


    def test_importarRolForm(self):
        c = Client()
        res = c.get('/modificarRol/1/',
                    {'ProyectoA': self.proyecto,
                     'ProyectoB': self.proyecto1,
                     })

        self.assertEquals(res.status_code, self.valid1)


    def test_crearsprintForm(self):

        c = Client()

        r = c.get('/proyecto/1/Sprints/nuevo/InformacionBasica/',
                    {'id':1,
                     'sprintNumber':1,
                     'rango': '[ 2021/11/02 - 2021/11/02 ]',
                     'fecha_inicio': 2021/ 10/27,
                     'fecha_fin': 2021/11/0o1,
                    })

        self.assertEquals(r.status_code, self.valid1)


    def test_modificarsprintForm(self):

        c = Client()

        r = c.get('/proyecto/nuevo/',
                    {'id':1,
                     'proyecto': 2,
                     'sprintNumber':1,
                     'rango': '[ 2021/11/02 - 2021/11/02 ]',
                     'fecha_inicio': 2021/ 10/27,
                     'fecha_fin': 2021/11/0o5,
                    })

        self.assertEquals(r.status_code, self.valid1)


    def test_visualizarsprintForm(self):

        c = Client()

        r = c.get('/proyecto/nuevo/',
                    {'id':1,
                     'proyecto': 2,
                     'sprintNumber':1,
                     'fecha_inicio': 2021/ 10/27,
                     'fecha_fin': 2021/11/0o5,
                     'historias': self.historias
                    })

        self.assertEquals(r.status_code, self.valid1)


    def test_extendersprintForm(self):

        c = Client()

        r = c.get('/proyecto/1/Sprints/',
                    {
                     'fecha_fin': 2021/11/0o6,
                    })

        self.assertEquals(r.status_code, self.valid1)


    def test_intercambiardeveloperForm(self):

        c = Client()

        r = c.get('/proyecto/1/Sprints/2/intercambiar/',
                    {
                     'miembroA': User.objects.filter(),
                     'miembroB': User.objects.filter()
                    })

        self.assertEquals(r.status_code, self.valid1)


    def test_crearHistoriaForm(self):

        c = Client()
        res = c.get('/proyecto/1/ProductBacklog/nuevo/',
                    {'nombre':'Historia Nro1',
                     'descripcion': 'Historia de prueba 1',
                     'prioridad': 'Alta',
                     'fecha_creacion': 2021/ 10/30,
                     'proyecto':1,
                     })

        self.assertEquals(res.status_code, self.valid1)


    def test_cargarHorasHistoriaForm(self):

        c = Client()
        res = c.get('proyecto/1/Sprints/1/KanbanActivo/Historia1/Op5',
                    {
                     'horas':6,
                     'comentario': 'comentario de prueba',
                     })

        self.assertEquals(res.status_code, self.invalid)


    def test_seleccionarHistoriaForm(self):

        c = Client()

        res = c.get('modificarHistoria/1/',
                    {
                     'Historia': self.historias,
                    })

        self.assertEquals(res.status_code, self.invalid)



    def test_asignarEncargadoForm(self):

        c = Client()

        res = c.get('asignarEncargado/',
                    {
                     'Usuario': User.objects.filter(),
                     'Historia': self.historias,
                    })

        self.assertEquals(res.status_code, self.invalid)



    def test_modificarHistoriaForm(self):

        c = Client()

        res = c.get('proyecto/1/ProductBacklog/modificar/Historia1/',
                    {'nombre':'Historia Nro1',
                     'descripcion': 'Historia de prueba 1',
                     'prioridad': 'Baja',
                     })

        self.assertEquals(res.status_code, self.invalid)


    def test_eliminarHistoriaForm(self):

        c = Client()

        res = c.get('proyecto/1/ProductBacklog/Eliminar/Historia1/',
                    {
                     'Historia': self.historias,
                    })

        self.assertEquals(res.status_code, self.invalid)



    def test_asignaryestimarHistoriaForm(self):

        c = Client()

        res = c.get('proyecto/1/Sprints/2/AsignarHistorias/',
                    {
                     'encargado': User.objects.all(),
                     'estimado':27
                    })

        self.assertEquals(res.status_code, self.invalid)


    def test_crearRolForms(self):

        form = crearRolForm(
         data={
            'RolName':'New rol',
        })

        self.assertTrue(form.is_valid())


    def test_asignarRolForms(self):

        c = Client()
        res = c.post('/asignarRol/2/', {'Usuario': 'Cristhian', 'Roles': 'Scrum Master'})

        self.assertEquals(res.status_code, self.valid1)


    def test_seleccionarRolForms(self):

        c = Client()
        res = c.post('/modificarRol/2/', {'Rol': 'Scrum Master'})

        self.assertEquals(res.status_code, self.valid1)


    def test_modificarRolForms(self):

        c = Client()
        res = c.post('/modificarRol/3/', {'RolName': 'Scrum Master'})

        self.assertEquals(res.status_code, self.valid1)


    def test_crearUsuarioForms(self):
        form = crearUsuarioForm(data={
            'Nombre':'Juan',
            'correo':'juan3@gmail.com'
        })

        self.assertTrue(form.is_valid())


    def test_registroDeUsuariosForms1(self):

        c = Client()
        res = c.get('/registrarUsuario/', {'Usuario':'Cristhian', 'Habilitado':'true'})

        self.assertEquals(res.status_code, self.valid1)


    def test_asignarcapacidadForms(self):

        c = Client()
        res = c.get('/registrarUsuario/', {'Usuario':'Cristhian', 'Habilitado':'true'})

        self.assertEquals(res.status_code, self.valid1)


    def test_asignarCapacidadForms(self):

        form = asignarcapacidadForm({
            'capacidad':14
        })

        self.assertTrue(form.is_valid())

    def test_crearproyectoForms(self):

        c = Client()
        res = c.get('/proyecto/nuevo/',
                    {'nombre':'Proyecto1',
                     'descripcion': 'Proyecto de prueba 1',
                     'estado': 'Pendiente',
                     'fecha': 2021/ 10/30,
                     'fecha_entrega': 2021/11/0o3,
                     'miembros': ('Edher', 'Cynthia'),
                    })

        self.assertEquals(res.status_code, self.valid1)


    def test_modificarproyectoForms(self):

        c = Client()
        res = c.get('/proyecto/1/modificar/',
                    {'id':1,
                     'nombre':'Proyecto1',
                     'descripcion': 'Proyecto de prueba 1',
                     'estado': 'Pendiente',
                     'fecha': 2021/ 10/30,
                     'fecha_entrega': 2021/11/0o3,
                     'miembros': ('Cynthia'),
                     'usuarios': ('Edher','Mady','Milena')
                    })

        self.assertEquals(res.status_code, self.valid1)

    def test_seleccionarproyectoForms(self):
        c = Client()
        res = c.get('/modificarRol/1/',
                    {'Proyecto': self.proyecto,
                     })

        self.assertEquals(res.status_code, self.valid1)


    def test_importarRolForms(self):
        c = Client()
        res = c.get('/modificarRol/1/',
                    {'ProyectoA': self.proyecto,
                     'ProyectoB': self.proyecto1,
                     })

        self.assertEquals(res.status_code, self.valid1)


    def test_crearsprintForms(self):

        c = Client()

        r = c.get('/proyecto/1/Sprints/nuevo/InformacionBasica/',
                    {'id':1,
                     'sprintNumber':1,
                     'rango': '[ 2021/11/02 - 2021/11/02 ]',
                     'fecha_inicio': 2021/ 10/27,
                     'fecha_fin': 2021/11/0o1,
                    })

        self.assertEquals(r.status_code, self.valid1)


    def test_modificarsprintForms(self):

        c = Client()

        r = c.get('/proyecto/nuevo/',
                    {'id':1,
                     'proyecto': 2,
                     'sprintNumber':1,
                     'rango': '[ 2021/11/02 - 2021/11/02 ]',
                     'fecha_inicio': 2021/ 10/27,
                     'fecha_fin': 2021/11/0o5,
                    })

        self.assertEquals(r.status_code, self.valid1)


    def test_visualizarsprintForms(self):

        c = Client()

        r = c.get('/proyecto/nuevo/',
                    {'id':1,
                     'proyecto': 2,
                     'sprintNumber':1,
                     'fecha_inicio': 2021/ 10/27,
                     'fecha_fin': 2021/11/0o5,
                     'historias': self.historias
                    })

        self.assertEquals(r.status_code, self.valid1)


    def test_extendersprintForms(self):

        c = Client()

        r = c.get('/proyecto/1/Sprints/',
                    {
                     'fecha_fin': 2021/11/0o6,
                    })

        self.assertEquals(r.status_code, self.valid1)


    def test_intercambiardeveloperForms(self):

        c = Client()

        r = c.get('/proyecto/1/Sprints/2/intercambiar/',
                    {
                     'miembroA': User.objects.filter(),
                     'miembroB': User.objects.filter()
                    })

        self.assertEquals(r.status_code, self.valid1)


    def test_crearHistoriaForms(self):

        c = Client()
        res = c.get('/proyecto/1/ProductBacklog/nuevo/',
                    {'nombre':'Historia Nro1',
                     'descripcion': 'Historia de prueba 1',
                     'prioridad': 'Alta',
                     'fecha_creacion': 2021/ 10/30,
                     'proyecto':1,
                     })

        self.assertEquals(res.status_code, self.valid1)


    def test_cargarHorasHistoriaForms(self):

        c = Client()
        res = c.get('proyecto/1/Sprints/1/KanbanActivo/Historia1/Op5',
                    {
                     'horas':6,
                     'comentario': 'comentario de prueba',
                     })

        self.assertEquals(res.status_code, self.invalid)


    def test_seleccionarHistoriaForms(self):

        c = Client()

        res = c.get('modificarHistoria/1/',
                    {
                     'Historia': self.historias,
                    })

        self.assertEquals(res.status_code, self.invalid)



    def test_asignarEncargadoForms(self):

        c = Client()

        res = c.get('asignarEncargado/',
                    {
                     'Usuario': User.objects.filter(),
                     'Historia': self.historias,
                    })

        self.assertEquals(res.status_code, self.invalid)



    def test_modificarHistoriaForms(self):

        c = Client()

        res = c.get('proyecto/1/ProductBacklog/modificar/Historia1/',
                    {'nombre':'Historia Nro1',
                     'descripcion': 'Historia de prueba 1',
                     'prioridad': 'Baja',
                     })

        self.assertEquals(res.status_code, self.invalid)


    def test_eliminarHistoriaForms(self):

        c = Client()

        res = c.get('proyecto/1/ProductBacklog/Eliminar/Historia1/',
                    {
                     'Historia': self.historias,
                    })

        self.assertEquals(res.status_code, self.invalid)



    def test_asignaryestimarHistoriaForms(self):

        c = Client()

        res = c.get('proyecto/1/Sprints/2/AsignarHistorias/',
                    {
                     'encargado': User.objects.all(),
                     'estimado':27
                    })

        self.assertEquals(res.status_code, self.invalid)


    def test_crearRolForms1(self):

        form = crearRolForm(
         data={
            'RolName':'New rol',
        })

        self.assertTrue(form.is_valid())


    def test_asignarRolForms1(self):

        c = Client()
        res = c.post('/asignarRol/2/', {'Usuario': 'Cristhian', 'Roles': 'Scrum Master'})

        self.assertEquals(res.status_code, self.valid1)


    def test_seleccionarRolForms1(self):

        c = Client()
        res = c.post('/modificarRol/2/', {'Rol': 'Scrum Master'})

        self.assertEquals(res.status_code, self.valid1)


    def test_modificarRolForms1(self):

        c = Client()
        res = c.post('/modificarRol/3/', {'RolName': 'Scrum Master'})

        self.assertEquals(res.status_code, self.valid1)


    def test_crearUsuarioForms1(self):
        form = crearUsuarioForm(data={
            'Nombre':'Juan',
            'correo':'juan3@gmail.com'
        })

        self.assertTrue(form.is_valid())


    def test_registroDeUsuariosForms2(self):

        c = Client()
        res = c.get('/registrarUsuario/', {'Usuario':'Cristhian', 'Habilitado':'true'})

        self.assertEquals(res.status_code, self.valid1)


    def test_asignarcapacidadForms1(self):

        c = Client()
        res = c.get('/registrarUsuario/', {'Usuario':'Cristhian', 'Habilitado':'true'})

        self.assertEquals(res.status_code, self.valid1)


    def test_asignarCapacidadForms1(self):

        form = asignarcapacidadForm({
            'capacidad':14
        })

        self.assertTrue(form.is_valid())

    def test_crearproyectoForms1(self):

        c = Client()
        res = c.get('/proyecto/nuevo/',
                    {'nombre':'Proyecto1',
                     'descripcion': 'Proyecto de prueba 1',
                     'estado': 'Pendiente',
                     'fecha': 2021/ 10/30,
                     'fecha_entrega': 2021/11/0o3,
                     'miembros': ('Edher', 'Cynthia'),
                    })

        self.assertEquals(res.status_code, self.valid1)


    def test_modificarproyectoForms1(self):

        c = Client()
        res = c.get('/proyecto/1/modificar/',
                    {'id':1,
                     'nombre':'Proyecto1',
                     'descripcion': 'Proyecto de prueba 1',
                     'estado': 'Pendiente',
                     'fecha': 2021/ 10/30,
                     'fecha_entrega': 2021/11/0o3,
                     'miembros': ('Cynthia'),
                     'usuarios': ('Edher','Mady','Milena')
                    })

        self.assertEquals(res.status_code, self.valid1)

    def test_seleccionarproyectoForms1(self):
        c = Client()
        res = c.get('/modificarRol/1/',
                    {'Proyecto': self.proyecto,
                     })

        self.assertEquals(res.status_code, self.valid1)


    def test_importarRolForms1(self):
        c = Client()
        res = c.get('/modificarRol/1/',
                    {'ProyectoA': self.proyecto,
                     'ProyectoB': self.proyecto1,
                     })

        self.assertEquals(res.status_code, self.valid1)


    def test_crearsprintForms1(self):

        c = Client()

        r = c.get('/proyecto/1/Sprints/nuevo/InformacionBasica/',
                    {'id':1,
                     'sprintNumber':1,
                     'rango': '[ 2021/11/02 - 2021/11/02 ]',
                     'fecha_inicio': 2021/ 10/27,
                     'fecha_fin': 2021/11/0o1,
                    })

        self.assertEquals(r.status_code, self.valid1)


    def test_modificarsprintForms1(self):

        c = Client()

        r = c.get('/proyecto/nuevo/',
                    {'id':1,
                     'proyecto': 2,
                     'sprintNumber':1,
                     'rango': '[ 2021/11/02 - 2021/11/02 ]',
                     'fecha_inicio': 2021/ 10/27,
                     'fecha_fin': 2021/11/0o5,
                    })

        self.assertEquals(r.status_code, self.valid1)


    def test_visualizarsprintForms1(self):

        c = Client()

        r = c.get('/proyecto/nuevo/',
                    {'id':1,
                     'proyecto': 2,
                     'sprintNumber':1,
                     'fecha_inicio': 2021/ 10/27,
                     'fecha_fin': 2021/11/0o5,
                     'historias': self.historias
                    })

        self.assertEquals(r.status_code, self.valid1)


    def test_extendersprintForms1(self):

        c = Client()

        r = c.get('/proyecto/1/Sprints/',
                    {
                     'fecha_fin': 2021/11/0o6,
                    })

        self.assertEquals(r.status_code, self.valid1)


    def test_intercambiardeveloperForms1(self):

        c = Client()

        r = c.get('/proyecto/1/Sprints/2/intercambiar/',
                    {
                     'miembroA': User.objects.filter(),
                     'miembroB': User.objects.filter()
                    })

        self.assertEquals(r.status_code, self.valid1)


    def test_crearHistoriaForms1(self):

        c = Client()
        res = c.get('/proyecto/1/ProductBacklog/nuevo/',
                    {'nombre':'Historia Nro1',
                     'descripcion': 'Historia de prueba 1',
                     'prioridad': 'Alta',
                     'fecha_creacion': 2021/ 10/30,
                     'proyecto':1,
                     })

        self.assertEquals(res.status_code, self.valid1)


    def test_cargarHorasHistoriaForms1(self):

        c = Client()
        res = c.get('proyecto/1/Sprints/1/KanbanActivo/Historia1/Op5',
                    {
                     'horas':6,
                     'comentario': 'comentario de prueba',
                     })

        self.assertEquals(res.status_code, self.invalid)


    def test_seleccionarHistoriaForms1(self):

        c = Client()

        res = c.get('modificarHistoria/1/',
                    {
                     'Historia': self.historias,
                    })

        self.assertEquals(res.status_code, self.invalid)



    def test_asignarEncargadoForms1(self):

        c = Client()

        res = c.get('asignarEncargado/',
                    {
                     'Usuario': User.objects.filter(),
                     'Historia': self.historias,
                    })

        self.assertEquals(res.status_code, self.invalid)



    def test_modificarHistoriaForms1(self):

        c = Client()

        res = c.get('proyecto/1/ProductBacklog/modificar/Historia1/',
                    {'nombre':'Historia Nro1',
                     'descripcion': 'Historia de prueba 1',
                     'prioridad': 'Baja',
                     })

        self.assertEquals(res.status_code, self.invalid)


    def test_eliminarHistoriaForms1(self):

        c = Client()

        res = c.get('proyecto/1/ProductBacklog/Eliminar/Historia1/',
                    {
                     'Historia': self.historias,
                    })

        self.assertEquals(res.status_code, self.invalid)



    def test_asignaryestimarHistoriaForms1(self):

        c = Client()

        res = c.get('proyecto/1/Sprints/2/AsignarHistorias/',
                    {
                     'encargado': User.objects.all(),
                     'estimado':27
                    })

        self.assertEquals(res.status_code, self.invalid)


    """
    def test_asignarRolForm(self):

        form = asignarRolForm(data={
            'Usuario': 'Jasinto',
            'Roles': 'Scrum Master',
        })

        self.assertTrue(form.is_valid())
    

    def test_seleccionarRolForm(self):
        form = seleccionarRolForm(data={
            'Rol': Group.objects.all(),
            'RolName':'nuevo rol',
        })

        self.assertTrue(form.is_valid())
    """


    def test_crearRolForm1(self):
        form = crearRolForm(data={
            'RolName':'Scrum Master'
        })

        self.assertTrue(form.is_valid())

    def test_crearRolForm2(self):
        form = crearRolForm(data={
            'RolName':'Product Owner'
        })

        self.assertTrue(form.is_valid())

    def test_crearRolForm3(self):
        form = crearRolForm(data={
            'RolName':'Desarrollador'
        })

        self.assertTrue(form.is_valid())


    def test_crearRolForm4(self):
        form = crearRolForm(data={
            'RolName':'Nombre rol',
            'Proyecto':self.proyecto,
            'Sprint':self.sprints
        })

        self.assertTrue(not(form.is_valid()))

    def test_crearRolForm5(self):
        form = crearRolForm(data={
            'RolName':'nuevo rol'
        })

        self.assertTrue(form.is_valid())

    def test_crearRolForm6(self):
        form = crearRolForm(data={
            'RolName':'Nombre rol'
        })

        self.assertTrue(form.is_valid())


    """
    def test_registroDeUsuariosForm2(self):
        form = registroDeUsuariosForm(data={
            'Usuario':'Cynthia',
            'Habilitado':'true'
        })

        self.assertTrue(not(form.is_valid()))

    def test_registroDeUsuariosForm3(self):
        form = registroDeUsuariosForm(data={
            'Usuario':'Edher',
            'Habilitado':'true'
        })

        self.assertTrue(not(form.is_valid()))

    def test_registroDeUsuariosForm4(self):
        form = registroDeUsuariosForm(data={
            'Usuario':'Leo',
            'Habilitado':'false'
        })

        self.assertTrue(not(form.is_valid()))

    def test_registroDeUsuariosForm5(self):
        form = registroDeUsuariosForm(data={
            'Usuario':'Mady',
            'Habilitado':'true'
        })

        self.assertTrue(not(form.is_valid()))

    def test_registroDeUsuariosForm6(self):
        form = registroDeUsuariosForm(data={
            'Usuario':'Jose',
            'Habilitado':'true'
        })

        self.assertTrue(not(form.is_valid()))

    def test_registroDeUsuariosForm7(self):
        form = registroDeUsuariosForm(data={
            'Usuario':'Luis',
            'Habilitado':'true'
        })

        self.assertTrue(not(form.is_valid()))

    """
    def test_crearUsuarioForm1(self):
        form = crearUsuarioForm(data={
            'Nombre': 'Cristhian',
            'correo': 'cristhian4@gmail.com'
        })

        self.assertTrue(form.is_valid())


    def test_crearUsuarioForm2(self):
        form = crearUsuarioForm(data={
            'Nombre': 'Cynthia',
            'correo': 'Cynthia2@gmail.com'
        })

        self.assertTrue(form.is_valid())


    def test_crearUsuarioForm3(self):
        form = crearUsuarioForm(data={
            'Nombre': 'Mady',
            'correo': 'mady5@gmail.com'
        })

        self.assertTrue(form.is_valid())


    def test_crearUsuarioForm4(self):
        form = crearUsuarioForm(data={
            'Nombre': 'Luis',
            'correo': 'luis9@gmail.com'
        })

        self.assertTrue(form.is_valid())


    def test_crearUsuarioForm5(self):
        form = crearUsuarioForm(data={
            'Nombre': 'Jose',
            'correo': 'jose1@gmail.com'
        })

        self.assertTrue(form.is_valid())


    def test_crearUsuarioForm6(self):
        form = crearUsuarioForm(data={
            'Nombre': 'Leo',
            'correo': 'leo3@gmail.com'
        })

        self.assertTrue(form.is_valid())




    def test_asignarCapacidadForm1(self):

        form = asignarcapacidadForm({
            'capacidad':20
        })

        self.assertTrue(form.is_valid())


    def test_asignarCapacidadForm2(self):

        form = asignarcapacidadForm({
            'capacidad':10
        })

        self.assertTrue(form.is_valid())


    def test_asignarCapacidadFor3(self):

        form = asignarcapacidadForm({
            'capacidad':30
        })

        self.assertTrue(form.is_valid())


    def test_asignarCapacidadForm4(self):

        form = asignarcapacidadForm({
            'capacidad':17
        })

        self.assertTrue(form.is_valid())


    def test_seleccionarProyectoForm(self):

        form = seleccionarProyectoForm({
            'Proyecto':self.proyecto
        })

        self.assertTrue(form.is_valid())


    def test_seleccionarProyectoFormA(self):

        A = Proyecto.objects.create(
            nombre='Proyecto A',
            descripcion='Prueba proyecto A',
            estado='PENDIENTE',
            fecha='2021-09-01',
            fecha_entrega='2021-09-20'
        )

        form = seleccionarProyectoForm({
            'Proyecto':A
        })

        self.assertTrue(form.is_valid())

    def test_seleccionarProyectoFormB(self):
        B = Proyecto.objects.create(
            nombre='Proyecto B',
            descripcion='Prueba proyecto B',
            estado='PENDIENTE',
            fecha='2021-09-08',
            fecha_entrega='2021-09-30'
        )

        form = seleccionarProyectoForm({
            'Proyecto': B
        })

        self.assertTrue(form.is_valid())

    def test_seleccionarProyectoFormC(self):
        C = Proyecto.objects.create(
            nombre='Proyecto C',
            descripcion='Prueba proyecto C',
            estado='PENDIENTE',
            fecha='2021-10-15',
            fecha_entrega='2021-10-27'
        )

        form = seleccionarProyectoForm({
            'Proyecto': C
        })

        self.assertTrue(form.is_valid())

    def test_seleccionarProyectoFormD(self):
        D = Proyecto.objects.create(
            nombre='Proyecto D',
            descripcion='Prueba proyecto D',
            estado='PENDIENTE',
            fecha='2021-10-03',
            fecha_entrega='2021-10-28'
        )

        form = seleccionarProyectoForm({
            'Proyecto': D
        })

        self.assertTrue(form.is_valid())


    def test_seleccionarProyectoFormE(self):
        E = Proyecto.objects.create(
            nombre='Proyecto E',
            descripcion='Prueba proyecto E',
            estado='PENDIENTE',
            fecha='2021-11-01',
            fecha_entrega='2021-11-15'
        )

        form = seleccionarProyectoForm({
            'Proyecto': E
        })

        self.assertTrue(form.is_valid())


    def test_seleccionarProyectoFormF(self):
        F = Proyecto.objects.create(
            nombre='Proyecto F',
            descripcion='Prueba proyecto F',
            estado='PENDIENTE',
            fecha='2021-10-04',
            fecha_entrega='2021-10-19'
        )

        form = seleccionarProyectoForm({
            'Proyecto': F
        })

        self.assertTrue(form.is_valid())



    def test_importarRol1Form(self):

        P = Proyecto.objects.create(
            nombre='Primer Proyecto',
            descripcion='Prueba proyecto 1',
            estado='PENDIENTE',
            fecha='2021-09-11',
            fecha_entrega='2021-10-10'
        )

        form = importarRolForm({
            'ProyectoA':self.proyecto,
            'ProyectoB':P,
        })

        self.assertTrue(form.is_valid())


    def test_cargarHorasHistoria1Form(self):

        form = cargarHorasHistoriaForm({
            'horas':5,
            'comentario': 'Agregamos 5 horas a la historias'
        })

        self.assertTrue(form.is_valid())


    def test_cargarHorasHistoriaForm1(self):

        form = cargarHorasHistoriaForm({
            'horas': 24,
            'comentario': 'Agregamos 24 horas a la historias'
        })

        self.assertTrue(form.is_valid())


    def test_cargarHorasHistoriaForm2(self):

        form = cargarHorasHistoriaForm({
            'horas': 15,
            'comentario': 'Agregamos 15 horas a la historias'
        })

        self.assertTrue(form.is_valid())


    def test_cargarHorasHistoriaForm3(self):

        form = cargarHorasHistoriaForm({
            'horas': 18,
            'comentario': 'Agregamos 18 horas a la historias'
        })

        self.assertTrue(form.is_valid())


    def test_cargarHorasHistoriaForm4(self):

        form = cargarHorasHistoriaForm({
            'horas': 20,
            'comentario': 'Agregamos 20 horas a la historias'
        })

        self.assertTrue(form.is_valid())


    def test_cargarHorasHistoriaForm5(self):

        form = cargarHorasHistoriaForm({
            'horas': 7,
            'comentario': 'Agregamos 7 horas a la historias'
        })

        self.assertTrue(form.is_valid())



    def test_crearRollForm(self):
        form = crearRolForm(data={
            'RolName':'Scrum Master'
        })

        self.assertTrue(form.is_valid())

    def test_crear_RolForm1(self):
        form = crearRolForm(data={
            'RolName':'Product Owner'
        })

        self.assertTrue(form.is_valid())

    def test_crear_RolForm2(self):
        form = crearRolForm(data={
            'RolName':'Desarrollador'
        })

        self.assertTrue(form.is_valid())


    def test_crear_RolForms1(self):
        form = crearRolForm(data={
            'RolName':'Nombre rol',
            'Proyecto':self.proyecto,
            'Sprint':self.sprints
        })

        self.assertTrue(not(form.is_valid()))

    def test_crearRollForm1(self):
        form = crearRolForm(data={
            'RolName':'nuevo rol'
        })

        self.assertTrue(form.is_valid())

    def test_crearRollForm2(self):
        form = crearRolForm(data={
            'RolName':'Nombre rol'
        })

        self.assertTrue(form.is_valid())



    def test_crear_UsuarioForm(self):
        form = crearUsuarioForm(data={
            'Nombre': 'Cristhian',
            'correo': 'cristhian4@gmail.com'
        })

        self.assertTrue(form.is_valid())


    def test_crear_UsuarioForm2(self):
        form = crearUsuarioForm(data={
            'Nombre': 'Cynthia',
            'correo': 'Cynthia2@gmail.com'
        })

        self.assertTrue(form.is_valid())


    def test_crear_UsuarioForm3(self):
        form = crearUsuarioForm(data={
            'Nombre': 'Mady',
            'correo': 'mady5@gmail.com'
        })

        self.assertTrue(form.is_valid())


    def test_crear_UsuarioForm4(self):
        form = crearUsuarioForm(data={
            'Nombre': 'Luis',
            'correo': 'luis9@gmail.com'
        })

        self.assertTrue(form.is_valid())


    def test_crear_UsuarioForm5(self):
        form = crearUsuarioForm(data={
            'Nombre': 'Jose',
            'correo': 'jose1@gmail.com'
        })

        self.assertTrue(form.is_valid())


    def test_crear_UsuarioForm6(self):
        form = crearUsuarioForm(data={
            'Nombre': 'Leo',
            'correo': 'leo3@gmail.com'
        })

        self.assertTrue(form.is_valid())


    def test_asignar_CapacidadForm(self):

        form = asignarcapacidadForm({
            'capacidad':14
        })

        self.assertTrue(form.is_valid())


    def test_asignar_CapacidadForm1(self):

        form = asignarcapacidadForm({
            'capacidad':20
        })

        self.assertTrue(form.is_valid())


    def test_asignar_CapacidadForm2(self):

        form = asignarcapacidadForm({
            'capacidad':10
        })

        self.assertTrue(form.is_valid())


    def test_asignar_Capacidad_Form(self):

        form = asignarcapacidadForm({
            'capacidad':30
        })

        self.assertTrue(form.is_valid())


    def test_asignar_Capacidad_Form1(self):

        form = asignarcapacidadForm({
            'capacidad':17
        })

        self.assertTrue(form.is_valid())


    def test_seleccionarProyectosForm(self):

        form = seleccionarProyectoForm({
            'Proyecto':self.proyecto
        })

        self.assertTrue(form.is_valid())


    def test_seleccionarProyectosFormA(self):

        A = Proyecto.objects.create(
            nombre='Proyecto A',
            descripcion='Prueba proyecto A',
            estado='PENDIENTE',
            fecha='2021-09-01',
            fecha_entrega='2021-09-20'
        )

        form = seleccionarProyectoForm({
            'Proyecto':A
        })

        self.assertTrue(form.is_valid())

    def test_seleccionarProyectosFormB(self):
        B = Proyecto.objects.create(
            nombre='Proyecto B',
            descripcion='Prueba proyecto B',
            estado='PENDIENTE',
            fecha='2021-09-08',
            fecha_entrega='2021-09-30'
        )

        form = seleccionarProyectoForm({
            'Proyecto': B
        })

        self.assertTrue(form.is_valid())
