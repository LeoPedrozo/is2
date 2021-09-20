
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

    """
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

