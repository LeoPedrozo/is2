
import unittest
from random import randrange

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
            fecha='25/07/2021',
            fecha_entrega='2021-07-26'
        )

        self.sprints = Sprint.objects.create(
            sprintNumber=5,
            fecha_inicio='16/09/2021',
            fecha_fin='20/09/2021'
        )


    def test_crearRolForm(self):
        form = crearRolForm(data={
            'RolName':'Nombre rol',
            'Proyecto':self.proyecto,
            'Sprint':self.sprints
        })

        self.assertTrue(not(form.is_valid()))


    def test_asignarRolForm(self):
        form = asignarRolForm(data={
            'Usuario': User.objects.all(),
            'Roles': Group.objects.all(),
        })

        self.assertTrue(not(form.is_valid()))


    def test_seleccionarRolForm(self):
        form = seleccionarRolForm(data={
            'Rol': Group.objects.all(),
        })

        self.assertTrue(not(form.is_valid()))


    def test_modificarRolForm(self):
        form = modificarRolForm(data={
            'RolName':'Nombre rol',
            'Proyecto':self.proyecto,
            'Sprint':self.sprints
        })

        self.assertTrue(form.is_valid())


    def test_crearUsuarioForm(self):
        form = crearUsuarioForm(data={
            'Nombre':'Juan',
            'correo':'juan3@gmail.com'
        })

        self.assertTrue(form.is_valid())


    def test_registroDeUsuariosForm(self):
        form = registroDeUsuariosForm(data={
            'Usuario':User.objects.all(),
            'Habilitado':'true'
        })

        self.assertTrue(not(form.is_valid()))


    def test_crearproyectoForm(self):
        form = crearproyectoForm(data={
            'nombre':'Nombre proyecto',
            'descripcion':'prueba proyecto',
            'creador':'edhcoro',
            'estado':'pendiente',
            'fecha':'18/09/2021',
            'fecha_entrega':'20/09/2021',
            'miembros':User.objects.all()
        })

        self.assertTrue(form.is_valid())

    def test_modificarproyectoForm(self):
        form = modificarproyectoForm(data={
            'nombre': 'Nombre proyecto',
            'descripcion': 'prueba proyecto',
            'creador': 'madygamma',
            'estado': 'Finalizado',
            'fecha': '15/09/2021',
            'fecha_entrega': '30/09/2021',
            'miembros': User.objects.all()
        })

        self.assertTrue(form.is_valid())


    def test_crearSprintForm(self):
        form = crearSprintForm(data={
            'sprintNumber': 3,
            'fecha_inicio': '19/09/2021',
            'fecha_fin': '30/12/2021',
            'historias': Historia.objects.all(),
        })

        self.assertTrue(form.is_valid())


    def test_crearHistoriaForm(self):
        form = crearHistoriaForm(data={
            'nombre' : 'Historia 1',
            'descripcion' : 'Historia de prueba',
            'prioridad' : 'ALTA',
            'fecha_creacion' : '2021/09/02',
            'horasEstimadas' : 20,
            'estados' : 'PENDIENTE',
            'horas_dedicadas' : 50
        })



        self.assertTrue(form.is_valid())


    def test_seleccionarHistoriaForm(self):
        form = seleccionarHistoriaForm(data={
            'Historia':Historia.objects.all()
        })

        self.assertTrue(form.is_valid())


    def test_modificarHistoriaForm(self):
        form = modificarHistoriaForm(data={
            'id_historia':2,
            'nombre':'historia 1',
            'descripcion':'prueba historia',
            'prioridad':'Alta',
            'fecha_creacion':'25/09/2021',
            'horasEstimadas':10,
            'estados':'Pendiente',
            'horas_dedicadas':1
        })

        self.assertTrue(form.is_valid())
