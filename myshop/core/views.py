from django.shortcuts import render,get_object_or_404
from .models import offerproduct,Product,Category, Brands
from django.db.models import Count
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from cart.cart import Cart
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from datetime import datetime
from .models import Contact
from recommend.utils import build_recommendations, get_recommendations

# Create your views here.
# def home(request):
#     offer = offerproduct.objects.all()
#     cate = Category.objects.all()
#     br = Brands.objects.annotate(product_count=Count('product'))

#     catid = request.GET.get('category')
#     br_id = request.GET.get('brand')

#     product = Product.objects.all()

#     if catid and br_id:
#         product = Product.objects.filter(subcategory=catid, brands=br_id)
#     elif catid:
#         product = Product.objects.filter(subcategory=catid)
#     elif br_id:
#         product = Product.objects.filter(brands=br_id)
#     else:
#         product = Product.objects.all()

#     paginator = Paginator(product, 6)
#     num_pages = request.GET.get('page')
#     data = paginator.get_page(num_pages)
#     total = data.paginator.num_pages

#     context = {
#         'offer': offer,
#         'product': product,
#         'cate': cate,
#         'br': br,
#         'data': data,
#         'num': [i + 1 for i in range(total)]
#     }
#     return render(request, 'core/index.html', context)
def home(request):
    offer = offerproduct.objects.all()
    cate = Category.objects.all()
    br = Brands.objects.annotate(product_count=Count('product'))

    catid = request.GET.get('category')
    br_id = request.GET.get('brand')

    product = Product.objects.all()

    if catid and br_id:
        product = Product.objects.filter(subcategory=catid, brands=br_id)
    elif catid:
        product = Product.objects.filter(subcategory=catid)
    elif br_id:
        product = Product.objects.filter(brands=br_id)
    else:
        product = Product.objects.all()

    # ---------------- ML Recommendation Logic ----------------
    recommended_products = []
    slides = []
    if product.exists():
        featured_product = product.latest('created_date')  # choose product for recommendations
        df, cosine_sim = build_recommendations(product)
        rec_ids = get_recommendations(featured_product.id, df, cosine_sim)
        recommended_products = Product.objects.filter(id__in=rec_ids)
        slides = [recommended_products[i:i+3] for i in range(0, len(recommended_products), 3)]
    # ----------------------------------------------------------

    paginator = Paginator(product, 6)
    num_pages = request.GET.get('page')
    data = paginator.get_page(num_pages)
    total = data.paginator.num_pages

    context = {
        'offer': offer,
        'product': product,
        'cate': cate,
        'br': br,
        'data': data,
        'num': [i + 1 for i in range(total)],
        'slides': slides,  # pass ML recommendations to template
    }
    return render(request, 'core/index.html', context)

def product_detail(request,id):
    data=get_object_or_404(Product,id=id)
    return render(request,'core/product_detail.html',{'data':data})
def contact(request):
        if request.method == "POST":
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            message_input = request.POST.get("message")

            if not phone.isdigit() or len(phone) < 7:
                messages.error(request, "Phone number must be at least 7 digits.")
                return redirect('contact')

            try:
                # Save to database
                contact = Contact(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                    message=message_input
                )
                contact.full_clean()  # Optional: validates fields if you set model validators
                contact.save()

                # Send confirmation email
                subject = "Thank You for Contacting Us!"
                message_body = render_to_string('core/contact_message.html', {
                    'name': first_name,
                    'date': datetime.now()
                })

                send_mail(
                    subject,
                    message_body,
                    'sujanmijar018@gmail.com',  # Sender email
                    [email],                    # Recipient email
                    fail_silently=False,
                )

                messages.success(request, f"Dear {first_name}, your message has been sent successfully!")
                return redirect('contact')

            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
                return redirect('contact')

        return render(request,'core/contact.html')

# card section
@login_required(login_url="log_in")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="log_in")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="log_in")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="log_in")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="log_in")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="log_in")
def cart_detail(request):
    return render(request, 'core/cart.html')