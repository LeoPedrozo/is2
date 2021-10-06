from django.test import TestCase
import time

from Sprints.models import Sprint
from proyectos.models import Proyecto
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from gestionUsuario.models import User
from userStory.models import Historia

class TestModels(TestCase):

    """
    Clase de testeo de todos los models del sistema
    """

    def test_userAdmitido(self):
        """
        Test de usuario admitido a loggerarse al sistema
        """
        p = Proyecto(nombre='Primer Proyecto',descripcion='Proyecto de prueba',estado='PENDIENTE',fecha='25/07/2021',fecha_entrega='26/07/2021')
        userNew = User(proyecto=p.id)
        self.assertIsNotNone(userNew)


    def test_crearProyecto(self):
        """
        Test : Validacion de creacion del proyecto
        """
        nuevoProyecto = Proyecto(
            nombre='Primer Proyecto',
            descripcion='Proyecto de prueba',
            estado='PENDIENTE',
            fecha='2021-07-25',
            fecha_entrega='2021-07-30')
        nuevoProyecto.save()
        self.assertIsNotNone(nuevoProyecto)

    def test_validacion_nombre_proyecto(self):
        """
        Verifica que la validacion de obligatoriedad del campo nombre se ejecute correctamente
        """
        nuevoProyecto = Proyecto(
            #nombre='Primer Proyecto',
            descripcion='Proyecto de prueba',
            estado='PENDIENTE',
            fecha='2021-07-25',
            fecha_entrega='2021-07-26',
        )

        self.assertTrue(nuevoProyecto.validate_test(), "Debe ingresar el nombre del proyecto")


    def test_validacion_descripcion_proyecto(self):
        """
        Verifica que la validacion de obligatoriedad del campo descripcion se ejecute correctamente
        """
        nuevoProyecto = Proyecto(
            nombre='Primer Proyecto',
            #descripcion='Proyecto de prueba',
            estado='PENDIENTE',
            fecha='2021-07-25',
            fecha_entrega='2021-07-26',
        )

        self.assertTrue(nuevoProyecto.validate_test(), "Debe ingresar la descripcion del proyecto")


    def test_validacion_estado_proyecto(self):
        """
        Verifica que la validacion de obligatoriedad del campo estado se ejecute correctamente
        """
        P = Proyecto(
            nombre='Primer Proyecto',
            descripcion='Proyecto de prueba',
            #estado='PENDIENTE',
            fecha='2021-07-25',
            fecha_entrega='2021-07-26',
        )

        self.assertTrue(P.validate_test(), "Debe seleccionar el estado del proyecto")


    def test_validacion_fecha_proyecto(self):
        """
        Verifica que la validacion de obligatoriedad del campo fecha se ejecute correctamente
        """
        nuevoProyecto = Proyecto(
            nombre='Primer Proyecto',
            descripcion='Proyecto de prueba',
            estado='PENDIENTE',
            #fecha='2021-07-25',
            fecha_entrega='2021-07-26',
        )

        self.assertTrue(nuevoProyecto.validate_test(), "Debe ingresar la fecha de creacion del proyecto")


    def test_validacion_fecha_entrega_proyecto(self):
        """
        Verifica que la validacion de obligatoriedad del campo fecha_entrega se ejecute correctamente
        """
        nuevoProyecto = Proyecto(
            nombre='Primer Proyecto',
            descripcion='Proyecto de prueba',
            estado='PENDIENTE',
            fecha='2021-07-25',
            #fecha_entrega='2021-07-26',
        )

        self.assertTrue(nuevoProyecto.validate_test(), "Debe ingresar la fecha de entrega estimada del proyecto")


    def test_validacion_fechasProyecto(self):
        """
        Test: Validacion de inicio y fin de proyecto
        """
        p = Proyecto(nombre='Prueba proyecto', fecha='25/07/2021', fecha_entrega='26/07/2021')
        fechIni = time.strptime(p.fecha, "%d/%m/%Y")
        fechFin = time.strptime(p.fecha_entrega, "%d/%m/%Y")
        self.assertLessEqual(fechIni, fechFin, "Fecha no valida. fecha inicio debe ser menor a entrega")



    def test_creacionSprint(self):
        """
        Test de creacion de sprint
        """
        sprint = Sprint(
            sprintNumber=5,
            fecha_inicio='16/09/2021',
            fecha_fin='20/09/2021')
        self.assertIsNotNone(sprint)


    def test_validacion_sprint_number(self):
        """
        Verifica que la validacion de obligatoriedad del campo sprintNumber se ejecute correctamente
        """
        s = Sprint(
            #sprintNumber=9,
            fecha_inicio='2021-07-25',
            fecha_fin='2021-07-26'
        )
        self.assertTrue(s.validate_test(),"Debe ingresar el numero del sprint")



    def test_validacion_fecha_inicio_sprint(self):
        """
        Verifica que la validacion de obligatoriedad del campo fecha_inicio se ejecute correctamente
        """
        s = Sprint(
            sprintNumber=9,
            #fecha_inicio='2021-07-25',
            fecha_fin='2021-07-26'
        )
        self.assertTrue(s.validate_test(),"Debe ingresar la fecha de inicio del sprint")



    def test_validacion_fecha_fin_sprint(self):
        """
        Verifica que la validacion de obligatoriedad del campo fecha_fin se ejecute correctamente
        """
        s = Sprint(
            sprintNumber=9,
            fecha_inicio='2021-07-25',
            #fecha_fin='2021-07-26'
        )
        self.assertTrue(s.validate_test(),"Debe ingresar la fecha fin del sprint")



    def test_fechasSprintValida(self):
        """
        Test: Validacion de inicio y fin de sprint
        """
        sprint1 = Sprint(sprintNumber=7, fecha_inicio='25/07/2021', fecha_fin='26/07/2021')
        fechIni = time.strptime(sprint1.fecha_inicio, "%d/%m/%Y")
        fechFin = time.strptime(sprint1.fecha_fin, "%d/%m/%Y")
        self.assertLessEqual(fechIni, fechFin, "Fecha no valida. fecha inicio debe ser menor a fecha fin")

    def test_crearRol(self):
        """
        Test de creacion de Rol llamado rolNuevo con permiso para agregar proyecto
        """
        rol1, created = Group.objects.get_or_create(name='rolNuevo')
        #Obtener el contenido de proyecto
        ct = ContentType.objects.get_for_model(Proyecto)

        #permission = Permission.objects.create(codename='can_add_Proyecto',name='Can add Proyecto',content_type=ct)
        permission = Permission.objects.filter(codename='can_add_Proyecto').first()
        if permission:
            rol1.permissions.add(permission)

        self.assertIsNotNone(rol1)

    def test_crearUserStory(self):
        nuevoUS = Historia(id_historia=3,nombre='Historia 1',descripcion='Historia de prueba',prioridad='ALTA',
                           fecha_creacion='2021/09/02',horasEstimadas=20,estados='PENDIENTE',horas_dedicadas=50)
        self.assertIsNotNone(nuevoUS)


print(__name__)
if __name__ == '__main__':
    TestCase.main()








