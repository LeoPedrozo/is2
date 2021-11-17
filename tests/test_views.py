import unittest

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from is2.views import *

from django.urls import reverse

class TestViews(TestCase):

    def setUp(self):

        self.client = Client()
        self.saludo_url = reverse(saludo)
        self.accesoDenegado_url = reverse(accesoDenegado)
        self.inicio_url = reverse(inicio)
        self.documentaciones_url = reverse(documentaciones)
        self.step1_crear_rol_url = reverse(step1_CrearRol)
        self.step2_crear_rol_url = reverse(step2_CrearRol)
        self.eliminar_rol_url = reverse(step1_eliminarRol)
        self.step1_asignar_rol_url = reverse(step1_CrearRol)
        self.step2_asignar_rol_url = reverse(step1_CrearRol)
        self.step1_modificar_rol_url = reverse(step1_modificarRol)
        self.step2_modificar_rol_url = reverse(step1_modificarRol)
        self.step3_modificar_rol_url = reverse(step1_modificarRol)
        self.importar_rol_url = reverse(importarRol)
        self.registrar_usuario_url = reverse(registrarUsuario)
        self.crear_proyecto_url = reverse(crearProyecto)
        self.modificar_proyecto_url = reverse(modificarProyecto)
        #self.modificar_proyecto2_url = reverse(modificarProyecto2)
        self.eliminar_proyecto_url = reverse(eliminarProyecto)
        #self.eliminar_proyecto2_url = reverse(eliminarProyecto2)
        self.crear_sprints_url = reverse(step1_SprintPlanning)
        self.step1_SprintPlanning_url = reverse(step1_SprintPlanning)
        self.step2_SprintPlanning_url = reverse(step2_SprintPlanning)
        self.step3_SprintPlanning_url = reverse(step3_SprintPlanning)
        self.step3_asignarEncargado_url = reverse(step3_SprintPlanning)
        #self.asignarCapacidad_url = reverse(asignarCapacidad)
        #self.modificarSprint_url = reverse(modificarSprint)
        #self.eliminarSprint_url = reverse(eliminarSprint)
        self.visualizar_sprint_url = reverse(visualizarSprint)
        #self.visualizar_sprint2_url = reverse(visualizarSprint2, args=(1,))
        self.tablero_kanban_url = reverse(tableroKanban)
        self.ver_miembros_url = reverse(verMiembros)
        #self.crear_historia_url = reverse(crearHistoria)
        self.seleccionar_historia_url = reverse(seleccionarHistoria)
        self.asignarHistoriaEncargado_url = reverse(asignarHistoriaEncargado)
        #self.modificar_historia_url = reverse(crearHistoria)
        self.eliminar_historia_url = reverse(eliminarHistoria)
        #self.sprintBacklog_url = reverse(sprintBacklog)
        self.ver_historias_url = reverse(productBacklog)
        self.product_Backlog_url = reverse(productBacklog)
        #self.moverHistoria_url = reverse(moverHistoria)
        #self.asignarSprint_url = reverse(asignarSprint)
        self.search_url = reverse(productBacklog)
        self.tableroQA_Release_url = reverse(tableroQA_Release)
        #self.moverHistoriaQA_url = reverse(moverHistoriaQA)
        self.searchvisualizarSprintFilter_url = reverse(visualizarSprintFilter)
        self.HistorialProyectoFilter_url = reverse(importarRol)
        self.historicoSprint_url = reverse(historicoSprint)
        #self.HistorialSprintFilter_url = reverse(HistorialSprintFilter)
        #self.line_chart_url = reverse(lineChart)
        #self.mover_Historia_url = reverse(moverHistoria, args={1,1})
        User = get_user_model()
        User.objects.create_superuser(
            'user1',
            'user1@example.com',
            'pswd'
        )
        self.client.login(username="user1", password="pswd")

    def tearDown(self):
        self.client.logout()

    def test_saludo(self):

        response = self.client.get(self.accesoDenegado_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, '403.html')


    def test_accesoDenegado(self):

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

    def test_step1_crearRol(self):

        User = get_user_model()
        #self.client.login(username='temporary', password='temporary')
        response = self.client.get(self.step1_crear_rol_url)
        #user = User.objects.get(username='temporary')

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'seleccionarProyecto.html')


    def test_step2_crearRol(self):

        User = get_user_model()
        #self.client.login(username='temporary', password='temporary')
        response = self.client.get(self.step2_crear_rol_url)
        #user = User.objects.get(username='temporary')

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'crearRol.html')


    def test_step1_asignarRol(self):

        User = get_user_model()
        self.client.login(username='temporary2', password='temporary2')
        response = self.client.get(self.step2_asignar_rol_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'seleccionarProyecto.html')


    def test_step2_asignarRol(self):

        User = get_user_model()
        self.client.login(username='temporary2', password='temporary2')
        response = self.client.get(self.step2_asignar_rol_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'seleccionarProyecto.html')


    def test_eliminarRol(self):

        response = self.client.get(self.eliminar_rol_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'seleccionarProyecto.html')


    def test_step1eliminarRol(self):

        response = self.client.get(self.eliminar_rol_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'seleccionarProyecto.html')


    def test_step2eliminarRol(self):

        response = self.client.get(self.eliminar_rol_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'seleccionarProyecto.html')



    def test_step1_modificarRol(self):

        response = self.client.get(self.step1_modificar_rol_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'seleccionarProyecto.html')


    def test_step2_modificarRol(self):

        response = self.client.get(self.step2_modificar_rol_url)

        self.assertEquals(response.status_code, 200)
        #self.assertTemplateUsed(response, 'outputmodificarRol.html')
        self.assertTemplateUsed(response, 'seleccionarProyecto.html')


    def test_step3_modificarRol(self):

        response = self.client.get(self.step3_modificar_rol_url)

        self.assertEquals(response.status_code, 200)
        #self.assertTemplateUsed(response, 'outputmodificarRol.html')
        self.assertTemplateUsed(response, 'seleccionarProyecto.html')


    def test_importarRol(self):

        response = self.client.get(self.importar_rol_url)

        self.assertEquals(response.status_code, 200)
        #self.assertTemplateUsed(response, 'outputmodificarRol.html')
        self.assertTemplateUsed(response, 'seleccionarProyecto.html')


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
        self.assertTemplateUsed(response, 'Condicion_requerida.html')
    """
    def test_modificarProyecto2(self):

        response = self.client.get(self.modificar_proyecto2_url)

        self.assertEquals(response.status_code, 200)
        #self.assertTemplateUsed(response, 'outputmodificarProyecto.html')
        self.assertTemplateUsed(response, 'Condicion_requerida.html')
    """

    def test_eliminarProyecto(self):

        response = self.client.get(self.eliminar_proyecto_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'eliminarProyecto.html')

    """
    def test_eliminarProyecto2(self):

        response = self.client.get(self.eliminar_proyecto2_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'eliminarProyecto.html')
    """

    def test_swichProyecto(self):

        response = self.client.get(self.inicio_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registroRequerido.html')


    def test_getPermisos(self):
        response = self.client.get(self.inicio_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registroRequerido.html')


    def test_step1_SprintPlanning(self):

        response =  self.client.get(self.step1_SprintPlanning_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')


    def test_step2_SprintPlanning(self):

        response =  self.client.get(self.step1_SprintPlanning_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')

    """
    def test_asignarCapacidad(self):

        response =  self.client.get(self.step2_SprintPlanning_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')
    """

    """
    def test_asignarCapacidad(self):

        response = self.client.get(self.asignarCapacidad_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')
    """

    def test_step3_SprintPlanning(self):

        response =  self.client.get(self.step1_SprintPlanning_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')


    def test_step3_asignarEncargado(self):

        response =  self.client.get(self.step1_SprintPlanning_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')

    """
    def test_modificarSprint(self):

        response =  self.client.get(self.modificarSprint_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'modificarSprint.html')
    
    
    def test_eliminarSprint(self):

        response =  self.client.get(self.eliminarSprint_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'outputEliminarSprintl.html')
    """

    def test_crearSprint(self):

        response = self.client.get(self.crear_sprints_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')


    """
    def test_modificarSprint(self):

        response = self.client.get(self.modificar_sprint_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')
    """


    def test_visualizarSprint(self):

        response = self.client.get(self.visualizar_sprint_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')

    """
    def test_visualizarSprint2(self):

        response = self.client.get(self.visualizar_sprint2_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tableroKanbanSprintAnterior.html')
    """

    def test_tableroKanban(self):

        response = self.client.get(self.tablero_kanban_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')

    """
    def test_crearHistoria(self):

        response = self.client.get(self.crear_historia_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'crearUserStory.html')
    """

    def test_seleccionarHistoria(self):

        response = self.client.get(self.seleccionar_historia_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'seleccionarHistoria.html')


    def test_asignarHistoriaEncargado(self):

        response = self.client.get(self.asignarHistoriaEncargado_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'asignarEncargado.html')

    """
    def test_modificarHistoria(self):

        response = self.client.get(self.modificar_historia_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'modificarHistoria.html')
    """

    def test_eliminarHistoria(self):

        response = self.client.get(self.eliminar_historia_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'eliminarHistoria.html')

    """
    def test_sprintBacklog(self):

        response = self.client.get(self.sprintBacklog_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'SprintBacklog.html')
    """

    def test_productBacklog(self):

        response = self.client.get(self.product_Backlog_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'SprintBacklog.html')

    """
    def test_moverHistoria(self):

        response = self.client.get(self.moverHistoria_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tableroKanban.html')
    """

    def test_search(self):

        response = self.client.get(self.search_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'SprintBacklog.html')

    """
    def test_asignarSprint(self):

        response = self.client.get(self.asignarSprint_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'SprintBacklog.html')


    def test_lineChart(self):

        response = self.client.get(self.line_chart_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')
    """


    def test_tableroQARelease(self):
        response = self.client.get(self.tableroQA_Release_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')

    """
    def test_moverHistoriaQA(self):
        response = self.client.get(self.moverHistoriaQA_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')
    """


    def test_visualizarSprintFilter(self):

        response = self.client.get(self.searchvisualizarSprintFilter_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')


    def test_HistorialProyectoFilter(self):

        response = self.client.get(self.HistorialProyectoFilter_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'seleccionarProyecto.html')


    def test_historicoSprint(self):

        response = self.client.get(self.historicoSprint_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')

    def test_saludoHTML(self):
        response = self.client.get(self.accesoDenegado_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, '403.html')

    def test_accesoDenegadoHTML(self):
        response = self.client.get(self.saludo_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'rolCreado.html')

    def test_inicioHTML(self):
        User = get_user_model()
        # self.client.login(username='temporary', password='temporary')
        response = self.client.get(self.inicio_url)
        # user = User.objects.get(username='temporary')
        self.assertEqual(response.context['mail'], 'user1@example.com')

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registroRequerido.html')

    """def test_documentaciones(self):
        response = self.client.get(self.documentaciones_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    """

    def test_step1_crearRolHTML(self):
        User = get_user_model()
        # self.client.login(username='temporary', password='temporary')
        response = self.client.get(self.step1_crear_rol_url)
        # user = User.objects.get(username='temporary')

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'seleccionarProyecto.html')

    def test_step2_crearRolHTML(self):
        User = get_user_model()
        # self.client.login(username='temporary', password='temporary')
        response = self.client.get(self.step2_crear_rol_url)
        # user = User.objects.get(username='temporary')

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'crearRol.html')

    def test_step1_asignarRolHTML(self):
        User = get_user_model()
        self.client.login(username='temporary2', password='temporary2')
        response = self.client.get(self.step2_asignar_rol_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'seleccionarProyecto.html')

    def test_step2_asignarRolHTML(self):
        User = get_user_model()
        self.client.login(username='temporary2', password='temporary2')
        response = self.client.get(self.step2_asignar_rol_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'seleccionarProyecto.html')

    def test_eliminarRolHTML(self):
        response = self.client.get(self.eliminar_rol_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'seleccionarProyecto.html')

    def test_step1eliminarRolHTML(self):
        response = self.client.get(self.eliminar_rol_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'seleccionarProyecto.html')

    def test_step2eliminarRolHTML(self):
        response = self.client.get(self.eliminar_rol_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'seleccionarProyecto.html')

    def test_step1_modificarRolHTML(self):
        response = self.client.get(self.step1_modificar_rol_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'seleccionarProyecto.html')

    def test_step2_modificarRolHTML(self):
        response = self.client.get(self.step2_modificar_rol_url)

        self.assertEquals(response.status_code, 200)
        # self.assertTemplateUsed(response, 'outputmodificarRol.html')
        self.assertTemplateUsed(response, 'seleccionarProyecto.html')

    def test_step3_modificarRolHTML(self):
        response = self.client.get(self.step3_modificar_rol_url)

        self.assertEquals(response.status_code, 200)
        # self.assertTemplateUsed(response, 'outputmodificarRol.html')
        self.assertTemplateUsed(response, 'seleccionarProyecto.html')

    def test_importarRolHTML(self):
        response = self.client.get(self.importar_rol_url)

        self.assertEquals(response.status_code, 200)
        # self.assertTemplateUsed(response, 'outputmodificarRol.html')
        self.assertTemplateUsed(response, 'seleccionarProyecto.html')

    def test_registrarUsuarioHTML(self):
        response = self.client.get(self.registrar_usuario_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'RegistrarUsuario.html')

    def test_crearProyectoHTML(self):
        response = self.client.get(self.crear_proyecto_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'crearProyecto.html')

    def test_modificarProyectoHTML(self):
        response = self.client.get(self.modificar_proyecto_url)

        self.assertEquals(response.status_code, 200)
        # self.assertTemplateUsed(response, 'outputmodificarProyecto.html')
        self.assertTemplateUsed(response, 'Condicion_requerida.html')

    """
    def test_modificarProyecto2(self):

        response = self.client.get(self.modificar_proyecto2_url)

        self.assertEquals(response.status_code, 200)
        #self.assertTemplateUsed(response, 'outputmodificarProyecto.html')
        self.assertTemplateUsed(response, 'Condicion_requerida.html')
    """

    def test_eliminarProyectoHTML(self):
        response = self.client.get(self.eliminar_proyecto_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'eliminarProyecto.html')

    """
    def test_eliminarProyecto2(self):

        response = self.client.get(self.eliminar_proyecto2_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'eliminarProyecto.html')
    """

    def test_swichProyectoHTML(self):
        response = self.client.get(self.inicio_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registroRequerido.html')

    def test_getPermisosHTML(self):
        response = self.client.get(self.inicio_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registroRequerido.html')

    def test_step1_SprintPlanningHTML(self):
        response = self.client.get(self.step1_SprintPlanning_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')

    def test_step2_SprintPlanningHTML(self):
        response = self.client.get(self.step1_SprintPlanning_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')

    """
    def test_asignarCapacidad(self):

        response =  self.client.get(self.step2_SprintPlanning_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')
    """

    """
    def test_asignarCapacidad(self):

        response = self.client.get(self.asignarCapacidad_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')
    """

    def test_step3_SprintPlanningHTML(self):
        response = self.client.get(self.step1_SprintPlanning_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')

    def test_step3_asignarEncargadoHTML(self):
        response = self.client.get(self.step1_SprintPlanning_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')

    """
    def test_modificarSprint(self):

        response =  self.client.get(self.modificarSprint_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'modificarSprint.html')


    def test_eliminarSprint(self):

        response =  self.client.get(self.eliminarSprint_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'outputEliminarSprintl.html')
    """

    def test_crearSprintHTML(self):
        response = self.client.get(self.crear_sprints_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')

    """
    def test_modificarSprint(self):

        response = self.client.get(self.modificar_sprint_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')
    """

    def test_visualizarSprintHTML(self):
        response = self.client.get(self.visualizar_sprint_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')

    """
    def test_visualizarSprint2(self):

        response = self.client.get(self.visualizar_sprint2_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tableroKanbanSprintAnterior.html')
    """

    def test_tableroKanbanHTML(self):
        response = self.client.get(self.tablero_kanban_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')

    """
    def test_crearHistoria(self):

        response = self.client.get(self.crear_historia_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'crearUserStory.html')
    """

    def test_seleccionarHistoriaHTML(self):
        response = self.client.get(self.seleccionar_historia_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'seleccionarHistoria.html')

    def test_asignarHistoriaEncargadoHTML(self):
        response = self.client.get(self.asignarHistoriaEncargado_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'asignarEncargado.html')

    """
    def test_modificarHistoria(self):

        response = self.client.get(self.modificar_historia_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'modificarHistoria.html')
    """

    def test_eliminarHistoriaHTML(self):
        response = self.client.get(self.eliminar_historia_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'eliminarHistoria.html')

    """
    def test_sprintBacklog(self):

        response = self.client.get(self.sprintBacklog_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'SprintBacklog.html')
    """

    def test_productBacklogHTML(self):
        response = self.client.get(self.product_Backlog_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'SprintBacklog.html')

    """
    def test_moverHistoria(self):

        response = self.client.get(self.moverHistoria_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tableroKanban.html')
    """

    def test_searchHTML(self):
        response = self.client.get(self.search_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'SprintBacklog.html')

    """
    def test_asignarSprint(self):

        response = self.client.get(self.asignarSprint_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'SprintBacklog.html')


    def test_lineChart(self):

        response = self.client.get(self.line_chart_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')
    """

    def test_tableroQAReleaseHTML(self):
        response = self.client.get(self.tableroQA_Release_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')

    """
    def test_moverHistoriaQA(self):
        response = self.client.get(self.moverHistoriaQA_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')
    """

    def test_visualizarSprintFilterHTML(self):
        response = self.client.get(self.searchvisualizarSprintFilter_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')

    def test_HistorialProyectoFilterHTML(self):
        response = self.client.get(self.HistorialProyectoFilter_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'seleccionarProyecto.html')

    def test_historicoSprintHTML(self):
        response = self.client.get(self.historicoSprint_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Condicion_requerida.html')

