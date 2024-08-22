from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from contact.forms import ContactForm
from contact.models import Contact
from django.urls import reverse

@login_required(login_url='contact:login')
def create(request):
    form_action = reverse('contact:create')

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.first_name = contact.first_name.strip()
            contact.last_name = contact.last_name.strip()
            contact.phone = contact.phone.strip()
            contact.email = contact.email.strip()
            contact.description = contact.description.strip()
            contact.owner = request.user
            contact.save()
            
            return redirect('contact:update', contact_id=contact.pk)
        
        return render(request, 'pages/contact/create.html', {'form': form, 'form_action': form_action})

    return render(
        request,
        'pages/contact/create.html',
        {
            'form': ContactForm(),
            'form_action': form_action,
        }
    )

@login_required(login_url='contact:login')
def update(request, contact_id):
    contact = get_object_or_404(
        Contact, pk=contact_id, show=True, owner=request.user
    )
    form_action = reverse('contact:update', args=(contact_id,))

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
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
        'pages/contact/create.html',
        {'form': ContactForm(instance=contact), 'form_action': form_action}
    )

@login_required(login_url='contact:login')
def delete(request, contact_id):
    contact = get_object_or_404(
        Contact, pk=contact_id, show=True, owner=request.user
    )
    confirmation = request.POST.get('confirmation', 'no')

    if confirmation == 'yes':
        contact.delete()
        return redirect('contact:index')

    return render(
        request,
        'pages/contact/contact.html',
        {
            'contact': contact,
            'confirmation': confirmation,
        }
    )