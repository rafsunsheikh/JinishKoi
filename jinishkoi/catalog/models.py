from audioop import reverse
from pyexpat import model
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


# Create your models here.

class EquipmentType(models.Model):
    """Model representing a equipment type."""
    name = models.CharField(max_length=200, help_text='Enter a equipment type (e.g. Radio Set)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Equipment(models.Model):
    """Model  representing a equipment but not a specific copy of a equipment"""
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    store = models.ForeignKey('Store', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the equipment')
    manufacture_id = models.CharField('Manufacture', max_length=13, unique=True,
                             help_text='Unique manufacture number')

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    equipment_type = models.ManyToManyField(EquipmentType, help_text='Select a type for this equipment')


    class Meta:
        ordering = ['title', 'store']

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('equipment-detail', args=[str(self.id)])

    def display_equipment_type(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(equipment_type.name for equipment_type in self.equipment_type.all()[:3])

    display_equipment_type.short_description = 'Types'


import uuid # Required for unique equipment instances

class EquipmentInstance(models.Model):
    """Model representing a specific copy of a equipment (i.e. that can be borrowed from the store)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular equipment across whole institution')
    equipment = models.ForeignKey('Equipment', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Equipment availability',
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set equipment as returned"),)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.equipment.title})'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Store(models.Model):
    """Model representing a store."""
    store_name = models.CharField(max_length=100)
    coy_name = models.CharField(max_length=100)
    date_of_last_maintainance = models.DateField(null=True, blank=True)
    date_of_next_maintainance = models.DateField('Maintainance', null=True, blank=True)

    class Meta:
        ordering = ['coy_name', 'store_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular store instance."""
        return reverse('store-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0}, {1}'.format(self.coy_name, self.store_name)
