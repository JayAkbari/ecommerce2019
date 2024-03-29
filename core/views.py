from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item, Order, OrderItem
from django.contrib import messages
from django.utils import timezone
# Create your views here.


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home-page.html"


class OrderSummaryView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object':order
            }
            return render(self.request, 'order_summary.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have active order")
            return redirect('/')
class ItemDetailView(DetailView):
    model = Item
    template_name = 'product-page.html'


def item_list(request):
    context = {'items': Item.objects.all()}
    return render(request, 'home-page.html', context)


def checkout(request):
    return render(request, 'checkout-page.html', {})


def product(request):
    return render(request, 'product-page.html', {})

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'Cart Updated')
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, 'Add To Cart')
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Add To Cart")
        return redirect("core:order-summary")

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, "Remove From Cart")
            return redirect("core:order-summary")

        else:
            messages.info(request, "Not Exist in cart")
            return redirect("core:productpage", slug=slug)
    else:
        messages.info(request, "Not Any Active Order")
        return redirect("core:productpage", slug=slug)

    return redirect("core:productpage", slug=slug)



@login_required
def remove_single_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False)[0]
            if order_item.quantity >1:
                order_item.quantity-=1
                order_item.save()
            else:
                order_item.delete(order_item)
            messages.info(request,'This item quantity was updated. ')
            return redirect("core:order-summary")

        else:
            messages.info(request, "Not Exist in cart")
            return redirect("core:productpage", slug=slug)
    else:
        messages.info(request, "Not Any Active Order")
        return redirect("core:productpage", slug=slug)

    return redirect("core:productpage", slug=slug)
