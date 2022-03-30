from django.urls import path
from . import views

urlpatterns = [
    path('',views.landing,name='landing'),
    path("home/", views.PlaceholderHome.as_view(), name="supportdesk_placeholder"),
    path('customer/support-ticket/',views.CustomerCreateTicketView.as_view(),name='create-ticket'),
    path('customer/ticket-list/',views.CustomerTicketListView.as_view(),name='ticket-list'),
    path('agent/support-list',views.AgentSupportListView.as_view(),name='agent-list'),
    path('agent/support-detail/<int:pk>/',views.AgentSupportDetailView.as_view(),name='agent-detail'),
    path('agent/my-tickets/',views.my_tickets,name='my-tickets'),
    path('agent/reasign/ticket/<int:pk>/',views.reasign_view,name='reasign'),
]
