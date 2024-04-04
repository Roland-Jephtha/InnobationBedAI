from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone,dates
from datetime import date,time, timedelta,datetime
from .forms import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.core.paginator import Paginator,EmptyPage
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404
# from django.contrib.sites.models import Site


from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.views import PasswordResetView


from django.core.mail import send_mail
from django.template.loader import render_to_string







def sitemap(request):
    return render(request, 'sitemap_nerobuy.xml')

# @login_required(login_url='signin')

def products_view(request):
    
    
 
    
    text = request.GET.get('text')

    if text:
        products = Product.objects.filter(
        models.Q(name__icontains = text),
    )
    
        context = {
        "products": products
        }

        
        return render(request, "products_view.html", context)
    products = Product.objects.all()
    p = Paginator(products, 28)
    
    page_num = request.GET.get('page',1)
    
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
        
        
    context = {
        "products": page
    }
    return render(request, 'products_view.html', context)


def delete(request, pk):
    Product.objects.get(id = pk).delete()
    messages.success(request, "Product was deleted")
    return redirect('view_product')


@login_required(login_url='signin')

def add_product(request):
    category = Category.objects.all()
    products = Product.objects.filter(user = request.user)
    p = Paginator(products, 5)
    
    page_num = request.GET.get('page',1)
    
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
        
        
    if request.method == "POST":
       
            user = request.user
            name = request.POST['title']
            description = request.POST['description']
            price = request.POST['price']
            photo1 = request.FILES['image1']
      
            
            if 'image2' in request.FILES:
                photo2 = request.FILES['image2']     
            else:
                photo2 = None
            if 'image3' in request.FILES:
                photo3 = request.FILES['image3']     
            else:
                photo3 = None
            if 'image4' in request.FILES:
                photo4 = request.FILES['image4']     
            else:
                photo4 = None
             
                
            category = request.POST['category']
            store = request.user.business_name
            number = request.user.phone_number
         
            
            products = Product.objects.create(
                user = user,
                name = name,
                price = price,
                description = description,
                photo1 = photo1,
                photo2 = photo2,
                photo3 = photo3,
                photo4 = photo4,
                category = category,
                store = store,
                number = number
                
            )
            
            products.save()
            
            messages.success(request, 'Product was Added ')

            return redirect( 'add_product',)
    category = Category.objects.all()
    
    
    user_profile = Profile.objects.get(username = request.user.username)
    
    context = {
        'profile': user_profile,
        # 'form': form,
        'product': products,
        'category': category,
        
        
    }

    return render(request, "dashboard/add-products.html", context)


@login_required(login_url='signin')

def payment(request):
   
    if request.method == "POST":
       
        user = request.user
        name = request.POST['name']
        description = request.POST['description']
        amount = request.POST['amount']
        proof = request.FILES['proof']
    
            
            
        
        

        
        payrecords = PayRecord.objects.create(
            user = user,
            account_name = name,
            amount = amount,
            description = description,
            proof = proof,
            created = timezone.now()
          
        )
        
        payrecords.save()
        
        messages.success(request, 'Payment was Made ')

        return redirect( 'payment',)
    
    
    user_profile = Profile.objects.get(username = request.user.username)
    
    context = {
        'profile': user_profile,
        # 'form': form,
        
        
    }

    return render(request, "dashboard/payment.html", context)

















# update products
class UpdateProduct(UpdateView):
    model = Product
    fields = [ 'name', 'price',  'description']
    template_name = 'dashboard/update.html'
    context_object_name = "product"
    success_url = reverse_lazy('add_product')

    
    
# deleting of products
def delete_product(request, pk):
    Product.objects.get(id=pk).delete()
    messages.success(
        request, "Product Deleted Successfully!"
        )
    return redirect("add_product")





def home(request):
    products = Product.objects.all()
    
    
    text = request.GET.get('text')

    if text:
        products = Product.objects.filter(
        models.Q(name__icontains = text),
    )
    
        context = {
        "products": products
        }

        
        return render(request, "index.html", context)
    categories = Category.objects.all()
    recent_products = Product.objects.all()
    
    current_time = datetime.utcnow()
    

    
    
    
        
    p = Paginator(recent_products, 4)
    
    page_num = request.GET.get('page',1)
    
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
        
        
    p2 = Paginator(products, 12)
    
    page_num = request.GET.get('page',1)
    
    try:
        page2 = p2.page(page_num)
    except EmptyPage:
        page2 = p2.page(1)
        
    
    context= {
        "products": page2,
        "category" : categories,
        "recent_products": page
    }
    return render(request, 'index.html', context) 





@login_required(login_url='signin')

def dashboard(request):
    
    products = Product.objects.filter(user = request.user)
    current_time = datetime.utcnow()
    

    
    
    p = Paginator(products, 5)
    
    page_num = request.GET.get('page',1)
    
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
        
    user_profile = Profile.objects.get(username = request.user.username)
    # messages.success(request, "Product was deleted")

    
    context = {
        'profile': user_profile,
        'count' : products,
        'products' : page,
    }
    return render(request, "dashboard/dashboard.html", context)



@login_required(login_url='signin')

def view_product(request):

    products = Product.objects.filter(user = request.user)
    current_time = datetime.utcnow()
    
    p = Paginator(products, 6)
    
    page_num = request.GET.get('page',1)
    
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
        
        
    user_profile = Profile.objects.get(username = request.user.username)
    
    context = {
        'profile': user_profile,
        'products': page,
        'count' : products
    }
    return render(request, "dashboard/view_product.html", context)



# @login_required(login_url='signin')

# def items(request):
#     return render(request, "dashboard/items.html")


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        bname = request.POST['business_name']
        number = request.POST['number']
        password = request.POST['password']

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email Already Used ')
            return redirect('register')
        elif CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username Already Used")
            return redirect('register')
        else:
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            user.business_name = bname
            user.phone_number = number
          
            user.save()
            
            
             # email
            subject = 'Welcome to NeroBuy'
            email_from = settings.EMAIL_HOST_USER
            msg_html = render_to_string('email.html', {"username":username})
            message = f'''Hi {username}, thank you for registering On NeroBuy. Your Account Has Been Successful Created. Please Do Not Share Your Details With Anyone'''
            send_mail( "NeroBuy welcome message", message, email_from, [email], html_message=msg_html)
            
            store = Store.objects.create(
                user = user,
                name = bname
                
            )
            
            store.save()
            
            
            
            
            profile = Profile.objects.create(
            user = user,
            username = username,
            email = email,
            business_name = bname,
            number = number
     
            
        )
                
            
              
            messages.success(request, 'Account Created successfully')
            return redirect('signin')

    else:
        return render(request, 'register.html')
    
    
    
    

class CustomResetPasswordView(PasswordResetView):
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'email_subject.txt'
    success_url = 'password_reset/done'
    form_class = CustomPasswordResetForm

    
    
    
    
@login_required(login_url="signin")

def profile(request):
    profile = get_object_or_404(Profile, username = request.user.username)

    if request.method == 'POST':
      
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=profile)

        
            
    user_profile = Profile.objects.get(username = request.user.username)
    base_url = request.build_absolute_uri('/')
    
    context = {
        'profile': user_profile,
        'form': profile_form,
        'base_url' : base_url
    }

    return render(request, "dashboard/profile.html", context)    
    
    
    
    
    
    
    
def signin(request):
    if request.user.is_anonymous:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username,password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid Username or Password')
                return redirect('signin')
    else:
        return redirect("home")
    return render(request, 'signin.html')

    
    
    
    
    
@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('signin')




def store_category(request, store):
    
    text = request.GET.get('text')
    store  = Store.objects.get(name__contains=store)

    
    if text:
        products = Product.objects.filter(
            models.Q(name__icontains = text),
        )
        
        context = {
        "store": store,
        "products": products
        }
    
        
        return render(request, "store_category.html", context)
    
    
    
    products = Product.objects.filter(store =store)
    store  = Store.objects.get(name__contains=store)
    

    p = Paginator(products, 12)
    
    page_num = request.GET.get('page',1)
    
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
        
    if store.paid == True:
        context = {
        "store": store,
        "products": products
    }
    
        
        return render(request, "store_category.html", context)
    context = {
        "store": store,
    }
    return render(request, "store_category.html", context)




def product_category(request, category):
    product = Product.objects.filter(category__name__contains=category)
    context = {
        "category": category,
        "products": product
    }
    return render(request, "category.html", context)





def product(request,pk):
    product = Product.objects.get(id  = pk)
    base_url = request.build_absolute_uri('/')

    # category = Category.objects.get(id = pk)
    # related_product = Product.objects.filter(category__name = product.ca)
    return render(request, 'products.html', {'product': product, 'base_url' : base_url }) 
    # return render(request, 'products.html', {'product': product, 'related_product': related_product}) 









# def blog_category(request, category):
#     posts = Post.objects.filter(categories__name__contains=category).order_by('-date_create')
#     context = {
#         "category": category,
#         "posts": posts
#     }
#     return render(request, "blog_category.html", context)


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect(signin)