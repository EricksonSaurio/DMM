from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.models import Site
from premailer import transform
import os

def enviar_notificacion_correo(empleado, tarea):
    subject = f'Nueva tarea asignada: {tarea.titulo}'
    from_email = settings.DEFAULT_FROM_EMAIL
    to = empleado.email

    current_site = Site.objects.get_current()
    logo_url = f'http://{current_site.domain}/directora/static/images/logo.png'
    dashboard_url = f'http://{current_site.domain}/directora/listar-tareas/'

    # Cargar el CSS desde el archivo
    css_file_path = os.path.join(settings.BASE_DIR, '/directora/static/css/email_estilo.css')
    with open(css_file_path) as f:
        css_content = f.read()

    # Renderizar la plantilla HTML
    html_content = render_to_string('directora/tarea_asignada.html', {
        'empleado': empleado,
        'tarea': tarea,
        'logo_url': logo_url,
        'dashboard_url': dashboard_url,
        'css_url': f'http://{current_site.domain}/directora/static/css/email_estilo.css'
    })

    # Convertir CSS en línea usando Premailer
    html_content = transform(html_content, css_text=css_content)

    # Crear el correo electrónico
    email = EmailMultiAlternatives(subject, '', from_email, [to])
    email.attach_alternative(html_content, "text/html")
    email.send()
