from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.core.mail import send_mail
from django.utils import timezone

from .models import ResetPassword


class ResetPasswordView(TemplateView):
    template_name = 'users/reset_password.html'

    def post(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        reset_record = ResetPassword(
            user=self.request.user,
            created=timezone.now()
        )
        reset_record.save()
        reset_id = reset_record.id
        link = 'http://127.0.0.1:8000/users/reset-password-confirm?id='
        
        send_mail(
            'Email Confirmation',
            'Please click on this link {}{} to reset your password'.format(link, reset_id),
            'isaiahnavasquez@gmail.com',
            ['isaiahjan_caracol@umindanao.edu.ph'],
            fail_silently=False
        )

        return render(self.request, self.template_name,{
            'message': 'Email Confirmation has been sent'
        })


class ConfirmResetPasswordview(TemplateView):
    template_name = 'users/confirm_reset_password.html'
    
    def get_context_data(self, **kwargs):
        request_id = self.request.GET['id']
        print('ID: __ __ __ ' + str(request_id))
    
    
    
    
