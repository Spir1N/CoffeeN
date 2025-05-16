from django import forms
from shop.models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 
                  'email', 'city', 
                  'postal_code', 'room']
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
                