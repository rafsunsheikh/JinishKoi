from nturl2path import url2pathname
from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('equipments/', views.EquipmentListView.as_view(), name='equipments'),
    path('equipment/<int:pk>', views.EquipmentDetailView.as_view(), name='equipment-detail'),
    path('stores/', views.StoreListView.as_view(), name='stores'),
    path('store/<int:pk>',
         views.StoreDetailView.as_view(), name='store-detail'),
]
urlpatterns += [
    path('myequipments/', views.LoanedEquipmentsByUserListView.as_view(), name='my-borrowed'),
    path(r'borrowed/', views.LoanedEquipmentsAllListView.as_view(), name='all-borrowed'),  # Added for challenge
]

urlpatterns += [
    path('equipment/<uuid:pk>/renew/', views.renew_equipment_storeman, name='renew-equipment-storeman'),
]

# Add URLConf to create, update, and delete stores
urlpatterns += [
    path('store/create/', views.StoreCreate.as_view(), name='store-create'),
    path('store/<int:pk>/update/', views.StoreUpdate.as_view(), name='store-update'),
    path('store/<int:pk>/delete/', views.StoreDelete.as_view(), name='store-delete'),
]

# Add URLConf to create, update, and delete equipments
urlpatterns += [
    path('equipment/create/', views.EquipmentCreate.as_view(), name='equipment-create'),
    path('equipment/<int:pk>/update/', views.EquipmentUpdate.as_view(), name='equipment-update'),
    path('equipment/<int:pk>/delete/', views.EquipmentDelete.as_view(), name='equipment-delete'),
]