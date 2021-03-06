from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q


from .models import Product, Category, Product_Family
from .forms import ProductForm, ProductFamilyForm


def all_products(request):
    """ A view to show all active products, including sorting and search queries """
    # sorted in model by category division & name, ordered here by size
    products = Product.objects.filter(active=True)
    query = None
    categories = None
    division = None
    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
            for c in categories:
                if c.get_division != division:
                    division = c.division
                else:
                    return

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria.")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query) | Q(product_family__name__icontains=query) 
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'division': division,
    }
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """
    product_family = None
    family_products = None

    product = get_object_or_404(Product, pk=product_id)
    product_family = product.product_family
    family_products = Product.objects.filter(
        product_family=product_family)

    context = {
        'product': product,
        'family_products': family_products,
        'product_family': product_family,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request,
                           ('Failed to add product. '
                            'Please ensure the form is valid.'))
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def product_families(request):
    """ A view to show all product families """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product_families = Product_Family.objects.all()

    context = {
        'product_families': product_families,
    }

    return render(request, 'products/product_families.html', context)


@login_required
def add_product_family(request):
    """ Add a product_family to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductFamilyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product family!')
            return redirect(reverse('product_families'))
        else:
            messages.error(request,
                           ('Failed to add product family. '
                            'Please ensure the form is valid.'))
    else:
        form = ProductFamilyForm()

    template = 'products/add_product_family.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product_family(request, product_family_id):
    """ Edit a product family """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product_family = get_object_or_404(Product_Family, pk=product_family_id)
    if request.method == 'POST':
        form = ProductFamilyForm(request.POST, instance=product_family)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product family!')
            return redirect(reverse('product_families'))
        else:
            messages.error(request,
                           ('Failed to update product family. '
                            'Please ensure the form is valid.'))
    else:
        form = ProductFamilyForm(instance=product_family)
        messages.info(request, f'You are editing {product_family.name}')

    template = 'products/edit_product_family.html'
    context = {
        'form': form,
        'product_family': product_family,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request,
                           ('Failed to update product. '
                            'Please ensure the form is valid.'))
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def deactivate_product(request, product_id):
    """ Deactivate a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.active = False
    product.save()
    messages.success(request, 'Product deactivated!')
    return redirect(reverse('products'))
