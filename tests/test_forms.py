from django.test import TestCase
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
            fecha='2021-07-25',
            fecha_entrega='2021-07-26'
        )

        self.sprints = Sprint.objects.create(
            sprintNumber=5,
            fecha_inicio='2021-09-16',
            fecha_fin='2021-09-20'
        )


    def test_crearRolForm(self):
        form = crearRolForm(data={
            'RolName':'Nombre rol',
            'Proyecto':self.proyecto,
            'Sprint':self.sprints
        })

        self.assertTrue(not(form.is_valid()))

    """"
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

        self.assertTrue(form.is_valid())

    
    def test_modificarRolForm(self):
        form = modificarRolForm(data={
            'RolName':'Nombre rol',
            'Proyecto':self.proyecto,
            'Sprint':self.sprints
        })

        self.assertTrue(form.is_valid())
    """

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


    def test_crearRolForm1(self):
        form = crearRolForm(data={
            'RolName':'Nombre rol',
            'Proyecto':self.proyecto,
            'Sprint':self.sprints
        })

        self.assertTrue(not(form.is_valid()))

    def test_crearRolForm2(self):
        form = crearRolForm(data={
            'RolName':'Nombre rol',
            'Proyecto':self.proyecto,
            'Sprint':self.sprints
        })

        self.assertTrue(not(form.is_valid()))

    def test_crearRolForm3(self):
        form = crearRolForm(data={
            'RolName':'Nombre rol',
            'Proyecto':self.proyecto,
            'Sprint':self.sprints
        })

        self.assertTrue(not(form.is_valid()))


    def test_crearRolForm4(self):
        form = crearRolForm(data={
            'RolName':'Nombre rol',
            'Proyecto':self.proyecto,
            'Sprint':self.sprints
        })

        self.assertTrue(not(form.is_valid()))

    def test_crearRolForm5(self):
        form = crearRolForm(data={
            'RolName':'Nombre rol',
            'Proyecto':self.proyecto,
            'Sprint':self.sprints
        })

        self.assertTrue(not(form.is_valid()))

    def test_crearRolForm6(self):
        form = crearRolForm(data={
            'RolName':'Nombre rol',
            'Proyecto':self.proyecto,
            'Sprint':self.sprints
        })

        self.assertTrue(not(form.is_valid()))


    def test_registroDeUsuariosForm1(self):
        form = registroDeUsuariosForm(data={
            'Usuario':'Cristhian',
            'Habilitado':'false'
        })

        self.assertTrue(not(form.is_valid()))

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