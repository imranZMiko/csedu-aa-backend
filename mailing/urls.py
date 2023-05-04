from django.urls import path
from mailing.views import SystemMailList, SystemMailDetail, UserMailList, UserMailDetail, SendEmailToUser, AdminSendEmailToMultipleUser, UserSentMailList

urlpatterns = [
    # only for admins
    path('system/', SystemMailList.as_view(), name='system-mail-list'),
    path('system/<int:pk>/', SystemMailDetail.as_view(), name='system-mail-detail'),
    path('user/', UserMailList.as_view(), name='user-mail-list'),
    path('admin-send/', AdminSendEmailToMultipleUser.as_view(), name='send-email-to-multiple-user'),

    # users can access these too
    path('user/<int:pk>/', UserMailDetail.as_view(), name='user-mail-detail'),
    path('send/<str:username>/', SendEmailToUser.as_view(), name='send-email-to-user'),
    path('sent-mails/', UserSentMailList.as_view(), name='user-sent-mail-list'),
]
