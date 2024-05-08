from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import Http404
from .models import Tribe,Tribe_Image
from district_wise.models import District
from django.http import HttpResponse
from django.contrib.auth import get_user_model
User = get_user_model()
from django.conf import settings
from django.contrib.auth.decorators import login_required
import pandas as pd
import numpy as np
from openpyxl import Workbook


def tribe_detail_view(request, name, year):
    
    admin_user = User.objects.get(phone_number=settings.ADMIN_USER_PHONE_NUMBER)
    tribes = Tribe.objects.filter(user = admin_user, year='2022')
    districts=District.objects.filter(user = admin_user, year='2022')

    inputted_data = request.GET.get('inputted_data', False) == 'True'

    if inputted_data:
    # Use get_object_or_404 to handle the case when the tribe is not found
        tribe = get_object_or_404(Tribe, user=request.user, year=year, name=name)
    else:
        tribe = get_object_or_404(Tribe, user=admin_user, year=year, name=name)

    # tribe_of_slug = Tribe.objects.get(slug = slug1)
    # total_tribals = tribe.get_total_tribals
        

    health_contributions_to_dimension = [tribe.CD_contri_to_H, tribe.IM_contri_to_H, tribe.MC_contri_to_H, tribe.CM_contri_to_H, tribe.FS_contri_to_H]
    education_contributions_to_dimension = [tribe.LE_contri_to_E, tribe.DRO_contri_to_E]
    sol_contributions_to_dimension = [tribe.IC_contri_to_S, tribe.OW_contri_to_S, tribe.SANI_contri_to_S, tribe.FUEL_contri_to_S, tribe.DRWA_contri_to_S, tribe.ELECTR_contri_to_S, tribe.ASS_contri_to_S,]
    culture_contributions_to_dimension = [tribe.LAN_contri_to_C, tribe.ARTS_contri_to_C]
    governance_contributions_to_dimension = [tribe.EV_contri_to_G, tribe.MEET_contri_to_G]

    tribal_dimensional_index = [tribe.H_DI, tribe.E_DI, tribe.S_DI, tribe.C_DI, tribe.G_DI]
    dimension_contribution_to_tdi = [tribe.H_contri_to_TDI, tribe.E_contri_to_TDI, tribe.S_contri_to_TDI, tribe.C_contri_to_TDI, tribe.G_contri_to_TDI]
    tribal_incidence=tribe.tribal_incidence
    tribal_intensity=tribe.tribal_intensity

    tdi = tribe.TDI

    uncensored_tribe_arr = [tribe.UNC_CD_score, tribe.UNC_IM_score, tribe.UNC_MC_score, tribe.UNC_CM_score, tribe.UNC_FS_score, tribe.UNC_LE_score, tribe.UNC_DRO_score, tribe.UNC_IC_score, tribe.UNC_OW_score, tribe.UNC_SANI_score, tribe.UNC_FUEL_score, tribe.UNC_DRWA_score, tribe.UNC_ELECTR_score, tribe.UNC_ASS_score, tribe.UNC_LAN_score, tribe.UNC_ARTS_score, tribe.UNC_EV_score, tribe.UNC_MEET_score]

    
    
    censored_tribe_arr = [tribe.CEN_CD_score, tribe.CEN_IM_score, tribe.CEN_MC_score, tribe.CEN_CM_score, tribe.CEN_FS_score, tribe.CEN_LE_score, tribe.CEN_DRO_score, tribe.CEN_IC_score, tribe.CEN_OW_score, tribe.CEN_SANI_score, tribe.CEN_FUEL_score, tribe.CEN_DRWA_score, tribe.CEN_ELECTR_score, tribe.CEN_ASS_score, tribe.CEN_LAN_score, tribe.CEN_ARTS_score, tribe.CEN_EV_score, tribe.CEN_MEET_score]
    detail = tribe.village_details
    
    context = {
        'tribes' : tribes,
        'districts' :districts,
        'tribe': tribe,
        'health_contributions_to_dimension': health_contributions_to_dimension,
        'education_contributions_to_dimension': education_contributions_to_dimension,
        'sol_contributions_to_dimension': sol_contributions_to_dimension,
        'culture_contributions_to_dimension': culture_contributions_to_dimension,
        'governance_contributions_to_dimension': governance_contributions_to_dimension,
        'tribal_dimensional_index': tribal_dimensional_index,
        'dimension_contribution_to_tdi': dimension_contribution_to_tdi,
        'incidence':tribal_incidence,
        'intensity':tribal_intensity,
        'tdi' : tdi,
        'uncensored_tribe_arr' : uncensored_tribe_arr,
        'censored_tribe_arr' : censored_tribe_arr,
        'name' : 'bokaro'
    }
    
    for entry in detail:
        block_name_list_str = entry.get('Block_name_list')
        lines = block_name_list_str.split(',')  # Split by line breaks first


    context['detail_Block_name_list'] = lines
    context['detail'] = detail

    if inputted_data:
        template_name = 'pvtg/asurcopy.html' 
        
    else:
        template_name = 'pvtg/asur.html' 

    # Use render function with the determined template name
    return render(request, template_name, context=context)

        

import pandas as pd
from .test import perform_calculations

@login_required(login_url='/accounts/login/')
def tribe_form_view(request):
    user = User.objects.get(phone_number=settings.ADMIN_USER_PHONE_NUMBER)
    tribes = Tribe.objects.filter(user=user, year = '2022').distinct()
    alltribes_defined=Tribe.objects.filter(user = user)
    # YourModelFormSet = formset_factory(HouseholdForm, extra=1, can_delete=True, validate_max=True)
    if request.method == 'POST':


        year = request.POST.get('year')
       
        if request.user.is_authenticated:
            user_from_form = request.user  #user instance
        else:
            return HttpResponse('Login first')
        
          #tribe instance

        if 'households_excel_file' in request.FILES:
            uploaded_file  = request.FILES['households_excel_file']
            
            #create dataframe of base_data
            base_data_df = pd.read_excel(uploaded_file,engine='openpyxl')

            perform_calculations(base_data_df, user_from_form, year)
            inputted_data = True
            redirect_url = f'/tribe/asur/{request.POST["year"]}/?inputted_data={inputted_data}'
            return redirect(redirect_url)
        else:
            # tribe_slug = request.POST.get('tribe_slug')
            # cleaned_data_list = []
            # formset = YourModelFormSet(request.POST, prefix='form')
        
            # if formset.is_valid():
            #     for form in formset:
                    
            #         tribe, created = Tribe.objects.get_or_create(user=request.user, year=year, name=tribe_slug)
            #         household = form.save(commit=False)
            #         household.tribeID = tribe
            #         household.save()
            #         cleaned_data_list.append(household)
            # else:
            #     print(formset.errors)

            # if cleaned_data_list:
            #    redirect_url = f'/tribe/{tribe_slug}/{request.POST["year"]}?user={user_from_form.phone_number}'
            #    return redirect(redirect_url)
            return HttpResponse('Please upload excel')


    context = {
        'tribes': tribes,
        'alltribes':alltribes_defined,
    }
    return render(request, 'form/tribe_form.html',context)

    
def tribe_pdf_view(request, slug):
    tribe = Tribe.objects.get(slug = slug)
    tribes = Tribe.objects.all()
    user = request.user

    total_tribals = tribe.get_total_tribals
    districts = District.objects.all()
    
    contributions_to_dimension = tribe.indicator_contributions_to_dimension

    health_contributions_to_dimension = contributions_to_dimension[0] if contributions_to_dimension and len(contributions_to_dimension) > 0 else None
    education_contributions_to_dimension = contributions_to_dimension[1] if contributions_to_dimension and len(contributions_to_dimension) > 1 else None
    sol_contributions_to_dimension = contributions_to_dimension[2] if contributions_to_dimension and len(contributions_to_dimension) > 2 else None
    culture_contributions_to_dimension = contributions_to_dimension[3] if contributions_to_dimension and len(contributions_to_dimension) > 3 else None
    governance_contributions_to_dimension = contributions_to_dimension[4] if contributions_to_dimension and len(contributions_to_dimension) > 4 else None

    tribal_dimensional_index = tribe.tribal_dimensional_index
    dimension_contribution_to_tdi = tribe.dimension_contribution_to_tdi

    
    
    context = {
        'total_tribals': total_tribals,
        'tribe': tribe,
        'tribes' : tribes,
        'health_contributions_to_dimension': health_contributions_to_dimension,
        'education_contributions_to_dimension': education_contributions_to_dimension,
        'sol_contributions_to_dimension': sol_contributions_to_dimension,
        'culture_contributions_to_dimension': culture_contributions_to_dimension,
        'governance_contributions_to_dimension': governance_contributions_to_dimension,
        'tribal_dimensional_index': tribal_dimensional_index,
        'dimension_contribution_to_tdi': dimension_contribution_to_tdi,
        'districts' : districts,
        'user' : user,

    }
    return render(request, 'pdfs/tribe_pdf.html', context)



def test_view(request):
    user = User.objects.get(phone_number=settings.ADMIN_USER_PHONE_NUMBER)

    # tribe = Tribe.objects.get(user = user, year = '2022', name = 'asur')

    # total_tribals = tribe.get_total_tribals
    
    # cnt = 0
    # tribal_intensity = 0
    # for i in household:
    #     print('**')
    #     print(i.no_of_indicators, i.developed_indicators, i.calculate_weightage)
    #     print(i.D_DS)
    #     cnt+=i.D_DS[4]
    #     # cnt+=i.D_DS[2]
    #     # cnt+=i.D_DS[3]
    #     # cnt+=i.D_DS[4

    # print(cnt)

    context = {
        # 'household' : household,
        # 'total_tribals' : total_tribals,
        # 'tribe' : tribe,
        

    }
    return render(request, 'pvtg/test.html', context)



from django.http import HttpResponse
from io import BytesIO
import pandas as pd
import csv
def download_template(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=household_data_template.xlsx'

    # Create a new workbook and grab the active worksheet
    workbook = Workbook()
    worksheet = workbook.active

    # Add column headings to the worksheet
    headers = [
       '__fid__', 'village_name', 'Gram_panchayat', 'Block_name', 'District_name', 'Tribe_N', 'HH_S', 'Name',
    'Relationship_Respondent', 'Gender', 'Age', 'chronic_disease', 'disease_name', 'basic_vaccination',
    'Institutional_delivery', 'ANC', 'Infant_mortality', '2sqmeals', 'food_diversity', 'Ed', 'Inst_Credit',
    'ration_c_color', 'agricultureland', 'home_ownership', 'defecation', 'bath', 'source_fuel', 'source_drinking_water',
    'electricity', 'assets', 'smart_phone', 'no_hen_cock', 'no_goats', 'no_cows', 'no_buffaloes', 'no_oxan', 'no_pigs',
    'no_ducks', 'no_swan', 'Pond_Fish', 'Language', 'traditional_song', 'traditional_dance', 'traditional_instrument',
    'Traditional_Instrument', 'voter', 'traditional_sabha', 'traditional_meeting', 'gram_sabha_meeting',
    'Panchayat_meetings', 'SHG', 'Eligibility_CD', 'CD_Cum_Score', 'Eligibility_IMM', 'IMM_Cum_Score',
    'Eligibility_IND', 'IND_Cum_Score', 'Eligibility_ANC', 'ANC_Cum_Score', 'U5CM_Cum_Score', '2sq_Cum_Score',
    'Energy', 'Proteins', 'Vitamins', 'FD_Cum_Score', 'Eligibility LE', 'cum_score_LE', 'Eligibility DRO',
    'cum_score_DRO', 'Aadhaar_bank_account_MCP_Aayushman', 'Ration', 'Job/ Labour/ Kisan credit', 'CUM_SCORE_IC',
    'CUM_SCORE_OWN', 'CUM_SCORE_SANI', 'cum_score_Fuel', 'cum_score_SoDrWa', 'cum_score_ELECTR', 'ASS_INFO', 'ASS_LIVE',
    'ASS_TRANS', 'ASS', 'ANI', 'CUM_SCORE_ASS', 'cum_score_L', 'cum_score_So', 'cum_score_MuI', 'cum_score_Da',
    'cum_score_Arts', 'Eligibility_voter', 'cum_score_EV', 'Cum_score_meetings'
        # Add the rest of your headers here
    ]
    worksheet.append(headers)

    # Save the workbook to the response
    workbook.save(response)

    return response

	



