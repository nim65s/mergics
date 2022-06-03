from django.urls import path

from . import views

app_name = "mergics"
urlpatterns = [
    path("inputs/list", views.InputListView.as_view(), name="icsinputs"),
    path("inputs/create", views.InputCreateView.as_view(), name="icsinput-add"),
    # path('inputs/detail/<pk>', views.InputDetailView.as_view(), name='icsinput'),
    # path('inputs/update/<pk>', views.InputUpdateView.as_view(),
    # name='icsinput-update'),
    # path('inputs/delete/<pk>', views.InputDeleteView.as_view(),
    # name='icsinput-delete'),
    path("outputs/list", views.OutputListView.as_view(), name="icsoutputs"),
    path("outputs/create", views.OutputCreateView.as_view(), name="icsoutput-add"),
    path("outputs/detail/<slug>", views.OutputDetailView.as_view(), name="icsoutput"),
    path(
        "outputs/update/<slug>",
        views.OutputUpdateView.as_view(),
        name="icsoutput-update",
    ),
    # path('outputs/delete/<slug>', views.OutputDeleteView.as_view(),
    # name='icsoutput-delete'),
    path("public/<str:username>-<slug:slug>.ics", views.ics, name="ics"),
]
