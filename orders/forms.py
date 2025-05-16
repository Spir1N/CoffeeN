from django import forms
from shop.models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 
                 'email', 'city', 
                 'postal_code', 'room']
        
    def __init__(self, *args, **kwargs):
        self.cart = kwargs.pop('cart', None)
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        order = super().save(commit=False)
        if self.cart:
            order.total_amount = self.cart.get_total_price()
        
        if commit:
            order.save()
        return order