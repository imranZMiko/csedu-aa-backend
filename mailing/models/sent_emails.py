from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from users.models import User
from mailing.models.email import CommonEmailAddress
import smtplib, re
from django.utils import timezone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
import logging

logger = logging.getLogger(__name__)

class CommonMailManager(models.Manager):
    def create_and_send_mail(self, sender, recipients, subject, body):
        """
        Creates a new CommonMail instance and sends it using Django's send_mail function.
        Returns the newly created CommonMail instance.
        """
        try:
            # Split the recipients string into a list of email addresses
            recipient_emails = [email.strip() for email in re.split(r'[;, ]+', recipients) if email.strip()]

            # Validate the email addresses
            for email in recipient_emails:
                validate_email(email)

            # Create a new CommonMail instance
            mail = CommonMail.objects.create(sender=sender, subject=subject, body=body, sent_at=None)

            # Add recipients to the mail instance
            for email in recipient_emails:
                recipient, created = CommonEmailAddress.objects.get_or_create(email=email)
                mail.recipients.add(recipient)

            # logger.info(settings.EMAIL_HOST_USER)
            # Send the email using Django's send_mail function
            try:
                send_mail(
                    subject=subject,
                    message=body,
                    from_email= f"CSEDU Connect <{sender.email_address}>",
                    recipient_list=recipient_emails,
                    fail_silently=False,
                )
            except smtplib.SMTPException as e:
                # Set the is_sent flag to False to indicate that the email failed to send
                mail.is_sent = False
                mail.save()
                raise e

            # Update the is_sent field to indicate that the email was successfully sent
            mail.sent_at = timezone.now()
            mail.is_sent = True
            mail.save()

            return mail

        except ValidationError as e:
            raise ValueError(str(e))

class CommonMail(models.Model):
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sent_common_mails')
    recipients = models.ManyToManyField(CommonEmailAddress, related_name='received_common_mails')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(null=True)
    is_sent = models.BooleanField(default=False)

    objects = CommonMailManager()

    def __str__(self):
        return f'{self.sent_at} - {self.sender.username} - {self.subject}'

class UserMailManager(models.Manager):
    def create_and_send_mail(self, sender, usernames, subject, body):
        """
        Creates a new UserMail instance and sends it to the specified users using Django's send_mail function.
        Returns the newly created UserMail instance.
        """
        # Get the User objects for the specified usernames
        recipients = User.objects.filter(username__in=usernames)

        # Check that all usernames were found
        if recipients.count() != len(usernames):
            raise ValueError('One or more usernames were not found.')

        # Create a new UserMail instance
        mail = UserMail.objects.create(sender=sender, recipients=usernames, subject=subject, body=body, sent_at=None)

        # Send the email using Django's send_mail function
        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient.email_address for recipient in recipients],
                fail_silently=False,
                auth_user=settings.EMAIL_HOST_USER,
                auth_password=settings.EMAIL_HOST_PASSWORD,
            )
        except smtplib.SMTPException as e:
            # Set the is_sent flag to False to indicate that the email failed to send
            mail.is_sent = False
            mail.save()
            raise e

        # Update the is_sent field to indicate that the email was successfully sent
        mail.sent_at = timezone.now()
        mail.is_sent = True
        mail.save()

        return mail

class UserMail(models.Model):
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sent_user_mails')
    recipients = models.ManyToManyField(User, related_name='received_user_mails')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(null=True)
    is_sent = models.BooleanField(default=False)

    objects = UserMailManager()

    def __str__(self):
        return f'{self.sent_at} - {self.sender.username} - {self.subject}'
