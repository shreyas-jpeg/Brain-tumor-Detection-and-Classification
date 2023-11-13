from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('index', views.index, name='index'),
    path('about', views.about, name="about"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('contact', views.contact, name='contact'),
    path('manage', views.manage, name='manage'),
    path('upload_images', views.upload_images, name='upload_images'),
    path('update_model_data', views.update_model_data, name='update_model_data'),
    path('delete_pics/<patient_id>', views.delete_pics, name="delete_pics"),
    path('update_pics/<patient_id>', views.update_pics, name="update_pics"),
    path('rerun_prediction/<patient_id>', views.rerun_prediction, name="rerun_prediction"),
    path('run_report/<patient_id>', views.run_report, name="run_report"),
]