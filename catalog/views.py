from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from catalog.models import Product, Version


class ProductCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.add_product'
    success_url = reverse_lazy('catalog:home_page')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.who_added = user
        product.save()
        return super().form_valid(form)


class ProductDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = 'catalog.delete_product'
    success_url = reverse_lazy('catalog:home_page')


class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.update_product'
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

    def get_form_class(self):
        user = self.request.user
        if user == self.object.who_added:
            return ProductForm
        if user.has_perm('catalog.can_change_discription_product') and user.has_perm('catalog.can_chage_category_product'):
            return ProductModeratorForm
        raise PermissionDenied



class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        for product in context_data.get('object_list'):
            product.version = product.version_set.filter(active_version=True).first()

        return context_data


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        product = context_data.get('object')
        product.version = product.version_set.filter(active_version=True).first()

        return context_data


class ContactView(LoginRequiredMixin, View):
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

