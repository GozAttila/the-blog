from .views import ReportCreateView, ReportListView, ReportActionView

from django.urls import path

urlpatterns = [
    path('create/<str:content_type>/<int:object_id>/', ReportCreateView.as_view(), name='api-report-create'),
    path('', ReportListView.as_view(), name='report-list'),
    path('action/<int:report_id>/', ReportActionView.as_view(), name='report-action'),
]
