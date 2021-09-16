import unittest
import time
from proyectos.models import Proyecto
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from gestionUsuario.models import User
from userStory.models import Historia

class Test(unittest.TestCase):

    """
    Clase de testeo de todos los models del sistema
    """

    def test_crearProyecto(self):
        """
        Test : Validacion de creacion del proyecto
        """
        nuevoProyecto = Proyecto(nombre='Primer Proyecto',descripcion='Proyecto de prueba',estado='PENDIENTE',fecha='25/07/2021',fecha_entrega='26/07/2021')
        self.assertIsNotNone(nuevoProyecto)


    def test_fechasProyectoValida(self):
        """
        Test: Validacion de inicio y fin de proyecto
        """
        proyecto1 = Proyecto(nombre='Prueba proyecto', fecha='25/07/2021', fecha_entrega='26/07/2021')
        fechIni = time.strptime(proyecto1.fecha, "%d/%m/%Y")
        fechFin = time.strptime(proyecto1.fecha_entrega, "%d/%m/%Y")
        self.assertLessEqual(fechIni, fechFin, "Fecha no valida. fecha inicio debe ser menor a entrega")


    def test_userAdmitido(self):
        """
        Test de usuario admitido a loggerarse al sistema
        """
        user = User()
        self.assertIsNotNone(user)

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

    def test_crearUsuario(self):
        nuevoUsuario = User()
        self.assertIsNotNone(nuevoUsuario)

    def test_crearUserStory(self):
        nuevoUS = Historia(id_historia=3,nombre='Historia 1',descripcion='Historia de prueba',prioridad='ALTA',
                           fecha_creacion='2021/09/02',horasEstimadas=20,estados='PENDIENTE',horas_dedicadas=50)
        self.assertIsNotNone(nuevoUS)


print(__name__)
if __name__ == '__main__':
    unittest.main()








