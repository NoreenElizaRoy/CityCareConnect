from django.urls import path
from .views import ComplaintView,ComplaintEdit,TrackComplaint

app_name="Complaints"
urlpatterns=[
    path('complaint_create',ComplaintView.as_view(),name='complaint_create'),
    path('complaint_view',ComplaintView.as_view(),name='complaint_view'),
    path('complaint_update/<int:complaint_id>',ComplaintEdit.as_view(),name='complaint_update'),
    path('complaint_delete/<int:complaint_id>',ComplaintEdit.as_view(),name='complaint_delete'),
    path('complaint_track/<int:complaint_id>',TrackComplaint.as_view(),name='complaint_track')
]
