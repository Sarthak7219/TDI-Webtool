from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .models import Profile
from .forms import ProfileUpdateForm
from .models import Report_Excel

from django.contrib import messages
# Create your views here.
from .forms import *
from django.contrib.auth import get_user_model
User = get_user_model()
from django.conf import settings
from home.models import Tribe
from district_wise.models import District
from django.shortcuts import get_object_or_404
from mimetypes import guess_type


def register_view(request):
    if request.method == "POST":
        form = ProfileCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password1']
            user = authenticate(request, phone_number=phone_number, password=password)
            login(request, user)
            messages.success(request, 'Registration successful')
            return redirect('home')
        else:
            # Include form errors in the context
            context = {
                'form': form,
            }
            # Display error messages using Django messages framework
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ProfileCreationForm()
        context = {
            'form': form,
        }

    return render(request, 'accounts/register.html', context)




def login_view(request):
    context = {}
    if request.method == "POST":
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        user = authenticate(request, phone_number=phone_number, password=password)
        if user is None:
            messages.error(request, 'Invalid Phone Number or Password')
            return render(request, 'accounts/login.html', context=context)
        login(request, user)
        messages.success(request, 'Successfully logged in')
        return redirect('/')
    
    return render(request, 'accounts/login.html', context=context)

def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, 'Successfully logged out')
        return redirect('login')
    
    return render(request, 'accounts/logout.html')


def profile_view(request):
    admin_user = User.objects.get(phone_number=settings.ADMIN_USER_PHONE_NUMBER)
    tribes = Tribe.objects.filter(user = admin_user, year='2022')
    
    user_tribes =None
    user_districts = None

    
    districts=District.objects.filter(user = admin_user, year='2022')
    profile = request.user
    

    

    context = {
        'profile' :profile,
        'Tribe':Tribe,
        'tribes' : tribes,
        'districts' :districts,
    }

    excel_files = Report_Excel.objects.filter(user=profile)

    if excel_files:
        context['excel_files']=excel_files
    else:
        excel_files=None
        context['excel_files']=excel_files


    if request.method == 'POST':
            selected_year = request.POST.get('selected_year')
            file = Report_Excel.objects.filter(user=profile, year=selected_year).first()
            user_tribes = Tribe.objects.filter(user=profile, year=selected_year)
            user_districts = District.objects.filter(user=profile, year=selected_year)
            context['user_tribes']=user_tribes
            context['user_districts']=user_districts
            context['selected_year']=selected_year
            context['file']=file

    # if request.method == 'POST':
      
    #     form = ProfileCreationForm(request.POST, request.FILES, instance=profile)
    #     if form.is_valid():
    #         form.save()
            
    #         return redirect('accounts/profile.html')
    #     else:
    #         print(form.errors)
        

    return render (request, 'accounts/profile.html',context)

@login_required
def profile_edit_view(request):
    # Get the user's profile instance using the phone_number
    profile_instance, created = Profile.objects.get_or_create(phone_number=request.user.phone_number)
    print(profile_instance)
    print(profile_instance.first_name)
    print(profile_instance.last_name)
    print(profile_instance.email)
    print(profile_instance.phone_number)
    if request.method == 'POST':
        # Create an instance of the ProfileUpdateForm with the user's data
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_instance)
        print(form)
        if form.is_valid():
            # Save the form data to update the profile
            form.save()

            # Redirect to the profile page or any other page you want
            return redirect('profile')  # Change 'profile' to the actual name of your profile page

    else:
        # If it's a GET request, initialize the form with the current user's data
        form = ProfileUpdateForm(instance=profile_instance)

    context = {
        'form': form,
    }
    return render(request, 'accounts/editprofile.html', context)



def download_excel(request, file_id):
    excel_file = get_object_or_404(Report_Excel, id=file_id)
    file_path = excel_file.file.path
    content_type, encoding = guess_type(file_path)
    response = HttpResponse(content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{excel_file.file.name}"'
    with open(file_path, 'rb') as file:
        response.write(file.read())
    return response