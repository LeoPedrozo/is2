import unittest
from django.test import Client
from is2.views import *

from django.urls import reverse

class TestViews(unittest.TestCase):

    def setUp(self):

        self.client = Client()
        self.saludo_url = reverse(saludo)
        self.inicio_url = reverse(inicio)
        self.documentaciones_url = reverse(documentaciones)
        self.crear_rol_url = reverse(crearRol)
        self.asignar_rol_url = reverse(asignarRol)
        self.eliminar_rol_url = reverse(eliminarRol)
        self.seleccionar_rol_url = reverse(seleccionarRol)
        self.modificar_rol_url = reverse(modificarRol)
        self.registrar_usuario_url = reverse(registrarUsuario)
        self.crear_proyecto_url = reverse(crearProyecto)
        self.modificar_proyecto_url = reverse(modificarProyecto)
        self.eliminar_proyecto_url = reverse(eliminarProyecto)
        self.crear_sprints_url = reverse(crearSprint)
        self.ver_miembros_url = reverse(verMiembros)
        self.crear_historia_url = reverse(crearHistoria)
        self.seleccionar_historia_url = reverse(seleccionarHistoria)
        self.modificar_historia_url = reverse(modificarHistoria)
        self.ver_historias_url = reverse(verHistorias)


    def test_inicio(self):

        response = self.client.get(self.inicio_url)

        self.assertEquals(response.status_code, 200)



    def test_documentaciones(self):

        response = self.client.get(self.documentaciones_url)

        self.assertEquals(response.status_code, 200)



    def test_crearRol(self):

        response = self.client.get(self.crear_rol_url)

        self.assertEquals(response.status_code, 200)



    def test_asignarRol(self):

        response = self.client.get(self.asignar_rol_url)

        self.assertEquals(response.status_code, 200)



    def test_eliminarRol(self):

        response = self.client.get(self.eliminar_rol_url)

        self.assertEquals(response.status_code, 200)



    def test_seleccionarRol(self):

        response = self.client.get(self.seleccionar_rol_url)

        self.assertEquals(response.status_code, 200)



    def test_modificarRol(self):

        response = self.client.get(self.modificar_rol_url)

        self.assertEquals(response.status_code, 200)



    def test_registrarUsuario(self):

        response = self.client.get(self.registrar_usuario_url)

        self.assertEquals(response.status_code, 200)



    def test_crearProyecto(self):

        response = self.client.get(self.crear_proyecto_url)

        self.assertEquals(response.status_code, 200)



    def test_modificarProyecto(self):

        response = self.client.get(self.modificar_proyecto_url)

        self.assertEquals(response.status_code, 200)



    def test_eliminarProyecto(self):

        response = self.client.get(self.eliminar_proyecto_url)

        self.assertEquals(response.status_code, 200)



    def test_crearSprint(self):

        response = self.client.get(self.crear_sprints_url)

        self.assertEquals(response.status_code, 200)



    def test_verMiembros(self):

        response = self.client.get(self.ver_miembros_url)

        self.assertEquals(response.status_code, 200)



    def test_crearHistoria(self):

        response = self.client.get(self.crear_historia_url)

        self.assertEquals(response.status_code, 200)



    def test_seleccionarHistoria(self):

        response = self.client.get(self.seleccionar_historia_url)

        self.assertEquals(response.status_code, 200)



    def test_modificarHistoria(self):

        response = self.client.get(self.modificar_historia_url)

        self.assertEquals(response.status_code, 200)



    def test_verHistorias(self):

        response = self.client.get(self.ver_historias_url)

        self.assertEquals(response.status_code, 200)