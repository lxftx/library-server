from django.urls import path

from book.views import (FormListView, IndexView,  # , delete_form_model
                        get_info_form_model)

app_name = 'book'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('form/', FormListView.as_view(), name='form-view'),
    path('form/<form_model>', get_info_form_model, name='form-model'),
    # path('form/<form_model>/<int:pk>', delete_form_model, name='form-model-pk'),
]

