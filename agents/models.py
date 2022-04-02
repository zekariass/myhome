from django.db import models
from django.conf import settings
from commons import models as cmn_models
from django.utils import timezone
import os


def get_agent_logo_file_path(instance, filename):
    now = timezone.now()
    basename, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond//1000
    return f"agents/logos/{instance.pk}/{now:%Y%m%d%H%M%S}{milliseconds}{extension}"


"""Logo image for the agent"""
class AgentLogo(models.Model):
    logo = models.ImageField(verbose_name="agent logo", upload_to=get_agent_logo_file_path)
    uploaded_on = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.uploaded_on

"""Agent is who list properties to the system"""
class Agent(models.Model):
    name = models.CharField(verbose_name='agent name', max_length=100, blank=False, null=False)
    # manager = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    address = models.OneToOneField(cmn_models.Address, on_delete=models.SET_NULL, null=True)
    email = models.EmailField(verbose_name='contact email address', null=False, blank=False)
    contact_number = models.CharField(verbose_name='contact phone number', max_length=50, null=False, blank=False)
    slogan = models.CharField(verbose_name='agent slogan', max_length=100, null=True, blank=True)
    description = models.TextField()
    logo = models.OneToOneField(AgentLogo, on_delete=models.SET_NULL, null=True, blank=True)
    registered_on = models.DateField(default=timezone.now, editable=False)

    def __str__(self):
        return self.name

"""Aditional admin users added by the main agent administrator"""
class AgentAdmin(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, verbose_name='agent where admin works')
    admin = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    is_manager = models.BooleanField(verbose_name="is admin the main manager?", default=False)
    date_added = models.DateField(default=timezone.now, editable=False)

    def __str__(self):
        return '%s %s' % (self.agent.name, self.admin.first_name)

"""Agent's Message Preference"""
class AgentMessagePreference(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    opt_out_in_app_message = models.BooleanField(default=False, blank=True)
    opt_out_sms_message = models.BooleanField(default=False, blank=True)
    opt_out_email_message = models.BooleanField(default=False, blank=True)


    def __str__(self):
        return 'inapp=%s, sms=%s, email=%s' % (self.opt_out_in_app_message, self.opt_out_sms_message, self.opt_out_email_message)

    
"""In-System message that is sent between the user and agent and agent and system admin"""
class Message(models.Model):
    SENDER_PARTY = [
        ("USER", "User"),
        ("AGENT", "Agent")
    ]
    initiator_uer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='received_messages')
    sender_party = models.CharField(verbose_name="Who send the message?", choices=SENDER_PARTY, null=False, max_length=50)
    message = models.TextField(null=False, blank=False)
    sent_on = models.DateTimeField(default=timezone.now, editable=False)
    read = models.BooleanField(verbose_name="Does the receiver read the message?", default=False)

    def __str__(self):
        return self.message
