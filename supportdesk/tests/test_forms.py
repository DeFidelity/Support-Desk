from django.test import SimpleTestCase 
from django.urls import reverse, resolve 
from ..forms import CustomerRequestForm


class TestCustomerRequestForm(SimpleTestCase):
    
    def test_request_form_with_valid_data(self):
        form = CustomerRequestForm(data={
            'summary': 'Need an upgrade in the sales funel',
            'description': 'Sales are frowing and we are considering an upgrade in our funnel, we needs to take more ..',
            'is_prioritized': True,
        })
        
        self.assertTrue(form.is_valid())
        self.assertEquals(len(form.errors),0)
        
    def test_request_form_with_invalid_data(self):
        form = CustomerRequestForm(data={
            'description': 'Sales are frowing and we are considering an upgrade in our funnel, we needs to take more ..',
            'is_prioritized': True,
        })
        
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),1)
        
    