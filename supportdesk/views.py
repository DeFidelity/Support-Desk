from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

from .forms import CustomerRequestForm
from .models import SupportTicket

def landing(request):
    return render(request,'supportdesk/landing.html')

class PlaceholderHome(LoginRequiredMixin,TemplateView):
  
        template_name = "supportdesk/placeholder.html"
     
    
class CustomerCreateTicketView(LoginRequiredMixin,UserPassesTestMixin,View):
    def get(self,request):
        form = CustomerRequestForm()
        context = {
            'form':form
            }
        return render(request,'supportdesk/request-form.html',context)
    
    def post(self,request,*args,**kwargs):
        form = CustomerRequestForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            creator = User.objects.get(pk=request.user.pk)
            ticket.created_by =creator
            ticket.save()

            return redirect('ticket-list')
        else:
            return render(request,'supportdesk/request-form.html')
        
    def test_func(self):
        return not self.request.user.is_staff
        
        
class CustomerTicketListView(LoginRequiredMixin,UserPassesTestMixin,View):
    def get(self,request):
        tickets = SupportTicket.objects.filter(created_by=request.user)
        
        context = {
            'tickets':tickets
        }
        
        return render(request,'supportdesk/tickets-list.html',context)
    
    def test_func(self):
        return not self.request.user.is_staff
    
    
class AgentSupportListView(LoginRequiredMixin,UserPassesTestMixin,View):
    def get(self,request):
        tickets = SupportTicket.objects.all().exclude(level='completed')
        completed = SupportTicket.objects.filter(level='completed')
        
        context = {
            'tickets':tickets,
            'completed':completed
        }
        
        return render(request,'supportdesk/agent-list.html',context)
    
    def test_func(self):
        return self.request.user.is_staff
    
class AgentSupportDetailView(LoginRequiredMixin,UserPassesTestMixin,View):
    def get(self,request,pk):
        ticket = get_object_or_404(SupportTicket,pk=pk)
        ticket.level = 'progress'
        
        if not ticket.assign_to:
            ticket.assign_to = request.user
        ticket.save()
        
        context = {
            'ticket': ticket
        }
        return render(request,'supportdesk/agent-detail.html',context)
    
    def post(self,request,pk,*args,**kwargs):
        ticket = get_object_or_404(SupportTicket,pk=pk,assign_to=request.user)
        
        if ticket.level == 'progress':
            
            ticket.level = 'completed'
            ticket.assign_to = request.user
            ticket.save()
            return HttpResponse('marked as completed')
        else:
            ticket.level = 'progress'
            ticket.assign_to = request.user
            ticket.save()
            return HttpResponse('ticket in progress')
      
        
    def test_func(self):
        return self.request.user.is_staff
    
    
def reasign_view(request,pk):
    ticket = get_object_or_404(SupportTicket,pk=pk)
    ticket.assign_to = None
    ticket.level = 'progress'
    ticket.save()
    return HttpResponse('Ticket now open')


def test_function(user):
    return user.is_staff
    
    
@login_required
@user_passes_test(test_function)
def my_tickets(request):
    tickets = SupportTicket.objects.filter(assign_to = request.user)
    context = {
        'tickets':tickets
    }
    return render(request,'supportdesk/my-tickets.html',context)

    
    
        
        