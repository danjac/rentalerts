from django.conf import settings
from django.core.mail import send_mail
from django.template import Context, RequestContext, loader


def send_email_from_template(subject, recipient_list, 
        template, context, from_email=None, *args, **kwargs):

    if from_email is None:
        from_email = settings.SERVER_EMAIL

    subject = settings.EMAIL_SUBJECT_PREFIX + subject

    template = loader.get_template(template)

    message = template.render(context)

    return send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        *args, **kwargs
    )


