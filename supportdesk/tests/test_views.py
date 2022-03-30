from django.test import TestCase, Client 
from django.contrib.auth.models import User
from django.urls import reverse 
from ..models import SupportTicket 


class TestViewClasses(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.staff_user = User.objects.create_user(
            username='admin',
            first_name='new admin',
            password='testpassword',
            is_staff=True,
        )
        self.customer_user = User.objects.create_user(
            username='customer',
            first_name='new customer',
            password='testpassword',
            is_staff= False,
        )
        
        self.support_ticket = SupportTicket.objects.create(
            created_by = self.customer_user,
            summary = 'Need an upgrade in the sales funel',
            description= 'Sales are frowing and we are considering an upgrade in our funnel, we needs to take more ..',
            is_prioritized = True,
            assign_to = self.staff_user,
        )
        
    def test_landing_page(self):
        landing = reverse('landing')
        
        response = self.client.get(landing)
        
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed('supportdesk/landing.html')
        
    def test_placeholder_home_with_anon_user(self):
        placeholder = reverse('supportdesk_placeholder')
        
        response = self.client.get(placeholder)
        
        self.assertEquals(response.status_code,302)
        self.assertTemplateUsed("supportdesk/placeholder.html")
        
    def test_placeholder_home_with_customer_user(self):
        placeholder = reverse('supportdesk_placeholder')
        self.client.login(username=self.customer_user.username,password='testpassword')
        
        response = self.client.get(placeholder)
        
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed("supportdesk/placeholder.html")
        
    def test_customer_create_ticket_with_GET_method(self):
        create_ticket = reverse('create-ticket')
        
        self.client.login(username=self.customer_user.username,password='testpassword')
        response = self.client.get(create_ticket)
        
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed('supportdesk/request-form.html')
        self.assertTrue(response.context['form'])
        
    def test_customer_create_ticket_with_POST_method(self):
        create_ticket = reverse('create-ticket')
        
        self.client.login(username=self.customer_user.username,password='testpassword')
        response = self.client.post(create_ticket,data={
            'summary' : 'Need an upgrade in the sales funel',
            'description': 'Sales are frowing and we are considering an upgrade in our funnel, we needs to take more ..',
            'is_prioritized': False,
        })
        
        self.assertEquals(response.status_code,302)
        self.assertTemplateUsed('supportdesk/tickets-list.html')
    
    def test_customer_create_ticket_with_non_customer_user(self):
        create_ticket = reverse('create-ticket')
        
        self.client.login(username=self.staff_user.username,password='testpassword')
        response = self.client.get(create_ticket)
        
        self.assertEquals(response.status_code,403)
        
    def test_customer_ticket_list_view_with_customer_user(self):
        ticket_list = reverse('ticket-list')
        
        self.client.login(username=self.customer_user.username,password='testpassword')
        response = self.client.get(ticket_list)
        
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed('supportdesk/tickets-list.html')
        self.assertTrue(response.context['tickets'])
        
    def test_customer_ticket_list_view_with_non_customer_user(self):
        ticket_list = reverse('ticket-list')
        
        self.client.login(username=self.staff_user.username,password='testpassword')
        response = self.client.get(ticket_list)
        
        self.assertEquals(response.status_code,403)
        
    def test_agent_support_list_with_agent_user(self):
        agent_list = reverse('agent-list')

        self.client.login(username=self.staff_user.username,password='testpassword')
        response = self.client.get(agent_list)
        
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed('supportdesk/agent-list.html')
        self.assertTrue(response.context['tickets'])
        
    def test_agent_support_list_with_non_agent_user(self):
        agent_list = reverse('agent-list')

        self.client.login(username=self.customer_user.username,password='testpassword')
        response = self.client.get(agent_list)
        
        self.assertEquals(response.status_code,403)
        self.assertTemplateUsed('supportdesk/agent-list.html')
    
    def test_agent_support_detail_with_agent_user_GET_method(self):
        agent_detail = reverse('agent-detail',args=[self.support_ticket.pk])
        
        self.client.login(username=self.staff_user.username,password='testpassword')
        response = self.client.get(agent_detail)
        
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed('supportdesk/agent-detail.html')
        
    def test_agent_support_detail_with_agent_user_POST_method(self):
        agent_detail = reverse('agent-detail',args=[self.support_ticket.pk])
        
        self.client.login(username=self.staff_user.username,password='testpassword')
        response = self.client.get(agent_detail)
        
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed('supportdesk/agent-detail.html')
        
    def test_agent_support_detail_with_non_agent_user_GET_method(self):
        agent_detail = reverse('agent-detail',args=[self.support_ticket.pk])
        
        self.client.login(username=self.customer_user.username,password='testpassword')
        response = self.client.get(agent_detail)
        
        self.assertEquals(response.status_code,403)
        self.assertTemplateUsed('supportdesk/agent-detail.html')
        
    def test_my_tickets(self):
        my_tickets = reverse('my-tickets')
        
        self.client.login(username=self.staff_user.username,password='testpassword')
        response = self.client.get(my_tickets)
        
        self.assertEquals(response.status_code,200)
        self.assertEquals(response.context['tickets'].count(),1)
        self.assertTemplateUsed('supportdesk/my-tickets.html')
        

        
        
        
    
        