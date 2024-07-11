from django.shortcuts import render, redirect, get_object_or_404
from contact.forms import ContactForm
from contact.models import Contact
from django.urls import reverse

def create(request):
    form_action = reverse('contact:create')

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.first_name = contact.first_name.strip()
            contact.last_name = contact.last_name.strip()
            contact.phone = contact.phone.strip()
            contact.email = contact.email.strip()
            contact.description = contact.description.strip()
            contact.save()
            
            return redirect('contact:update', contact_id=contact.pk)
        
        return render(request, 'contact/create.html', {'form': form, 'form_action': form_action})

    return render(
        request,
        'contact/create.html',
        {'form': ContactForm(), 'form_action': form_action}
    )

def update(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, show=True)
    form_action = reverse('contact:update', args=(contact_id,))

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.first_name = contact.first_name.strip()
            contact.last_name = contact.last_name.strip()
            contact.phone = contact.phone.strip()
            contact.email = contact.email.strip()
            contact.description = contact.description.strip()
            contact.save()
            
            return redirect('contact:update', contact_id=contact.pk)
        
        return render(request, 'contact/create.html', {'form': form, 'form_action': form_action})
          
    return render(
        request,
        'contact/create.html',
        {'form': ContactForm(instance=contact), 'form_action': form_action}
    )