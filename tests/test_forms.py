from django.contrib.auth.models import Permission
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

        self.estados=(
            (True,"Habilitar acceso al sistema"),
            (False,"Restringir acceso al sistema"),
        )


    def test_crearRolForm(self):

        form = crearRolForm(
         data={
            'RolName':'New rol',
        })

        self.assertTrue(form.is_valid())

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

    def test_crearUsuarioForm(self):
        form = crearUsuarioForm(data={
            'Nombre':'Juan',
            'correo':'juan3@gmail.com'
        })

        self.assertTrue(form.is_valid())


    def test_registroDeUsuariosForm(self):
        form = registroDeUsuariosForm(data={
            'Usuario':User(username='Juan'),
            'Habilitado':"Habilitar acceso al sistema"
        })

        self.assertTrue(not(form.is_valid()))


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


    def test_asignarCapacidadForm(self):

        form = asignarcapacidadForm({
            'capacidad':14
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



    def test_importarRolForm(self):

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


    def test_cargarHorasHistoriaForm(self):

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


    def test_asignarEncargadoForm(self):

        user = User(username='luis_Alberto')

        form = asignarEncargadoForm({
            'Usuario': user,
            'Historia': Historia.objects.all()
        })

        self.assertTrue(form.is_valid())


    def test_asignarEncargadoForm1(self):

        user = User(username='AsuncionGM')

        form = asignarEncargadoForm({
            'Usuario': user,
            'Historia': Historia.objects.all()
        })

        self.assertTrue(form.is_valid())


    def test_asignarEncargadoFor2(self):

        user = User(username='Emigdio_Coronel')

        form = asignarEncargadoForm({
            'Usuario': user,
            'Historia': Historia.objects.all()
        })

        self.assertTrue(form.is_valid())


    def test_asignarEncargadoForm3(self):

        user = User(username='Felix_Alexander')

        form = asignarEncargadoForm({
            'Usuario': user,
            'Historia': Historia.objects.all()
        })

        self.assertTrue(form.is_valid())


    def test_asignarEncargadoForm4(self):

        user = User(username='Hector_Mendez')

        form = asignarEncargadoForm({
            'Usuario': user,
            'Historia': Historia.objects.all()
        })

        self.assertTrue(form.is_valid())


    def test_asignarEncargadoForm5(self):

        user = User(username='Dora_Anastacia')

        form = asignarEncargadoForm({
            'Usuario': user,
            'Historia': Historia.objects.all()
        })

        self.assertTrue(form.is_valid())


    def test_eliminarHistoriaForm(self):


        form = asignarEncargadoForm({
            'Historia': Historia.objects.all()
        })

        self.assertTrue(form.is_valid())

