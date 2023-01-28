from django.urls import path, include
from django.contrib import admin


from . import views

urlpatterns = [
	path('admin/', admin.site.urls),

    path("", views.index, name="index"),

	path("about/", views.about, name="about"),
	path("contact/", views.contact, name="contact"),

	path("login/", views.login_user, name="login"),
	path("logout/", views.logout_user, name="logout"),


	path("users/", views.users, name="users"),
	path("edit_user/", views.edit_user, name="edit_user"),
	path("rpc/users/", views.users_rpc, name="users_rpc"),
	path("rpc/users234/", views.users_csv, name="users_csv"),

	path("presentation/<str:pres_id>", views.presentation_view, name="presentation_view"),
	path("manage_files/", views.manage_files, name="manage_files"),
	path("delete_files/<str:pres_id>/<str:filename>", views.delete_files, name="delete_files"),
	path("files/<str:pres_id>/<str:filename>", views.files, name="files"),

	path('calendar/<str:day>/', views.calendar_view, name="calendar"),
	path('filelist/', views.filelist, name="filelist"),

	path("template/", views.template, name="template"),
]
