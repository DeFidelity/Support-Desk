from django.db import models
from django.contrib.auth.models import User

LEVELS = (
    ('submitted', 'submitted'),
    ('progress', 'in progress'),
    ('completed', 'completed')
)


class SupportTicket(models.Model):
    created_by = models.ForeignKey(User,related_name='customer',on_delete=models.CASCADE)
    summary = models.CharField(max_length=300)
    description = models.TextField()
    is_prioritized = models.BooleanField(default=False)
    level = models.CharField(max_length=20,choices=LEVELS,default='submitted')
    assign_to = models.ForeignKey(User,related_name='agent',on_delete=models.CASCADE,null=True,blank=True)
    created = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['is_prioritized','created']
        
    def __str__(self):
        return self.summary
    
    @property
    def number_of_request(self,user):
        ticket = SupportTicket.objects.filter(created_by=user)
        
        return ticket.count()