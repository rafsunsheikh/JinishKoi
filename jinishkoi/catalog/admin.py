from django.contrib import admin

# Register your models here.
from .models import Store, EquipmentType, Equipment, EquipmentInstance

# admin.site.register(Equipment)
# admin.site.register(Store)
admin.site.register(EquipmentType)
# admin.site.register(EquipmentInstance)

class EquipmentsInline(admin.TabularInline):
    """Defines format of inline Equipment insertion (used in AuthorAdmin)"""
    model = Equipment

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    """Administration object for Store models.
    Defines:
     - fields to be displayed in list view (list_display)
     - orders fields in detail view (fields),
       grouping the date fields horizontally
     - adds inline addition of equipments in store view (inlines)
    """
    list_display = ('coy_name',
                    'store_name', 'date_of_last_maintainance', 'date_of_next_maintainance')
    fields = ['store_name', 'coy_name', ('date_of_last_maintainance', 'date_of_next_maintainance')]
    inlines = [EquipmentsInline]


# # Register the admin class with the associated model
# admin.site.register(Store, StoreAdmin)


# Register the Admin classes for Equipment using the decorator
class EquipmentInstanceInline(admin.TabularInline):
    model = EquipmentInstance



class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'store', 'display_equipment_type')

    inlines = [EquipmentInstanceInline]


admin.site.register(Equipment, EquipmentAdmin)

# Register the Admin classes for BookInstance using the decorator
@admin.register(EquipmentInstance)
class EquipmentInstanceAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('equipment', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
