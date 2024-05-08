from django.shortcuts import render
from home.models import Tribe
from district_wise.models import District

from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.
from django.conf import settings


def home_view(request):
    user = User.objects.get(phone_number=settings.ADMIN_USER_PHONE_NUMBER)
    tribes = Tribe.objects.filter(user = user, year='2022')
    districts=District.objects.filter(user = user, year='2022')
    user = request.user

    # tribe_wise_tdi = []
    # for tribe in tribes:
    #     tribe_wise_tdi.append(tribe.tribal_index)
    


    districts_name = []
    for district in districts:
        districts_name.append(district.name)


    # district_wise_tdi = []
    # for district in districts:
    #     district_wise_tdi.append(district.get_tdi_score()[0])

    context = {
        'tribes' : tribes,
        'districts' :districts,
        # 'tribe_wise_tdi' : tribe_wise_tdi,
        'districts_name' : districts_name,
        # 'district_wise_tdi' : district_wise_tdi,
        'user' : user,
    }




    return render(request,'home/index.html',context=context)



def gallery_view(request):
    user = User.objects.get(phone_number=settings.ADMIN_USER_PHONE_NUMBER)
    tribes = Tribe.objects.filter(user = user, year='2022')
    districts=District.objects.filter(user = user, year='2022')

    context={
        'tribes' : tribes,
        'districts' :districts,
    }
    return render(request,'gallery.html', context)


