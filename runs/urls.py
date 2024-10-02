from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("runs/", views.run_list, name="run_list"),
    path("add_run/", views.add_run, name="add_run"),
    path("yearly_total/", views.yearly_total, name="yearly_total"),
    path("weekly_total/", views.weekly_total, name="weekly_total"),
    path("yearly-distance-data/", views.yearly_distance_data, name="yearly_distance_data"),
    path("delete-run/<int:run_id>/", views.delete_run, name="delete_run"),
    path("cumulative-distance-data/", views.cumulative_distance_data, name="cumulative_distance_data"),
]
