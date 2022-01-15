from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='index'),
    path('register',views.register,name='register'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('user_login',views.user_login,name='user_login'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('password',views.change_password,name="password"),
    path('update_profile',views.update_profile,name='update_profile'),
    path('complaint',views.complaint,name="complaint"),
    path('feedback',views.feedback,name="feedback"),
    path('requirement',views.requirement,name="requirement"),
    path('requirement_view',views.requirement_view,name="requirement_view"),
    path('update_requirement/<int:requirement_id>',views.update_requirement,name='update_requirement'),
    path('view_complaints',views.view_complaints,name='view_complaints'),
    path('chat',views.chat,name='chat'),
    path('admin_chat',views.admin_chat,name="admin_chat"),
    path('leave',views.leave,name="leave"),
    path('leave_list',views.leave_list,name="leave_list"),
    path('previous_work',views.previous_work,name="previous_work"),
    path('profile',views.profile,name="profile"),



]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)