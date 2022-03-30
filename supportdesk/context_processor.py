import re
from .models import SupportTicket

def my_tickets(request):
    if request.user.is_staff: 
        mytickets = SupportTicket.objects.filter(assign_to =request.user)
        return {'mytickets':mytickets}
    else:
        return {'mytickets':[]}

def tickets(request):
    if request.user.is_staff:
        tickets = SupportTicket.objects.all().exclude(level='completed')
        return {'uncompleted_ticket': tickets}

    else:
        return {'uncompleted_ticket': []}

def customer_tickets(request):
    if not request.user.is_staff:
        tickets = SupportTicket.objects.filter(created_by=request.user)
        
        return {'customer_tickets': tickets}
    
    else:
        return {'customer_tickets': []}
