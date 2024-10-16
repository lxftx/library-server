from django.urls import reverse_lazy


class TitleMixin(object):
    title = None
    model_form_url = None

    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def get_success_url(self):
        return reverse_lazy("book:form-model", kwargs={'form_model': self.model_form_url})
