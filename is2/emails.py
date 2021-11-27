from django.core.mail import send_mail
from gestionUsuario.models import User, UserProyecto, UserSprint
from proyectos.models import Proyecto
from Sprints.models import Sprint
from userStory.models import Historia
from is2 import settings
from django.contrib.auth.models import Group

#email 1.1
def email_nuevoProyecto(proyecto,miembros):

    for miembro in miembros:
        u = User.objects.get(email=miembro)
        asunto = "Nuevo Proyecto!!"
        mensaje = "Hola " + u.first_name +" "+u.last_name+", has sido agregado al proyecto '" + proyecto.nombre + "'\n El proyecto se estima que inicie el " + str(
            proyecto.fecha)
        de = settings.EMAIL_HOST_USER
        destino = [u.email]
        send_mail(asunto, mensaje, de, destino)

#email 1.2
def email_rolAsignado(u, grupo, proyecto):

    asunto = "Rol Asignado"
    mensaje = "Hola " + u.first_name + " " + u.last_name + ", has sido asignado como '"+grupo.name+ "' del proyecto '" + proyecto.nombre + "'"
    de = settings.EMAIL_HOST_USER
    destino = [u.email]
    send_mail(asunto, mensaje, de, destino)

#email 2
def email_historiaAsignado(historia, id_proyecto, encargado):

    p = Proyecto.objects.get(id=id_proyecto)

    asunto = "Encargado User Story"
    mensaje = "Hola " + encargado.first_name + " " + encargado.last_name + ", has sido asignado como encargado " \
                                             "de un nuevo User Story del proyecto '" + p.nombre + "'\n\n Nombre del User" \
                                             " Story: " + historia.nombre + "\n Fecha de creacion: " + str(
        historia.fecha_creacion)
    de = settings.EMAIL_HOST_USER
    destino = [encargado.email]
    send_mail(asunto, mensaje, de, destino)

#email 4
def email_actividadEnKanban(historia, id_proyecto, id_sprint, encargado, horasAgg, comentario,opcion):

    p = Proyecto.objects.get(id=id_proyecto)
    s = Sprint.objects.get(id=id_sprint)
    userSprints = UserSprint.objects.filter(sprint=s)
    miembros = []

    for usprint in userSprints:
        miembros.append(usprint.usuario)
    # email 5
    if (opcion == 2):
        for miembro in miembros:
            if (miembro.email != encargado.email):
                asunto = "Actividad en el Kanban, User Story en curso"
                mensaje = "Hola " + miembro.first_name + " " + miembro.last_name + ", se ha realizado una nueva actividad en el tablero kanban" \
                                                                                       " del proyecto '" + p.nombre + "'\n\n El usuario " + encargado.first_name + " " + encargado.last_name + " pasó el User Story '" + historia.nombre + "'\n a la columna 'EN CURSO'"
                de = settings.EMAIL_HOST_USER
                destino = [miembro.email]
                send_mail(asunto, mensaje, de, destino)
    # email 6
    if (opcion == 5):
        for miembro in miembros:
            if (miembro.email != encargado.email):
                asunto = "Actividad en el Kanban"
                mensaje = "Hola " + miembro.first_name + " " + miembro.last_name + ", se ha realizado una nueva actividad en el tablero kanban" \
                                                                                       " del proyecto '" + p.nombre + "'\n\n El usuario "+encargado.first_name+" "+encargado.last_name+" agregó horas y comentario al User Story '" + historia.nombre + "'\n Horas agregadas: "+horasAgg+" hs." \
                                                                                       "\n Comentario agregado: "+comentario
                de = settings.EMAIL_HOST_USER
                destino = [miembro.email]
                send_mail(asunto, mensaje, de, destino)
    # email 7
    if (opcion == 3):
        for miembro in miembros:
            if (miembro.email != encargado.email):
                asunto = "Actividad en el Kanban, User Story finalizado"
                mensaje = "Hola " + miembro.first_name + " " + miembro.last_name + ", se ha realizado una nueva actividad en el tablero kanban" \
                                                                                   " del proyecto '" + p.nombre + "'\n\n El usuario " + encargado.first_name + " " + encargado.last_name + " movió el User Story '" + historia.nombre + "'\n a la columna 'FINALIZADO'"
                de = settings.EMAIL_HOST_USER
                destino = [miembro.email]
                send_mail(asunto, mensaje, de, destino)
    # email 7.0
    if (opcion == 1):
        for miembro in miembros:
            if (miembro.email != encargado.email):
                asunto = "Actividad en el Kanban, User Story pendiente"
                mensaje = "Hola " + miembro.first_name + " " + miembro.last_name + ", se ha realizado una nueva actividad en el tablero kanban" \
                                                                                   " del proyecto '" + p.nombre + "'\n\n El usuario " + encargado.first_name + " " + encargado.last_name + " movió el User Story '" + historia.nombre + "'\n a la columna 'PENDIENTE'"
                de = settings.EMAIL_HOST_USER
                destino = [miembro.email]
                send_mail(asunto, mensaje, de, destino)

#email 9
def email_actividadEnQA(historia,id_proyecto,id_sprint,opcion,scrumMaster):

    p = Proyecto.objects.get(id=id_proyecto)
    s = Sprint.objects.get(id=id_sprint)
    userSprints = UserSprint.objects.filter(sprint=s)
    miembros = []

    for usprint in userSprints:
        miembros.append(usprint.usuario)

    encargado = historia.encargado

    # email 9.1
    if (opcion == 6):
        asunto = "User Story aceptado!!"
        mensaje = "Hola " + encargado.first_name + " " + encargado.last_name + ", el User Story '"+historia.nombre+"'" \
                                                                           " el proyecto '" + p.nombre + " en el que estas como encargado, ha sido aceptado por el Scrum Master "+scrumMaster.first_name + " " + scrumMaster.last_name
        de = settings.EMAIL_HOST_USER
        destino = [encargado.email]
        send_mail(asunto, mensaje, de, destino)

    # email 9.2
    if (opcion == 7):
        asunto = "User Story rechazado"
        mensaje = "Hola " + encargado.first_name + " " + encargado.last_name + ", el User Story '" + historia.nombre + "'" \
                                                                          " del proyecto '" + p.nombre + " en el que estas como encargado, ha sido rechazado por el Scrum Master " + scrumMaster.first_name + " " + scrumMaster.last_name
        de = settings.EMAIL_HOST_USER
        destino = [encargado.email]
        send_mail(asunto, mensaje, de, destino)

    # email 9.3
    if (opcion == 8):
        for miembro in miembros:
            asunto = "Sprint Verificado"
            mensaje = "Hola " + miembro.first_name + " " + miembro.last_name + ", el sprint 'Nro. "+s.sprintNumber+"' del proyecto '" + p.nombre + "en el que formas parte" \
                                                            ", ha sido verificado por el Scrum Master " + scrumMaster.first_name + " " + scrumMaster.last_name
            de = settings.EMAIL_HOST_USER
            destino = [miembro.email]
            send_mail(asunto, mensaje, de, destino)

#email 10
def email_nuevoSprint(id_proyecto, id_sprint, miembros):

    proyecto = Proyecto.objects.get(id=id_proyecto)
    sprint = Sprint.objects.get(id=id_sprint)

    for miembro in miembros:

        asunto = "Nuevo Sprint!!"
        mensaje = "Hola " + miembro.first_name +" "+miembro.last_name+", has sido agregado al sprint Nro. '" + sprint.sprintNumber + "' del proyecto '"+proyecto.nombre+"' la fecha de inicio estimado de este sprint es el" + str(sprint.fecha_inicio)
        de = settings.EMAIL_HOST_USER
        destino = [miembro.email]
        send_mail(asunto, mensaje, de, destino)

#email 11 y 12
def email_sprintExtFin(id_proyecto,id_sprint,opcion,scrumMaster):

    p = Proyecto.objects.get(id=id_proyecto)
    s = Sprint.objects.get(id=id_sprint)
    userSprints = UserSprint.objects.filter(sprint=s)
    miembros = []

    for usprint in userSprints:
        miembros.append(usprint.usuario)

    # email 11
    if (opcion == 'expandir'):
        for miembro in miembros:
            asunto = "Sprint Extendido"
            mensaje = "Hola " + miembro.first_name + " " + miembro.last_name + ", el sprint 'Nro. "+s.sprintNumber+"' del proyecto '" + p.nombre + "en el que formas parte" \
                                                            ", ha sido EXTENDIDO por el Scrum Master " + scrumMaster.first_name + " " + scrumMaster.last_name
            de = settings.EMAIL_HOST_USER
            destino = [miembro.email]
            send_mail(asunto, mensaje, de, destino)

    # email 12
    if (opcion == 'finalizar'):
        for miembro in miembros:
            asunto = "Sprint Finalizado!!"
            mensaje = "Hola " + miembro.first_name + " " + miembro.last_name + ", el sprint 'Nro. " + s.sprintNumber + "' del proyecto '" + p.nombre + "en el que formas parte" \
                                                                                                                                                       ", ha sido FINALIZADO por el Scrum Master " + scrumMaster.first_name + " " + scrumMaster.last_name
            de = settings.EMAIL_HOST_USER
            destino = [miembro.email]
            send_mail(asunto, mensaje, de, destino)

# email 13 y 17
def email_proyectoFin(id_proyecto):

    p = Proyecto.objects.get(id=id_proyecto)
    usersProyecto = UserProyecto.objects.filter(proyecto=p)
    miembrosProy = []

    for userProyecto in usersProyecto:
        miembrosProy.append(userProyecto.usuario)

    for miembro in miembrosProy:
        asunto = "Proyecto finalizado!!"
        mensaje = "Hola " + miembro.first_name + " " + miembro.last_name + ", el proyecto '" + p.nombre + "' del que formas parte ha finalizado"
        de = settings.EMAIL_HOST_USER
        destino = [miembro.email]
        send_mail(asunto, mensaje, de, destino)

# email 14 y 18
def email_proyectoIni(id_proyecto):

    p = Proyecto.objects.get(id=id_proyecto)
    usersProyecto = UserProyecto.objects.filter(proyecto=p)
    miembrosProy = []

    for userProyecto in usersProyecto:
        miembrosProy.append(userProyecto.usuario)

    for miembro in miembrosProy:
        asunto = "Proyecto iniciado!!"
        mensaje = "Hola " + miembro.first_name + " " + miembro.last_name + ", el proyecto '" + p.nombre + "' del que formas parte ha iniciado"
        de = settings.EMAIL_HOST_USER
        destino = [miembro.email]
        send_mail(asunto, mensaje, de, destino)

# email 19
def email_sprintCreado(id_proyecto, id_sprint):

    p = Proyecto.objects.get(id=id_proyecto)
    s = Sprint.objects.get(id=id_sprint)
    lista_usuarios = User.objects.all()

    for usuario in lista_usuarios:
        if(usuario.is_superuser):
            asunto = "Nuevo sprint creado!!"
            mensaje = "Hola " + usuario.first_name + " " + usuario.last_name + ", se creó un nuevo sprint en el proyecto '" + p.nombre + "'\n\n Nro de sprint: "+s.sprintNumber+" \n " \
                                                                        "Fecha de inicio estimado: "+ str(s.fecha_inicio) +"\n Fecha de finalizacion esperada: "+str(s.fecha_fin)
            de = settings.EMAIL_HOST_USER
            destino = [usuario.email]
            send_mail(asunto, mensaje, de, destino)


# email 20
def email_sprintIniciado(id_proyecto, id_sprint):

    p = Proyecto.objects.get(id=id_proyecto)
    s = Sprint.objects.get(id=id_sprint)
    lista_usuarios = User.objects.all()

    for usuario in lista_usuarios:
        if(usuario.is_superuser):
            asunto = "Sprint iniciado!!"
            mensaje = "Hola " + usuario.first_name + " " + usuario.last_name + ", el sprint Nro. "+s.sprintNumber+" del proyecto '" + p.nombre + "' ha iniciado"
            de = settings.EMAIL_HOST_USER
            destino = [usuario.email]
            send_mail(asunto, mensaje, de, destino)


# email 21
def email_sprintFinalizado(id_proyecto, id_sprint):

    p = Proyecto.objects.get(id=id_proyecto)
    s = Sprint.objects.get(id=id_sprint)
    lista_usuarios = User.objects.all()

    for usuario in lista_usuarios:
        if(usuario.is_superuser):
            asunto = "Sprint finalizado!!"
            mensaje = "Hola " + usuario.first_name + " " + usuario.last_name + ", el sprint Nro. "+s.sprintNumber+" del proyecto '" + p.nombre + "' ha finalizado"
            de = settings.EMAIL_HOST_USER
            destino = [usuario.email]
            send_mail(asunto, mensaje, de, destino)