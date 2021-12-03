from django.core.mail import send_mail
from gestionUsuario.models import User, UserProyecto, UserSprint
from proyectos.models import Proyecto
from Sprints.models import Sprint
from userStory.models import Historia
from is2 import settings
from django.contrib.auth.models import Group

#email 1.1
#funca
def email_nuevoProyecto(proyecto,miembros):
    """
    Correo que notifica al usuario cuando es agregado a un proyecto

    :param proyecto: Proyecto al que fue agregado
    :param miembros: Los usuarios que recibiran el correo
    :return: void
    """
    #print("\nCorreo aviso, agregado a un nuevo proyecto\n")
    for miembro in miembros:
        u = User.objects.get(email=miembro)
        asunto = "Nuevo Proyecto!!"
        mensaje = "Hola " + u.first_name +" "+u.last_name+", has sido agregado al proyecto '" + proyecto.nombre + "'\n El proyecto se estima que inicie el " + str(
            proyecto.fecha)
        de = settings.EMAIL_HOST_USER
        destino = [u.email]
        send_mail(asunto, mensaje, de, destino)
        #print(mensaje)


def email_excluidoDelProyecto(proyecto,miembros):
    """
    Correo que notifica al usuario cuando es excluido de un proyecto

    :param proyecto: Proyecto
    :param miembros: Los usuarios que recibiran el correo
    :return: void
    """

    #print("\nCorreo aviso, que ha sido excluido del proyecto\n")

    for miembro in miembros:
        u = User.objects.get(email=miembro)
        asunto = "Apartado del Proyecto!!"
        mensaje = "Hola " + u.first_name +" "+u.last_name+", has sido apartado del proyecto '" + proyecto.nombre + "'"
        de = settings.EMAIL_HOST_USER
        destino = [u.email]
        send_mail(asunto, mensaje, de, destino)
        #print(mensaje)


#email 1.2
#funca
def email_rolAsignado(u, grupo, proyecto):
    """
    Correo que notifica al usuario que fue asignado con un rol en el proyecto

    :param u: usuario
    :param grupo: rol
    :param proyecto: proyecto
    :return: void
    """

    #print("\nCorreo rol Asignado\n")
    asunto = "Rol Asignado"
    mensaje = "Hola " + u.first_name + " " + u.last_name + ", has sido asignado como '"+grupo.name+ "' del proyecto '" + proyecto.nombre + "'"
    de = settings.EMAIL_HOST_USER
    destino = [u.email]
    send_mail(asunto, mensaje, de, destino)
    #print(mensaje)

#email 2
#funca
def email_historiaAsignado(historia, id_proyecto, encargado):
    """
    Correo que notifica al usuario cuando es asignado a una historia

    :param historia: User Story al que fue asignado
    :param id_proyecto: identificador de proyecto
    :param encargado: usuario que recibira el correo
    :return:
    """
    #print("\nCorreo historia asignada\n")
    p = Proyecto.objects.get(id=id_proyecto)

    asunto = "Encargado User Story"
    mensaje = "Hola " + encargado.first_name + " " + encargado.last_name + ", has sido asignado como encargado " \
                                             "de un nuevo User Story del proyecto '" + p.nombre + "'\n\n Nombre del User" \
                                             " Story: " + historia.nombre + "\n Fecha de creacion: " + str(
        historia.fecha_creacion)
    de = settings.EMAIL_HOST_USER
    destino = [encargado.email]
    send_mail(asunto, mensaje, de, destino)
    #print(mensaje)

#email 4
#funca
def email_actividadEnKanban(historia, id_proyecto, id_sprint, encargado, horasAgg, comentario,opcion):
    """
    Correo que notifica a los integrantes del sprint sobre las actividades en el kamban de sus compañeros

    :param historia: historia que fue modificada
    :param id_proyecto: identificador de proyecto
    :param id_sprint: identificador de sprint
    :param encargado: encargado de la historia
    :param horasAgg: horas agg en la historia
    :param comentario: comentarios agg en la historia
    :param opcion: opcion del que se elige cual de los correos predefinidos enviar
    :return: void
    """
    p = Proyecto.objects.get(id=id_proyecto)
    s = Sprint.objects.get(id=id_sprint)
    userSprints = UserSprint.objects.filter(sprint=s)
    miembros = []

    for usprint in userSprints:
        miembros.append(usprint.usuario)
    # email 5
    #oiko
    if (opcion == 2):
        #print("\nCorreo cuando un compañero de sprint mueve su US a en curso\n")
        for miembro in miembros:
            if (miembro.email != encargado.email):
                asunto = "Actividad en el Kanban, User Story en curso"
                mensaje = "Hola " + miembro.first_name + " " + miembro.last_name + ", se ha realizado una nueva actividad en el tablero kanban" \
                                                                                       " del proyecto '" + p.nombre + "'\n\n El usuario " + encargado.first_name + " " + encargado.last_name + " pasó el User Story '" + historia.nombre + "'\n a la columna 'EN CURSO'"
                de = settings.EMAIL_HOST_USER
                destino = [miembro.email]
                send_mail(asunto, mensaje, de, destino)
                #print(mensaje)
    # email 6
    #oiko
    if (opcion == 5):
        #print("\nCorreo cuando un compañero de sprint agg horas y comentario\n")
        for miembro in miembros:
            if (miembro.email != encargado.email):
                asunto = "Actividad en el Kanban"
                mensaje = "Hola " + miembro.first_name + " " + miembro.last_name + ", se ha realizado una nueva actividad en el tablero kanban" \
                                                                                       " del proyecto '" + p.nombre + "'\n\n El usuario "+encargado.first_name+" "+encargado.last_name+" agregó horas y comentario al User Story '" + historia.nombre + "'\n Horas agregadas: "+str(horasAgg)+" hs." \
                                                                                       "\n Comentario agregado: "+comentario
                de = settings.EMAIL_HOST_USER
                destino = [miembro.email]
                send_mail(asunto, mensaje, de, destino)
                #print(mensaje)
    # email 7
    #oiko
    if (opcion == 3):
        #print("\nCorreo cuando un compañero de sprint mueve su US a finalizado\n")
        for miembro in miembros:
            if (miembro.email != encargado.email):
                asunto = "Actividad en el Kanban, User Story finalizado"
                mensaje = "Hola " + miembro.first_name + " " + miembro.last_name + ", se ha realizado una nueva actividad en el tablero kanban" \
                                                                                   " del proyecto '" + p.nombre + "'\n\n El usuario " + encargado.first_name + " " + encargado.last_name + " movió el User Story '" + historia.nombre + "'\n a la columna 'FINALIZADO'"
                de = settings.EMAIL_HOST_USER
                destino = [miembro.email]
                send_mail(asunto, mensaje, de, destino)
                #print(mensaje)
    # email 7.0
    #oiko
    if (opcion == 1):
        #print("\nCorreo cuando un compañero de sprint mueve su US a en pendiente\n")
        for miembro in miembros:
            if (miembro.email != encargado.email):
                asunto = "Actividad en el Kanban, User Story pendiente"
                mensaje = "Hola " + miembro.first_name + " " + miembro.last_name + ", se ha realizado una nueva actividad en el tablero kanban" \
                                                                                   " del proyecto '" + p.nombre + "'\n\n El usuario " + encargado.first_name + " " + encargado.last_name + " movió el User Story '" + historia.nombre + "'\n a la columna 'PENDIENTE'"
                de = settings.EMAIL_HOST_USER
                destino = [miembro.email]
                send_mail(asunto, mensaje, de, destino)
                #print(mensaje)

#email 9
def email_actividadEnQA(historia,id_proyecto,id_sprint,opcion,scrumMaster):
    """
    Correo que notifica las actividades en el QA

    :param historia: historia
    :param id_proyecto: identificador de proyecto
    :param id_sprint: identificador de sprint
    :param opcion: opcion del que se elige cual de los correos predefinidos enviar
    :param scrumMaster: Scrum master que realizo la actividad
    :return:void
    """

    p = Proyecto.objects.get(id=id_proyecto)
    s = Sprint.objects.get(id=id_sprint)
    userSprints = UserSprint.objects.filter(sprint=s)
    miembros = []

    for usprint in userSprints:
        miembros.append(usprint.usuario)

    encargado = historia.encargado

    # email 9.1
    #oiko
    if (opcion == 6):
        #print("\nCorreo cuando un scrum master acepta un US\n")
        asunto = "User Story aceptado!!"
        mensaje = "Hola " + encargado.first_name + " " + encargado.last_name + ", el User Story '"+historia.nombre+"'" \
                                                                           " del proyecto '" + p.nombre + "' en el que estas como encargado, ha sido aceptado por el Scrum Master "+scrumMaster.first_name + " " + scrumMaster.last_name
        de = settings.EMAIL_HOST_USER
        destino = [encargado.email]
        send_mail(asunto, mensaje, de, destino)
        #print(mensaje)

    # email 9.2
    #oiko
    if (opcion == 7):
        #print("\nCorreo cuando un scrum master rechaza un US\n")
        asunto = "User Story rechazado"
        mensaje = "Hola " + encargado.first_name + " " + encargado.last_name + ", el User Story '" + historia.nombre + "'" \
                                                                          " del proyecto '" + p.nombre + "' del que estas como encargado, ha sido rechazado por el Scrum Master " + scrumMaster.first_name + " " + scrumMaster.last_name +"\n\n " \
                                                                                                                                                                                                                                           "Motivo de rechazo: "+historia.extraData
        de = settings.EMAIL_HOST_USER
        destino = [encargado.email]
        send_mail(asunto, mensaje, de, destino)
        #print(mensaje)

    # email 9.3

#oiko
def sprintVerificado(id_proyecto,id_sprint,scrumMaster):
    """
    Correo que notifica a los integrantes de un sprint cuando un scrum master verifica el sprint

    :param id_proyecto: identificador de proyecto
    :param id_sprint: identificador de sprint
    :param scrumMaster: scrum master del proyecto
    :return: void
    """
    p = Proyecto.objects.get(id=id_proyecto)
    s = Sprint.objects.get(id=id_sprint)
    userSprints = UserSprint.objects.filter(sprint=s)
    miembros = []

    #print("\nCorreo cuando un scrum master verifica un sprint\n")

    for usprint in userSprints:
        miembros.append(usprint.usuario)

    for miembro in miembros:
        asunto = "Sprint Verificado"
        mensaje = "Hola " + miembro.first_name + " " + miembro.last_name + ", el sprint 'Nro. " + str(
            s.sprintNumber) + "' del proyecto '" + p.nombre + "' del que formas parte" \
                                                              ", ha sido marcado como verificado por el Scrum Master " + scrumMaster.first_name + " " + scrumMaster.last_name
        de = settings.EMAIL_HOST_USER
        destino = [miembro.email]
        send_mail(asunto, mensaje, de, destino)
        #print(mensaje)

#email 10
#oiko pero no usamos
def email_nuevoSprint(id_proyecto, id_sprint, usuario):
    """
    Correo que notifica al usuario cuando se le agrega a un sprint

    :param id_proyecto: identificador de proyecto
    :param id_sprint: identificador de sprint
    :param usuario: usuario que recibira el correo
    :return: void
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    sprint = Sprint.objects.get(id=id_sprint)
    #print("\nCorreo cuando se le agrega a un sprint\n")
    #for miembro in miembros:

    asunto = "Nuevo Sprint!!"
    mensaje = "Hola " + usuario.first_name +" "+usuario.last_name+", has sido agregado al sprint Nro. '" + str(sprint.sprintNumber) + "' del proyecto '"+proyecto.nombre+"' la fecha de inicio esperado de este sprint es el" + str(sprint.fecha_inicio)
    de = settings.EMAIL_HOST_USER
    destino = [usuario.email]
    send_mail(asunto, mensaje, de, destino)
    #print(mensaje)

#email 11 y 12
def email_sprintExtFin(id_proyecto,id_sprint,opcion,scrumMaster):
    """
    Correo que notifica cuando un sprint se finaliza o se extiende

    :param id_proyecto: identificador de proyecto
    :param id_sprint: identificador de spirnt
    :param opcion: define cual de los correos se envia
    :param scrumMaster: Scrum master del proyecto
    :return: void
    """
    p = Proyecto.objects.get(id=id_proyecto)
    s = Sprint.objects.get(id=id_sprint)
    userSprints = UserSprint.objects.filter(sprint=s)
    miembros = []

    for usprint in userSprints:
        miembros.append(usprint.usuario)

    # email 11
    #oiko
    if (opcion == 'expandir'):
        #print("\nCorreo cuando un sprint se extiende\n")
        for miembro in miembros:
            asunto = "Sprint Extendido"
            mensaje = "Hola " + miembro.first_name + " " + miembro.last_name + ", el sprint 'Nro. "+str(s.sprintNumber)+"' del proyecto '" + p.nombre + "en el que formas parte" \
                                                            ", ha sido EXTENDIDO por el Scrum Master " + scrumMaster.first_name + " " + scrumMaster.last_name+" \n\nFecha de finalizacion actualizado del sprint: "+str(s.fecha_fin)
            de = settings.EMAIL_HOST_USER
            destino = [miembro.email]
            send_mail(asunto, mensaje, de, destino)
            #print(mensaje)

    # email 12
    #oiko
    if (opcion == 'finalizar'):
        #print("\nCorreo cuando un sprint se finaliza\n")
        for miembro in miembros:
            asunto = "Sprint Finalizado!!"
            mensaje = "Hola " + miembro.first_name + " " + miembro.last_name + ", el sprint 'Nro. " + str(s.sprintNumber) + "' del proyecto '" + p.nombre + "' del que formas parte" \
                                                                                                                                                       ", ha sido FINALIZADO por el Scrum Master " + scrumMaster.first_name + " " + scrumMaster.last_name
            de = settings.EMAIL_HOST_USER
            destino = [miembro.email]
            send_mail(asunto, mensaje, de, destino)
            #print(mensaje)

# email 13 y 17
#oiko
def email_proyectoFin(id_proyecto):
    """
    Correo que notifica la finalizacion de un proyecto a los integrates

    :param id_proyecto: identificador de proyecto
    :return: void
    """
    #print("\nCorreo cuando un proyecto se finaliza\n")
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
        #print(mensaje)

# email 14 y 18
#oiko
def email_proyectoIni(id_proyecto):
    """
    Correo que notifica la finalizacion de un proyecto a los integrantes

    :param id_proyecto:
    :return:
    """
    #print("\nCorreo cuando un proyecto se inicia\n")
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
        #print(mensaje)

# email 19
#oiko
def email_sprintCreado(id_proyecto, id_sprint):
    """
    Correo que notifica al Product Owner cuando se crea correctamente el sprint

    :param id_proyecto: identificador de proyecto
    :param id_sprint: identificador de sprint
    :return: void
    """
    #print("\nCorreo al prodcut owner cuando un sprint se crea\n")
    p = Proyecto.objects.get(id=id_proyecto)
    s = Sprint.objects.get(id=id_sprint)
    lista_usuarios = User.objects.all()

    for usuario in lista_usuarios:
        if(usuario.is_superuser):
            asunto = "Nuevo sprint creado!!"
            mensaje = "Hola " + usuario.first_name + " " + usuario.last_name + ", se creó un nuevo sprint en el proyecto '" + p.nombre + "'\n\n Nro de sprint: "+str(s.sprintNumber)+" \n " \
                                                                        "Fecha de inicio estimado: "+ str(s.fecha_inicio) +"\n Fecha de finalizacion esperada: "+str(s.fecha_fin)
            de = settings.EMAIL_HOST_USER
            destino = [usuario.email]
            send_mail(asunto, mensaje, de, destino)
            #print(mensaje)


# email 20
#oiko
def email_sprintIniciado(id_proyecto, id_sprint):
    """
    Correo que notifica al Product Owner cuando se inicia un sprint

    :param id_proyecto: identificador de proyecto
    :param id_sprint: identificador de sprint
    :return: void
    """
    #print("\nCorreo al prodcut owner cuando un sprint se inicia\n")

    p = Proyecto.objects.get(id=id_proyecto)
    s = Sprint.objects.get(id=id_sprint)
    lista_usuarios = User.objects.all()

    for usuario in lista_usuarios:
        if(usuario.is_superuser):
            asunto = "Sprint iniciado!!"
            mensaje = "Hola " + usuario.first_name + " " + usuario.last_name + ", el sprint Nro. "+str(s.sprintNumber)+" del proyecto '" + p.nombre + "' ha iniciado"
            de = settings.EMAIL_HOST_USER
            destino = [usuario.email]
            send_mail(asunto, mensaje, de, destino)
            #print(mensaje)

# email 21
#oiko
def email_sprintFinalizado(id_proyecto, id_sprint):
    """
    Correo que notifica al Product Owner cuando se finaliza un sprint

    :param id_proyecto: identificador de proyecto
    :param id_sprint: identificador de sprint
    :return: void
    """
    #print("\nCorreo cuando un proyecto se finaliza\n")
    p = Proyecto.objects.get(id=id_proyecto)
    s = Sprint.objects.get(id=id_sprint)
    lista_usuarios = User.objects.all()

    for usuario in lista_usuarios:
        if(usuario.is_superuser):
            asunto = "Sprint finalizado!!"
            mensaje = "Hola " + usuario.first_name + " " + usuario.last_name + ", el sprint Nro. "+str(s.sprintNumber)+" del proyecto '" + p.nombre + "' ha finalizado"
            de = settings.EMAIL_HOST_USER
            destino = [usuario.email]
            send_mail(asunto, mensaje, de, destino)
            #print(mensaje)