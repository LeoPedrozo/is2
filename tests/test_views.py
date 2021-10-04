import unittest

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from is2.views import *

from django.urls import reverse

class TestViews(TestCase):

    def setUp(self):

        self.client = Client()
        self.saludo_url = reverse(saludo)
        self.inicio_url = reverse(inicio)
        self.documentaciones_url = reverse(documentaciones)
        self.crear_rol_url = reverse(crearRol)
        self.asignar_rol_url = reverse(asignarRol)
        self.eliminar_rol_url = reverse(eliminarRol)
        self.seleccionar_rol_url = reverse(seleccionarRol)
        self.modificar_rol_url = reverse(crearRol)
        self.registrar_usuario_url = reverse(registrarUsuario)
        self.crear_proyecto_url = reverse(crearProyecto)
        self.modificar_proyecto_url = reverse(modificarProyecto)
        self.eliminar_proyecto_url = reverse(eliminarProyecto)
        self.crear_sprints_url = reverse(crearSprint)
        self.modificar_sprint_url = reverse(modificarSprint)
        self.visualizar_sprint_url = reverse(visualizarSprint)
        self.visualizar_sprint2_url = reverse(visualizarSprint2, args=(1,))
        self.tablero_kanban_url = reverse(tableroKanban)
        self.ver_miembros_url = reverse(verMiembros)
        self.crear_historia_url = reverse(crearHistoria)
        self.seleccionar_historia_url = reverse(seleccionarHistoria)
        self.modificar_historia_url = reverse(crearHistoria)
        self.eliminar_historia_url = reverse(eliminarHistoria)
        self.ver_historias_url = reverse(verHistorias)
        #self.product_Backlog_url = reverse(productBacklog)
        #self.mover_Historia_url = reverse(moverHistoria, args={1,1})
        User = get_user_model()
        User.objects.create_superuser(
            'user1',
            'user1@example.com',
            'pswd',
            proyecto_id = 1,
        )
        self.client.login(username="user1", password="pswd")

    def tearDown(self):
        self.client.logout()

    def test_saludo(self):

        response = self.client.get(self.saludo_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'rolCreado.html')


    def test_inicio(self):

        User = get_user_model()
        #self.client.login(username='temporary', password='temporary')
        response = self.client.get(self.inicio_url)
        #user = User.objects.get(username='temporary')
        self.assertEqual(response.context['mail'], 'user1@example.com')

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registroRequerido.html')


    """def test_documentaciones(self):

        response = self.client.get(self.documentaciones_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    """

    def test_crearRol(self):

        User = get_user_model()
        #self.client.login(username='temporary', password='temporary')
        response = self.client.get(self.crear_rol_url)
        #user = User.objects.get(username='temporary')

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'crearRol.html')



    def test_asignarRol(self):

        User = get_user_model()
        self.client.login(username='temporary2', password='temporary2')
        response = self.client.get(self.asignar_rol_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'asignarRol.html')



    def test_eliminarRol(self):

        response = self.client.get(self.eliminar_rol_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'eliminarRol.html')



    def test_seleccionarRol(self):

        response = self.client.get(self.seleccionar_rol_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'seleccionarRol.html')



    def test_modificarRol(self):

        response = self.client.get(self.modificar_rol_url)

        self.assertEquals(response.status_code, 200)
        #self.assertTemplateUsed(response, 'outputmodificarRol.html')
        self.assertTemplateUsed(response, 'crearRol.html')



    def test_registrarUsuario(self):

        response = self.client.get(self.registrar_usuario_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'RegistrarUsuario.html')



    def test_crearProyecto(self):

        response = self.client.get(self.crear_proyecto_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'crearProyecto.html')


    def test_modificarProyecto(self):

        response = self.client.get(self.modificar_proyecto_url)

        self.assertEquals(response.status_code, 200)
        #self.assertTemplateUsed(response, 'outputmodificarProyecto.html')
        self.assertTemplateUsed(response, 'modificarProyecto.html')


    def test_eliminarProyecto(self):

        response = self.client.get(self.eliminar_proyecto_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'eliminarProyecto.html')


    def test_crearSprint(self):

        response = self.client.get(self.crear_sprints_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'crearSprint.html')


    def test_modificarSprint(self):

        response = self.client.get(self.modificar_sprint_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')


    def test_visualizarSprint(self):

        response = self.client.get(self.visualizar_sprint_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'ListarSprints.html')


    def test_visualizarSprint2(self):

        response = self.client.get(self.visualizar_sprint2_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tableroKanbanSprintAnterior.html')


    def test_tableroKanban(self):

        response = self.client.get(self.tablero_kanban_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tableroKanban.html')


    def test_crearHistoria(self):

        response = self.client.get(self.crear_historia_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'crearUserStory.html')


    def test_seleccionarHistoria(self):

        response = self.client.get(self.seleccionar_historia_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'seleccionarHistoria.html')


    def test_modificarHistoria(self):

        User = get_user_model()
        response = self.client.get(self.modificar_historia_url)
        #user = User.objects.get(username='temporary')

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'crearUserStory.html')


    def test_eliminarHistoria(self):

        response = self.client.get(self.eliminar_historia_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'eliminarHistoria.html')


    def test_verHistorias(self):

        response = self.client.get(self.ver_historias_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'HistoriaContent.html')


    """def test_productBacklog(self):

        response = self.client.get(self.product_Backlog_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'HistoriaContent.html')
    """
    #def test_moverHistoria(self):



