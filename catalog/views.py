from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version


class ProductCreate(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home_page')


class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home_page')


class ProductUpdate(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home_page')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']

        if formset.is_valid and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()

            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        for product in context_data.get('object_list'):
            product.version = product.version_set.filter(active_version=True).first()

        return context_data


class ProductDetailView(DetailView):
    model = Product


class ContactView(View):
    model = Product

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name} {phone} {message}')
        return render(request, 'catalog/contacts.html')

    def get(self, request):
        return render(request, 'catalog/contacts.html')


class VersionList(ListView):
    model = Version
    success_url = reverse_lazy('catalog:version_list')

    def get_queryset(self, *args, **kwargs):
        queryset = Version.objects.filter(product=self.kwargs.get('pk'))
        return queryset

