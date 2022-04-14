from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import generic

# Create your views here.
from .models import Equipment, Store, EquipmentInstance, EquipmentType

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_equipments = Equipment.objects.all().count()
    num_instances = EquipmentInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = EquipmentInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_stores = Store.objects.count()


    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1


    context = {
        'num_equipments': num_equipments,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_stores': num_stores,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)



class EquipmentListView(generic.ListView):
    model = Equipment
    paginate_by = 10


class EquipmentDetailView(generic.DetailView):
    model = Equipment
    paginate_by = 10

    def equipment_detail_view(request, primary_key):
        equipment = get_object_or_404(Equipment, pk=primary_key)
        return render(request, 'catalog/equipment_detail.html', context={'equipment': equipment})


class StoreListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Store
    paginate_by = 10

class StoreDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = Store


from django.contrib.auth.mixins import LoginRequiredMixin


class LoanedEquipmentsByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = EquipmentInstance
    template_name ='catalog/equipmentinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return EquipmentInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

# Added as part of challenge!
from django.contrib.auth.mixins import PermissionRequiredMixin


class LoanedEquipmentsAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all equipments on loan. Only visible to users with can_mark_returned permission."""
    model = EquipmentInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/equipmentinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return EquipmentInstance.objects.filter(status__exact='o').order_by('due_back')


import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from catalog.forms import RenewEquipmentForm


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_equipment_storeman(request, pk):
    equipment_instance = get_object_or_404(EquipmentInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewEquipmentForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            equipment_instance.due_back = form.cleaned_data['renewal_date']
            equipment_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewEquipmentForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'equipment_instance': equipment_instance,
    }

    return render(request, 'catalog/equipment_renew_storeman.html', context)


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Store


class StoreCreate(PermissionRequiredMixin, CreateView):
    model = Store
    fields = ['store_name', 'coy_name', 'date_of_last_maintainance', 'date_of_next_maintainance']
    initial = {'date_of_next_maintainance': '11/06/2020'}
    permission_required = 'catalog.can_mark_returned'

class StoreUpdate(PermissionRequiredMixin, UpdateView):
    model = Store
    fields = '__all__' # Not recommended (potential security issue if more fields added)
    permission_required = 'catalog.can_mark_returned'


class StoreDelete(PermissionRequiredMixin, DeleteView):
    model = Store
    success_url = reverse_lazy('stores')
    permission_required = 'catalog.can_mark_returned'


# Classes created for the forms challenge
class EquipmentCreate(PermissionRequiredMixin, CreateView):
    model = Equipment
    fields = ['title', 'store', 'summary', 'manufacture_id', 'equipment_type']
    permission_required = 'catalog.can_mark_returned'


class EquipmentUpdate(PermissionRequiredMixin, UpdateView):
    model = Equipment
    fields = ['title', 'store', 'summary', 'manufacture_id', 'equipment_type']
    permission_required = 'catalog.can_mark_returned'


class EquipmentDelete(PermissionRequiredMixin, DeleteView):
    model = Equipment
    success_url = reverse_lazy('equipments')
    permission_required = 'catalog.can_mark_returned'