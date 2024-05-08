import pandas as pd
import numpy as np
from django.conf import settings
def perform_calculations(base_data_df, user, year):


    # base_data_df = pd.read_excel()

    base_data_df['Eligibility_CD'] = np.where(base_data_df['chronic_disease'].str.strip() == 'लागू नहीं', 0, 1)

        
    base_data_df['CD_Cum_Score'] = np.where(base_data_df['chronic_disease'].str.strip() == "हां", 0, 1)

    base_data_df['Age'] = pd.to_numeric(base_data_df['Age'], errors='coerce')

    base_data_df['Eligibility_IMM'] = np.where(base_data_df['Age'] < 1, 0, 1)




    conditions_IMM_Cum_Score = [
        (base_data_df['Age'] < 16),
        (base_data_df['basic_vaccination'].str.strip() == 'पूरी तरह')
    ]
    values_IMM_Cum_Score = [np.nan, 1]
    base_data_df['IMM_Cum_Score'] = np.select(conditions_IMM_Cum_Score, values_IMM_Cum_Score, default=0)


    base_data_df['Eligibility_IND'] = np.where(base_data_df['Institutional_delivery'].str.strip() == 'लागू नहीं', 0, 1)



    conditions_IND_Cum_Score = [
        (base_data_df['Institutional_delivery'].str.strip() == 'स्वास्थ्य केंद्र'),
        (base_data_df['Eligibility_IND'] == 0)
    ]
    values_IND_Cum_Score = [1, np.nan]
    base_data_df['IND_Cum_Score'] = np.select(conditions_IND_Cum_Score, values_IND_Cum_Score, default=0)



    conditions_Eligibility_ANC = [
        (base_data_df['ANC'].str.strip() == 'लागू नहीं') | (16 > base_data_df['Age']) | (base_data_df['Age'] > 45) | (base_data_df['Gender'].str.strip() != 'महिला')
    ]
    values_Eligibility_ANC = [0]
    base_data_df['Eligibility_ANC'] = np.select(conditions_Eligibility_ANC, values_Eligibility_ANC, default=1)


    conditions_ANC_Cum_Score = [
        (base_data_df['ANC'].str.strip().isin(['हाँ, सभी तिमाही', 'हाँ, 1 तिमाही', 'हाँ, 2 तिमाही'])),
        (base_data_df['Eligibility_ANC'] == 0)
    ]
    values_ANC_Cum_Score = [1, np.nan]
    base_data_df['ANC_Cum_Score'] = np.select(conditions_ANC_Cum_Score, values_ANC_Cum_Score, default=0)


    condition_U5CM_Cum_Score = (base_data_df['Infant_mortality'].str.strip() == 'हां')
    base_data_df['U5CM_Cum_Score'] = np.where(condition_U5CM_Cum_Score, 0, 1)

    condition_2sq_Cum_Score = (base_data_df['2sqmeals'].str.strip() == 'हाँ, पर्याप्त')
    base_data_df['2sq_Cum_Score'] = np.where(condition_2sq_Cum_Score, 1, 0)

    keywords_Energy = ['चावल', 'रोटी', 'ज्वार', 'आलू', 'बाजरा', 'लिट्टी']
    condition_Energy = base_data_df['food_diversity'].str.strip().apply(lambda x: any(keyword in x for keyword in keywords_Energy))
    base_data_df['Energy'] = np.where(condition_Energy, 1, 0)

    proteins_condition = (
        base_data_df['food_diversity'].str.contains('दाल|मछली|मांस|खुकड़ी|सत्तू', regex=True, na=False)
    )
    base_data_df['Proteins'] = np.where(proteins_condition, 1, 0)

    condition_Vitamins = base_data_df['food_diversity'].apply(lambda x: 1 if 'साग' in x or 'अन्य' in x else 0)
    base_data_df['Vitamins'] = condition_Vitamins

    condition_FD_Cum_Score = (np.sum(base_data_df[['Energy', 'Proteins', 'Vitamins']], axis=1) == 3)
    base_data_df['FD_Cum_Score'] = np.where(condition_FD_Cum_Score, 1, 0)

    condition_eligibility_LE = (base_data_df['Age'] >= 10)
    base_data_df['Eligibility LE'] = np.where(condition_eligibility_LE, 1, 0)

    conditions = [
        (base_data_df['Ed'].isin(["6th कक्षा पूरा किया हुआ", "7th कक्षा पूरा किया हुआ", "8th कक्षा पूरा किया हुआ", "9th कक्षा पूरा किया हुआ", "10th कक्षा पूरा किया हुआ", "11th कक्षा पूरा किया हुआ", "12th कक्षा पूरा किया हुआ", "डिप्लोमा पूरा किया हुआ", "डिग्री पूरा किया हुआ", "पोस्ट ग्रेजुएशन पूरा किया हुआ"])),
        (base_data_df['Eligibility LE'] == 0)
    ]

    choices = [1, np.nan]

    base_data_df['cum_score_LE'] = np.select(conditions, choices, default=0)

    condition_Eligibility_DRO = np.logical_or(base_data_df['Age'] < 15, base_data_df['Age'] > 64)
    base_data_df['Eligibility DRO'] = np.where(condition_Eligibility_DRO, 0, 1)



    conditions_cum_score_DRO = [
        (base_data_df['Ed'].str.strip().isin(['10th कक्षा पूरा किया हुआ', '11th कक्षा पूरा किया हुआ', '12th कक्षा पूरा किया हुआ', 'डिप्लोमा पूरा किया हुआ', 'डिग्री पूरा किया हुआ', 'पोस्ट ग्रेजुएशन पूरा किया हुआ'])),
        (base_data_df['Eligibility DRO'] == 0)
    ]

    values_cum_score_DRO = [1, np.nan]
    base_data_df['cum_score_DRO'] = np.select(conditions_cum_score_DRO, values_cum_score_DRO, default=0)




    condition_Aadhaar_bank_account_MCP_Aayushman = (
        (base_data_df['Inst_Credit'].str.contains('आधार कार्ड')) &
        (base_data_df['Inst_Credit'].str.contains('बैंक खाता')) &
        (base_data_df['Inst_Credit'].str.contains('आयुष्मान कार्ड')) &
        (base_data_df['Inst_Credit'].str.contains('जच्चा बच्चा पात्रता'))
    )
    base_data_df['Aadhaar_bank_account_MCP_Aayushman'] = np.where(
        condition_Aadhaar_bank_account_MCP_Aayushman, 1, 0
    )

    condition_Ration = (base_data_df['ration_c_color'].str.strip() == 'लागू नहीं')
    base_data_df['Ration'] = np.where(condition_Ration, 0, 1)


    condition_job_labour_kisan_credit = base_data_df['Inst_Credit'].str.contains('जॉब कार्ड|श्रम कार्ड|किसान क्रेडिट कार्ड', case=False, na=False)
    base_data_df['Job/ Labour/ Kisan credit'] = np.where(condition_job_labour_kisan_credit, 1, 0)


    condition_CUM_SCORE_IC = ((base_data_df['Aadhaar_bank_account_MCP_Aayushman'] + base_data_df['Ration'] + base_data_df['Job/ Labour/ Kisan credit']) >= 1)

    base_data_df['CUM_SCORE_IC'] = np.where(condition_CUM_SCORE_IC, 1, 0)


    condition_CUM_SCORE_OWN = (base_data_df['agricultureland'].str.strip() == 'हां') | (base_data_df['home_ownership'].str.strip() == 'हां')
    base_data_df['CUM_SCORE_OWN'] = np.where(condition_CUM_SCORE_OWN, 1, 0)


    condition_CUM_SCORE_SANI = (base_data_df['defecation'].str.contains('घर के भीतर') | base_data_df['bath'].str.contains('घर के भीतर'))
    base_data_df['CUM_SCORE_SANI'] = np.where(condition_CUM_SCORE_SANI, 1, 0)


    condition_cum_score_Fuel = base_data_df['source_fuel'].str.contains("गैस")
    base_data_df['cum_score_Fuel'] = np.where(condition_cum_score_Fuel, 1, 0)


    condition_cum_score_SoDrWa = base_data_df['source_drinking_water'].str.contains("घर का नल")
    base_data_df['cum_score_SoDrWa'] = np.where(condition_cum_score_SoDrWa, 1, 0)

    base_data_df['cum_score_ELECTR'] = np.where(base_data_df['electricity'].str.strip() == 'हां', 1, 0)

    condition_ASS_INFO = (
        (base_data_df['assets'].str.contains('इंटरनेट का उपयोग')) |
        (base_data_df['assets'].str.contains('सामान्य फोन')) |
        (base_data_df['assets'].str.contains('टेलीविजन')) |
        (base_data_df['assets'].str.contains('कंप्यूटर सिस्टम/लैपटॉप/टैबलेट'))|
        (base_data_df['smart_phone'].str.contains('हां'))
    )
    base_data_df['ASS_INFO'] = np.where(
        condition_ASS_INFO, 1, 0
    )


    condition_ASS_LIVE = (
        (base_data_df['assets'].str.contains('बिजली का पंखा')) |
        (base_data_df['assets'].str.contains('गैस - चूल्हा')) |
        (base_data_df['assets'].str.contains('हल')) |
        (base_data_df['assets'].str.contains('मिक्सी'))|
        (base_data_df['assets'].str.contains('सिचाई के लिए पम्पसेट'))|
        (base_data_df['assets'].str.contains('प्रेशर कुकर'))|
        (base_data_df['assets'].str.contains('तालाब'))
    )
    base_data_df['ASS_LIVE'] = np.where(
        condition_ASS_LIVE, 1, 0
    )


    condition_ASS_TRANS = (
        (base_data_df['assets'].str.contains('गाड़ी')) |
        (base_data_df['assets'].str.contains('साइकिल')) |
        (base_data_df['assets'].str.contains('दो पहिया')) |
        (base_data_df['assets'].str.contains('रिक्शा'))|
        (base_data_df['assets'].str.contains('ट्रैक्टर'))
    )
    base_data_df['ASS_TRANS'] = np.where(
        condition_ASS_TRANS, 1, 0
    )


    condition_ASS = ((base_data_df['ASS_TRANS'] + base_data_df['ASS_LIVE'] + base_data_df['ASS_INFO'])) == 3
    base_data_df['ASS'] = np.where(condition_ASS, 1, 0)


    columns_to_handle = ['no_hen_cock', 'no_goats', 'no_cows', 'no_buffaloes', 'no_oxan', 'no_pigs', 'no_ducks', 'no_swan']

    for column in columns_to_handle:
            base_data_df[column] = pd.to_numeric(base_data_df[column], errors='coerce').fillna(0).astype(int)


    condition_ANI = (
    (base_data_df['no_hen_cock'] + base_data_df['no_goats'] + base_data_df['no_cows'] + base_data_df['no_buffaloes'] + base_data_df['no_oxan'] + base_data_df['no_pigs'] + base_data_df['no_ducks'] + base_data_df['no_swan']) > 0 | (base_data_df['Pond_Fish'] == 'हां'))


    base_data_df['ANI'] = np.where(condition_ANI, 1, 0)




    condition_CUM_SCORE_ASS = (base_data_df['ASS'] + base_data_df['ANI']== 2)
    base_data_df['CUM_SCORE_ASS'] = np.where(condition_CUM_SCORE_ASS, 1, 0)


    condition_cum_score_L = (
        (base_data_df['Language'].str.contains('कोरथा')) |
        (base_data_df['Language'].str.contains('मुंडारी')) |
        (base_data_df['Language'].str.contains('बिरहोर')) |
        (base_data_df['Language'].str.contains('बिरजिया'))|
        (base_data_df['Language'].str.contains('करमाली'))|
        (base_data_df['Language'].str.contains('हो')) |
        (base_data_df['Language'].str.contains('खरिया')) |
        (base_data_df['Language'].str.contains('खोंडी')) |
        (base_data_df['Language'].str.contains('संताली'))|
        (base_data_df['Language'].str.contains('कोरा'))|
        (base_data_df['Language'].str.contains('कोरवा')) |
        (base_data_df['Language'].str.contains('पहाड़िया')) |
        (base_data_df['Language'].str.contains('कुरुख/ओरांव')) |
        (base_data_df['Language'].str.contains('सावर'))
        
    )
    base_data_df['cum_score_L'] = np.where(
        condition_cum_score_L, 1, 0
    )

    base_data_df['cum_score_So'] = np.where(base_data_df['traditional_song'].str.strip() == "हां", 1, 0)



    condition_cum_score_MuI = (
        (base_data_df['traditional_instrument'].str.strip() == "हां") |
        (base_data_df['Traditional_Instrument'].str.strip() != "कुछ नहीं")
    )

    base_data_df['cum_score_MuI'] = np.where(condition_cum_score_MuI, 1, 0)



    condition_cum_score_Da = (base_data_df['traditional_dance'].str.strip() == "हां")
    base_data_df['cum_score_Da'] = np.where(condition_cum_score_Da, 1, 0)


    condition_cum_score_Arts = ((base_data_df['cum_score_Da'] + base_data_df['cum_score_MuI'] + base_data_df['cum_score_So'])) > 0
    base_data_df['cum_score_Arts'] = np.where(condition_cum_score_Arts, 1, 0)


    condition_Eligibility_voter = (base_data_df['Age'] >= 18)
    base_data_df['Eligibility_voter'] = np.where(condition_Eligibility_voter, 1, 0)






    conditions_cum_score_EV = [
        (base_data_df['Eligibility_voter'] == 0),
        ((base_data_df['voter'] > 0) | (base_data_df['voter'] == np.nan) | (base_data_df['voter'] == "") | base_data_df['voter'].isnull())
    ]


    values_cum_score_EV = [np.nan, 1]
    base_data_df['cum_score_EV'] = np.select(conditions_cum_score_EV, values_cum_score_EV, default=0)



    condition_Cum_s_core_meetings = (
        (base_data_df['SHG'].str.contains("हां")) |
        (base_data_df['traditional_meeting'].str.contains("हां")) |
        (base_data_df['gram_sabha_meeting'].str.contains("हां")) |
        (base_data_df['Panchayat_meetings'].str.contains("हां"))
        
    )
    base_data_df['Cum_s core_meetings'] = np.where(
        condition_Cum_s_core_meetings, 1, 0
    )


    # excel_writer = pd.ExcelWriter("C:/SARTHAK\NOTES/SEM5\Web TDI/pandas/New datas/TRI_base_data_file.xlsx", engine='xlsxwriter')
    # base_data_df.to_excel(excel_writer, sheet_name='Sheet1', na_rep='NA', index=False)
    # excel_writer._save()
    print("Result Excel file saved successfully.")
    # base_data_df.to_excel(settings.EXCEL_FILE_PATH, index=False)
    # print("Result Excel file saved successfully.")

    base_data_df.to_excel(settings.EXCEL_FILE_PATH1, index=False)
    print("Result Excel file saved successfully.")

    total_fid = base_data_df[['__fid__']].values.tolist()
    tribes = np.array(base_data_df['Tribe_N']).flatten().tolist()
    Block_name = np.array(base_data_df['Block_name']).flatten().tolist()
    village_name = np.array(base_data_df['village_name']).flatten().tolist()
    District_name = np.array(base_data_df['District_name']).flatten().tolist()



    unique_fid = []
    unique_tribes = []
    unique_Block_name = []
    unique_village_name = []
    unique_District_name = []

    for x in total_fid:
        if x not in unique_fid:
            unique_fid.append(x)

    for x in tribes:
        if x not in unique_tribes:
            unique_tribes.append(x)

    for x in Block_name:
        if x not in unique_Block_name:
            unique_Block_name.append(x)
    for x in village_name:
        if x not in unique_village_name:
            unique_village_name.append(x)
    for x in District_name:
        if x not in unique_District_name:
            unique_District_name.append(x)



    total_tribes = len(unique_tribes)
    length_fid = len(unique_fid)


    score = [0] * length_fid
    HH_size_list = [0] * length_fid
    HH_tribe_list = [""] * length_fid
    HH_village_name_list = [""] * length_fid
    HH_District_name_list = [""] * length_fid
    HH_Block_name_list = [""] * length_fid


    for i in range(length_fid):
            for j in range(len(total_fid)):

                if unique_fid[i] == total_fid[j]:
                    HH_size_list[i] += 1
                    if HH_tribe_list[i] == "":
                        HH_tribe_list[i] = tribes[j]
                        HH_village_name_list[i]=village_name[j]
                        HH_District_name_list[i]=District_name[j]
                        HH_Block_name_list[i]=Block_name[j]




    def calScore(list1,list2,score):
        for i in range(length_fid):
            score[i] = 0
            for j in range(len(list1)):

                if unique_fid[i] == list1[j]:
                    if pd.isna(list2[j]) or list2[j] == np.nan:
                        continue  
                    score[i] += int(list2[j])

    # Rest of your code remains unchanged

    # Rest of your code remains unchanged


    # Rest of your code remains unchanged


    score_columns = {}

    for column in ['Eligibility_CD', 'CD_Cum_Score', 'Eligibility_IMM','IMM_Cum_Score','Eligibility_IND', 'IND_Cum_Score', 'Eligibility_ANC', 'ANC_Cum_Score', 'U5CM_Cum_Score', '2sq_Cum_Score', 'FD_Cum_Score', 'Eligibility LE', 'cum_score_LE', 'Eligibility DRO', 'cum_score_DRO', 'CUM_SCORE_IC', 'CUM_SCORE_OWN', 'CUM_SCORE_SANI', 'cum_score_Fuel', 'cum_score_SoDrWa', 'cum_score_ELECTR','CUM_SCORE_ASS', 'Cum_s core_meetings', 'cum_score_L', 'cum_score_Arts', 'Eligibility_voter', 'cum_score_EV']:
        # Initialize a list to store cumulative scores
        score_column = [0] * length_fid

        # Calculate the cumulative score
        calScore(total_fid, base_data_df[column], score_column)

        # Add the cumulative score to the dictionary
        score_columns[f'Sum of {column}'] = score_column

    # Combine the cumulative scores into a DataFrame
    cum_score_df = pd.DataFrame({
        '_fid_': unique_fid,
        **score_columns
    })

    cum_score_df.to_excel(settings.EXCEL_FILE_PATH2, index=False)
    print("Result Excel file saved successfully.")


    HH_score_df = pd.DataFrame({
        '_fid_': unique_fid,
        'Tribe_N' : HH_tribe_list,
        'Sum of HH_S' : HH_size_list,
        'HH_village_name_list':HH_village_name_list,
        'HH_Block_name_list':HH_Block_name_list,
        'HH_District_name_list':HH_District_name_list,

    })

    village_block_list = [""] * total_tribes
    Block_name_list = [""] * total_tribes
    District_name_list = [""] * total_tribes

    for i in range(total_tribes):
        for j in range(len(tribes)):
            if tribes[j] == unique_tribes[i] and District_name_list[i].find(District_name[j]) == -1:
                District_name_list[i] += District_name[j] + ', '
            if tribes[j] == unique_tribes[i] and village_block_list[i].find(village_name[j]) == -1:
                village_block_list[i] += village_name[j] + ':' + Block_name[j] + ', '


# Remove trailing commas and spaces from concatenated strings
    village_block_list = [village_block.rstrip(', ') for village_block in village_block_list]
    # village_block_list = [village_block.replace(', ', '\n') for village_block in village_block_list]

# Now village_block_list contains the desired concatenation
   
            
    # from .models import Tribe


    # Assuming village_name_list has been created and populated




    # # Conditions and value assigning for the new column 'HH_Score_H_CD'
    HH_score_df['HH_Score_H_CD'] = np.where(cum_score_df['Sum of Eligibility_CD'] == cum_score_df['Sum of CD_Cum_Score'], 1, 0)
    HH_score_df['HH_Score_H_IMM'] = np.where(cum_score_df['Sum of Eligibility_IMM'] == cum_score_df['Sum of IMM_Cum_Score'], 1, 0)

    conditions = [
        (cum_score_df['Sum of Eligibility_IND'] == HH_score_df['Sum of HH_S']),
        (cum_score_df['Sum of Eligibility_IND'] != HH_score_df['Sum of HH_S'])
    ]

    choices = [
        np.where(cum_score_df['Sum of IND_Cum_Score'] > 1, 1, 0),
        np.nan
    ]

    HH_score_df['HH_Score_H_IND'] = np.select(conditions, choices, default=0).astype('object')


    condition_HH_Score_H_ANC = (cum_score_df['Sum of Eligibility_ANC'] > 0) & (cum_score_df['Sum of ANC_Cum_Score'] > 1)
    HH_score_df['HH_Score_H_ANC'] = np.where(condition_HH_Score_H_ANC, 1, np.where(cum_score_df['Sum of Eligibility_ANC'] > 0, 0, np.nan)).astype('object')



    HH_score_df['HH_Score_H_IND'] = pd.to_numeric(HH_score_df['HH_Score_H_IND'], errors='coerce')
    HH_score_df['HH_Score_H_ANC'] = pd.to_numeric(HH_score_df['HH_Score_H_ANC'], errors='coerce')

    conditions_HH_Score_H_MC = [
        (HH_score_df['HH_Score_H_IND'].notna() & HH_score_df['HH_Score_H_ANC'].notna() & (HH_score_df['HH_Score_H_IND'] + HH_score_df['HH_Score_H_ANC'] == 2)),
        (HH_score_df['HH_Score_H_IND'].isna() | HH_score_df['HH_Score_H_ANC'].isna())
    ]
    choices_HH_Score_H_MC = [1, np.nan]
    HH_score_df['HH_Score_H_MC'] = np.select(conditions_HH_Score_H_MC, choices_HH_Score_H_MC, default=0)
    HH_score_df['HH_Score_H_MC'] = pd.to_numeric(HH_score_df['HH_Score_H_MC'], errors='coerce')

    HH_score_df['HH_Score_H_U5CM'] = np.where(cum_score_df['Sum of U5CM_Cum_Score'] < HH_score_df['Sum of HH_S'], 0, 1)
    HH_score_df['HH_Score_H_FS'] = np.where((cum_score_df['Sum of 2sq_Cum_Score'] == HH_score_df['Sum of HH_S']) & (cum_score_df['Sum of FD_Cum_Score'] == HH_score_df['Sum of HH_S']), 1, 0)

    HH_score_df['H_TOT_IND'] = HH_score_df[['HH_Score_H_CD', 'HH_Score_H_IMM', 'HH_Score_H_MC', 'HH_Score_H_U5CM', 'HH_Score_H_FS']].apply(lambda row: row.value_counts().get(1, 0) + row.value_counts().get(0, 0), axis=1)
    HH_score_df['H_DEV_IND'] = HH_score_df[['HH_Score_H_CD', 'HH_Score_H_IMM', 'HH_Score_H_MC', 'HH_Score_H_U5CM', 'HH_Score_H_FS']].eq(1).sum(axis=1)
    HH_score_df['H_weightage'] = round((0.2 / HH_score_df['H_TOT_IND']),4)
    HH_score_df['H_DS'] = round((HH_score_df['H_weightage'] * HH_score_df['H_DEV_IND']),3)


    HH_score_df['HH_Score_E_LE'] = np.where(cum_score_df['Sum of cum_score_LE'] >= 1, 1, 0)
    HH_score_df['HH_Score_E_DRO'] = np.where(cum_score_df['Sum of cum_score_DRO'] == cum_score_df['Sum of Eligibility DRO'], 1, 0)

    HH_score_df['E_TOT_IND'] = HH_score_df[['HH_Score_E_LE', 'HH_Score_E_DRO']].apply(lambda row: row.value_counts().get(1, 0) + row.value_counts().get(0, 0), axis=1)
    HH_score_df['E_DEV_IND'] = HH_score_df[['HH_Score_E_LE', 'HH_Score_E_DRO']].eq(1).sum(axis=1)
    HH_score_df['E_weightage'] = round((0.2 / HH_score_df['E_TOT_IND']),4)
    HH_score_df['E_DS'] = round((HH_score_df['E_weightage'] * HH_score_df['E_DEV_IND']),3)


    HH_score_df['HH_Score_S_IC'] = np.where(cum_score_df['Sum of CUM_SCORE_IC'] >= 1, 1, 0)


    # Assuming 'cum_score_df' is your DataFrame

    # Assigning values for the column "HH_Score_S_OWN"
    HH_score_df['HH_Score_S_OWN'] = np.where(cum_score_df['Sum of CUM_SCORE_OWN'] >= 1, 1, 0)

    # Assigning values for the column "HH_Score_S_SANI"
    HH_score_df['HH_Score_S_SANI'] = np.where(cum_score_df['Sum of CUM_SCORE_SANI'] == HH_score_df['Sum of HH_S'], 1, 0)

    # Assigning values for the column "HH_Score_S_Fuel"
    HH_score_df['HH_Score_S_Fuel'] = np.where(cum_score_df['Sum of cum_score_Fuel'] >= 1, 1, 0)

    # Assigning values for the column "HH_Score_S_SoDrWa"
    HH_score_df['HH_Score_S_SoDrWa'] = np.where(cum_score_df['Sum of cum_score_SoDrWa'] >= 1, 1, 0)

    # Assigning values for the column "HH_Score_S_ELECTR"
    HH_score_df['HH_Score_S_ELECTR'] = np.where(cum_score_df['Sum of cum_score_ELECTR'] >= 1, 1, 0)

    # Assigning values for the column "HH_Score_S_ASS"
    HH_score_df['HH_Score_S_ASS'] = np.where(cum_score_df['Sum of CUM_SCORE_ASS'] >= 1, 1, 0)

    HH_score_df['S_TOT_IND'] = HH_score_df[['HH_Score_S_IC', 'HH_Score_S_OWN', 'HH_Score_S_SANI', 'HH_Score_S_Fuel', 'HH_Score_S_SoDrWa', 'HH_Score_S_ELECTR', 'HH_Score_S_ASS']].apply(lambda row: row.value_counts().get(1, 0) + row.value_counts().get(0, 0), axis=1)
    HH_score_df['S_DEV_IND'] = HH_score_df[['HH_Score_S_IC', 'HH_Score_S_OWN', 'HH_Score_S_SANI', 'HH_Score_S_Fuel', 'HH_Score_S_SoDrWa', 'HH_Score_S_ELECTR', 'HH_Score_S_ASS']].eq(1).sum(axis=1)
    HH_score_df['S_weightage'] = round((0.2 / HH_score_df['S_TOT_IND']),4)
    HH_score_df['S_DS'] = round((HH_score_df['S_weightage'] * HH_score_df['S_DEV_IND']),3)


    HH_score_df['HH_Score_C_L'] = np.where(cum_score_df['Sum of cum_score_L'] >= 1, 1, 0)
    HH_score_df['HH_Score_C_Arts'] = np.where(cum_score_df['Sum of cum_score_Arts'] >= 1, 1, 0)

    HH_score_df['C_TOT_IND'] = HH_score_df[['HH_Score_C_L', 'HH_Score_C_Arts']].apply(lambda row: row.value_counts().get(1, 0) + row.value_counts().get(0, 0), axis=1)
    HH_score_df['C_DEV_IND'] = HH_score_df[['HH_Score_C_L', 'HH_Score_C_Arts']].eq(1).sum(axis=1)
    HH_score_df['C_weightage'] = round((0.2 / HH_score_df['C_TOT_IND']),4)
    HH_score_df['C_DS'] = round((HH_score_df['C_weightage'] * HH_score_df['C_DEV_IND']),3)




    conditions_HH_Score_G_EV = [
        (np.logical_and(cum_score_df['Sum of cum_score_EV'] > 0, cum_score_df['Sum of cum_score_EV'] == cum_score_df['Sum of Eligibility_voter'])),
        (cum_score_df['Sum of Eligibility_voter'] == 0)
    ]

    choices_HH_Score_G_EV = [1, np.nan]

    HH_score_df['HH_Score_G_EV'] = np.select(conditions_HH_Score_G_EV, choices_HH_Score_G_EV, default=0)
    HH_score_df['HH_Score_G_EV'] = pd.to_numeric(HH_score_df['HH_Score_G_EV'], errors='coerce')

    HH_score_df['HH_Score_G_meeting'] = np.where(cum_score_df['Sum of Cum_s core_meetings'] > 0, 1, 0)

    HH_score_df['G_TOT_IND'] = HH_score_df[['HH_Score_G_EV', 'HH_Score_G_meeting']].apply(lambda row: row.value_counts().get(1, 0) + row.value_counts().get(0, 0), axis=1)
    HH_score_df['G_DEV_IND'] = HH_score_df[['HH_Score_G_EV', 'HH_Score_G_meeting']].eq(1).sum(axis=1)
    HH_score_df['G_weightage'] = round((0.2 / HH_score_df['G_TOT_IND']),4)
    HH_score_df['G_DS'] = round((HH_score_df['G_weightage'] * HH_score_df['G_DEV_IND'] ),3)

    HH_score_df['HH_DS'] = np.sum(HH_score_df[['H_DS', 'E_DS', 'S_DS', 'C_DS', 'G_DS']].values, axis=1)


    HH_score_df['H_Is_the_HH_developed'] = np.where(HH_score_df['H_DS'] < 0.066, 0, 1)
    HH_score_df['E_Is_the_HH_developed'] = np.where(HH_score_df['E_DS'] < 0.066, 0, 1)
    HH_score_df['S_Is_the_HH_developed'] = np.where(HH_score_df['S_DS'] < 0.066, 0, 1)
    HH_score_df['C_Is_the_HH_developed'] = np.where(HH_score_df['C_DS'] < 0.066, 0, 1)
    HH_score_df['G_Is_the_HH_developed'] = np.where(HH_score_df['G_DS'] < 0.066, 0, 1)

    HH_score_df['Is_the_HH_multidimensionally_developed'] = np.where(HH_score_df['HH_DS'] <= 0.33, 0, 1)

    HH_score_df['H_HH_members_of_developed_HHs'] = np.where(HH_score_df['H_Is_the_HH_developed'] == 1, HH_score_df['Sum of HH_S'], 0)
    HH_score_df['E_HH_members_of_developed_HHs'] = np.where(HH_score_df['E_Is_the_HH_developed'] == 1, HH_score_df['Sum of HH_S'], 0)
    HH_score_df['S_HH_members_of_developed_HHs'] = np.where(HH_score_df['S_Is_the_HH_developed'] == 1, HH_score_df['Sum of HH_S'], 0)
    HH_score_df['C_HH_members_of_developed_HHs'] = np.where(HH_score_df['C_Is_the_HH_developed'] == 1, HH_score_df['Sum of HH_S'], 0)
    HH_score_df['G_HH_members_of_developed_HHs'] = np.where(HH_score_df['G_Is_the_HH_developed'] == 1, HH_score_df['Sum of HH_S'], 0)

    HH_score_df['HH_members_of_developed_HHs'] = np.where(HH_score_df['Is_the_HH_multidimensionally_developed'] == 1, HH_score_df['Sum of HH_S'], 0)


        


    Tribe_cum_score_df = pd.DataFrame({
        'Tribe_N' : unique_tribes,
    })

    Total_Sum_of_HH_S=[0]*total_tribes
    Total_H_Is_the_HH_developed=[0]*total_tribes
    Total_E_Is_the_HH_developed=[0]*total_tribes
    Total_S_Is_the_HH_developed=[0]*total_tribes
    Total_C_Is_the_HH_developed=[0]*total_tribes
    Total_G_Is_the_HH_developed=[0]*total_tribes
    Total_Is_the_HH_mulltidimensionally_developed=[0]*total_tribes
    Total_H_HH_members_of_developed_HHs=[0]*total_tribes
    Total_E_HH_members_of_developed_HHs=[0]*total_tribes
    Total_S_HH_members_of_developed_HHs=[0]*total_tribes
    Total_C_HH_members_of_developed_HHs=[0]*total_tribes
    Total_G_HH_members_of_developed_HHs=[0]*total_tribes
    Total_HH_members_of_developed_HHs=[0]*total_tribes


    for i in range(total_tribes):
        for j in range(len(HH_tribe_list)):
            if HH_tribe_list[j] == unique_tribes[i]:
                Total_Sum_of_HH_S[i] += HH_size_list[j]
                Total_H_Is_the_HH_developed[i] += HH_score_df['H_Is_the_HH_developed'][j]
                Total_E_Is_the_HH_developed[i] += HH_score_df['E_Is_the_HH_developed'][j]
                Total_S_Is_the_HH_developed[i] += HH_score_df['S_Is_the_HH_developed'][j]
                Total_C_Is_the_HH_developed[i] += HH_score_df['C_Is_the_HH_developed'][j]
                Total_G_Is_the_HH_developed[i] += HH_score_df['G_Is_the_HH_developed'][j]
                Total_Is_the_HH_mulltidimensionally_developed[i] += HH_score_df['Is_the_HH_multidimensionally_developed'][j]
                Total_H_HH_members_of_developed_HHs[i] += HH_score_df['H_HH_members_of_developed_HHs'][j]
                Total_E_HH_members_of_developed_HHs[i] += HH_score_df['E_HH_members_of_developed_HHs'][j]
                Total_S_HH_members_of_developed_HHs[i] += HH_score_df['S_HH_members_of_developed_HHs'][j]
                Total_C_HH_members_of_developed_HHs[i] += HH_score_df['C_HH_members_of_developed_HHs'][j]
                Total_G_HH_members_of_developed_HHs[i] += HH_score_df['G_HH_members_of_developed_HHs'][j]
                Total_HH_members_of_developed_HHs[i] += HH_score_df['HH_members_of_developed_HHs'][j]

    Tribe_cum_score_df['Total_Sum_of_HH_S'] = Total_Sum_of_HH_S
    Tribe_cum_score_df['Total_H_Is_the_HH_developed'] = Total_H_Is_the_HH_developed
    Tribe_cum_score_df['Total_E_Is_the_HH_developed'] = Total_E_Is_the_HH_developed
    Tribe_cum_score_df['Total_S_Is_the_HH_developed'] = Total_S_Is_the_HH_developed
    Tribe_cum_score_df['Total_C_Is_the_HH_developed'] = Total_C_Is_the_HH_developed
    Tribe_cum_score_df['Total_G_Is_the_HH_developed'] = Total_G_Is_the_HH_developed
    Tribe_cum_score_df['Total_Is_the_HH_mulltidimensionally_developed'] = Total_Is_the_HH_mulltidimensionally_developed
    Tribe_cum_score_df['Total_H_HH_members_of_developed_HHs'] = Total_H_HH_members_of_developed_HHs
    Tribe_cum_score_df['Total_E_HH_members_of_developed_HHs'] = Total_E_HH_members_of_developed_HHs
    Tribe_cum_score_df['Total_S_HH_members_of_developed_HHs'] = Total_S_HH_members_of_developed_HHs
    Tribe_cum_score_df['Total_C_HH_members_of_developed_HHs'] = Total_C_HH_members_of_developed_HHs
    Tribe_cum_score_df['Total_G_HH_members_of_developed_HHs'] = Total_G_HH_members_of_developed_HHs
    Tribe_cum_score_df['Total_HH_members_of_developed_HHs'] = Total_HH_members_of_developed_HHs




    HH_score_df['H_Incidence_of_Tribal_development'] = [0.00] * len(HH_tribe_list)
    HH_score_df['E_Incidence_of_Tribal_development'] = [0.00] * len(HH_tribe_list)
    HH_score_df['S_Incidence_of_Tribal_development'] = [0.00] * len(HH_tribe_list)
    HH_score_df['C_Incidence_of_Tribal_development'] = [0.00] * len(HH_tribe_list)
    HH_score_df['G_Incidence_of_Tribal_development'] = [0.00] * len(HH_tribe_list)
    HH_score_df['Incidence_of_Tribal_development'] = [0.00] * len(HH_tribe_list)
    HH_score_df['H_Intensity_of_Tribal_development'] = [0.00] * len(HH_tribe_list)
    HH_score_df['E_Intensity_of_Tribal_development'] = [0.00] * len(HH_tribe_list)
    HH_score_df['S_Intensity_of_Tribal_development'] = [0.00] * len(HH_tribe_list)
    HH_score_df['C_Intensity_of_Tribal_development'] = [0.00] * len(HH_tribe_list)
    HH_score_df['G_Intensity_of_Tribal_development'] = [0.00] * len(HH_tribe_list)
    HH_score_df['Intensity_of_Tribal_development'] = [0.00] * len(HH_tribe_list)



    for i in range(total_tribes):
        total_sum_of_hh_s = Tribe_cum_score_df['Total_Sum_of_HH_S'][i]
        total_h_hh_members = Tribe_cum_score_df['Total_H_HH_members_of_developed_HHs'][i]
        total_e_hh_members = Tribe_cum_score_df['Total_E_HH_members_of_developed_HHs'][i]
        total_s_hh_members = Tribe_cum_score_df['Total_S_HH_members_of_developed_HHs'][i]
        total_c_hh_members = Tribe_cum_score_df['Total_C_HH_members_of_developed_HHs'][i]
        total_g_hh_members = Tribe_cum_score_df['Total_G_HH_members_of_developed_HHs'][i]
        total_hh_members = Tribe_cum_score_df['Total_HH_members_of_developed_HHs'][i]

        for j in range(len(HH_tribe_list)):
            if HH_tribe_list[j] == unique_tribes[i]:
                HH_score_df.loc[j,'H_Incidence_of_Tribal_development'] = round(float(HH_score_df['H_HH_members_of_developed_HHs'][j] / total_sum_of_hh_s) if total_sum_of_hh_s != 0 else 0, 5)
                HH_score_df.loc[j,'E_Incidence_of_Tribal_development'] = round(float(HH_score_df['E_HH_members_of_developed_HHs'][j] / total_sum_of_hh_s) if total_sum_of_hh_s != 0 else 0, 5)
                HH_score_df.loc[j,'S_Incidence_of_Tribal_development'] = round(float(HH_score_df['S_HH_members_of_developed_HHs'][j] / total_sum_of_hh_s) if total_sum_of_hh_s != 0 else 0, 5)
                HH_score_df.loc[j,'C_Incidence_of_Tribal_development'] = round(float(HH_score_df['C_HH_members_of_developed_HHs'][j] / total_sum_of_hh_s) if total_sum_of_hh_s != 0 else 0, 5)
                HH_score_df.loc[j,'G_Incidence_of_Tribal_development'] = round(float(HH_score_df['G_HH_members_of_developed_HHs'][j] / total_sum_of_hh_s) if total_sum_of_hh_s != 0 else 0, 5)
                HH_score_df.loc[j,'Incidence_of_Tribal_development'] = round(float(HH_score_df['HH_members_of_developed_HHs'][j] / total_sum_of_hh_s) if total_sum_of_hh_s != 0 else 0, 5)
                
                HH_score_df.loc[j,'H_Intensity_of_Tribal_development'] = round(float((HH_score_df['H_DS'][j] * HH_score_df['H_HH_members_of_developed_HHs'][j] * 5) / total_h_hh_members) if total_h_hh_members != 0 else 0, 5)
                HH_score_df.loc[j,'E_Intensity_of_Tribal_development'] = round(float((HH_score_df['E_DS'][j] * HH_score_df['E_HH_members_of_developed_HHs'][j] * 5) / total_e_hh_members) if total_e_hh_members != 0 else 0, 5)
                HH_score_df.loc[j,'S_Intensity_of_Tribal_development'] = round(float((HH_score_df['S_DS'][j] * HH_score_df['S_HH_members_of_developed_HHs'][j] * 5) / total_s_hh_members) if total_s_hh_members != 0 else 0, 5)
                HH_score_df.loc[j,'C_Intensity_of_Tribal_development'] = round(float((HH_score_df['C_DS'][j] * HH_score_df['C_HH_members_of_developed_HHs'][j] * 5) / total_c_hh_members) if total_c_hh_members != 0 else 0, 5)
                HH_score_df.loc[j,'G_Intensity_of_Tribal_development'] = round(float((HH_score_df['G_DS'][j] * HH_score_df['G_HH_members_of_developed_HHs'][j] * 5) / total_g_hh_members) if total_g_hh_members != 0 else 0, 5)
                HH_score_df.loc[j,'Intensity_of_Tribal_development'] = round(float((HH_score_df['HH_DS'][j] * HH_score_df['HH_members_of_developed_HHs'][j]) / total_hh_members) if total_hh_members != 0 else 0, 5)


    Total_H_Incidence_of_Tribal_development=[0]*total_tribes
    Total_E_Incidence_of_Tribal_development=[0]*total_tribes
    Total_S_Incidence_of_Tribal_development=[0]*total_tribes
    Total_C_Incidence_of_Tribal_development=[0]*total_tribes
    Total_G_Incidence_of_Tribal_development=[0]*total_tribes
    Total_Incidence_of_Tribal_development=[0]*total_tribes

    Total_H_Intensity_of_Tribal_development=[0]*total_tribes
    Total_E_Intensity_of_Tribal_development=[0]*total_tribes
    Total_S_Intensity_of_Tribal_development=[0]*total_tribes
    Total_C_Intensity_of_Tribal_development=[0]*total_tribes
    Total_G_Intensity_of_Tribal_development=[0]*total_tribes
    Total_Intensity_of_Tribal_development=[0]*total_tribes



    for i in range(total_tribes):
        for j in range(len(HH_tribe_list)):
            if HH_tribe_list[j] == unique_tribes[i]:
                Total_H_Incidence_of_Tribal_development[i] += HH_score_df['H_Incidence_of_Tribal_development'][j]
                Total_E_Incidence_of_Tribal_development[i] += HH_score_df['E_Incidence_of_Tribal_development'][j]
                Total_S_Incidence_of_Tribal_development[i] += HH_score_df['S_Incidence_of_Tribal_development'][j]
                Total_C_Incidence_of_Tribal_development[i] += HH_score_df['C_Incidence_of_Tribal_development'][j]
                Total_G_Incidence_of_Tribal_development[i] += HH_score_df['G_Incidence_of_Tribal_development'][j]
                Total_Incidence_of_Tribal_development[i] += HH_score_df['Incidence_of_Tribal_development'][j]

                Total_H_Intensity_of_Tribal_development[i] += HH_score_df['H_Intensity_of_Tribal_development'][j]
                Total_E_Intensity_of_Tribal_development[i] += HH_score_df['E_Intensity_of_Tribal_development'][j]
                Total_S_Intensity_of_Tribal_development[i] += HH_score_df['S_Intensity_of_Tribal_development'][j]
                Total_C_Intensity_of_Tribal_development[i] += HH_score_df['C_Intensity_of_Tribal_development'][j]
                Total_G_Intensity_of_Tribal_development[i] += HH_score_df['G_Intensity_of_Tribal_development'][j]
                Total_Intensity_of_Tribal_development[i] += HH_score_df['Intensity_of_Tribal_development'][j]

        Total_H_Incidence_of_Tribal_development[i] = round(Total_H_Incidence_of_Tribal_development[i],3)
        Total_E_Incidence_of_Tribal_development[i] = round(Total_E_Incidence_of_Tribal_development[i],3)
        Total_S_Incidence_of_Tribal_development[i] = round(Total_S_Incidence_of_Tribal_development[i],3)
        Total_C_Incidence_of_Tribal_development[i] = round(Total_C_Incidence_of_Tribal_development[i],3)
        Total_G_Incidence_of_Tribal_development[i] = round(Total_G_Incidence_of_Tribal_development[i],3)
        Total_Incidence_of_Tribal_development[i] = round(Total_Incidence_of_Tribal_development[i],2)
        Total_H_Intensity_of_Tribal_development[i] = round(Total_H_Intensity_of_Tribal_development[i],3)
        Total_E_Intensity_of_Tribal_development[i] = round(Total_E_Intensity_of_Tribal_development[i],3)
        Total_S_Intensity_of_Tribal_development[i] = round(Total_S_Intensity_of_Tribal_development[i],3)
        Total_C_Intensity_of_Tribal_development[i] = round(Total_C_Intensity_of_Tribal_development[i],3)
        Total_G_Intensity_of_Tribal_development[i] = round(Total_G_Intensity_of_Tribal_development[i],3)
        Total_Intensity_of_Tribal_development[i] = round(Total_Intensity_of_Tribal_development[i],2)

    Tribe_cum_score_df['Total_H_Incidence_of_Tribal_development'] = Total_H_Incidence_of_Tribal_development
    Tribe_cum_score_df['Total_E_Incidence_of_Tribal_development'] = Total_E_Incidence_of_Tribal_development
    Tribe_cum_score_df['Total_S_Incidence_of_Tribal_development'] = Total_S_Incidence_of_Tribal_development
    Tribe_cum_score_df['Total_C_Incidence_of_Tribal_development'] = Total_C_Incidence_of_Tribal_development
    Tribe_cum_score_df['Total_G_Incidence_of_Tribal_development'] = Total_G_Incidence_of_Tribal_development
    Tribe_cum_score_df['Total_Incidence_of_Tribal_development'] = Total_Incidence_of_Tribal_development
    Tribe_cum_score_df['Total_H_Intensity_of_Tribal_development'] = Total_H_Intensity_of_Tribal_development
    Tribe_cum_score_df['Total_E_Intensity_of_Tribal_development'] = Total_E_Intensity_of_Tribal_development
    Tribe_cum_score_df['Total_S_Intensity_of_Tribal_development'] = Total_S_Intensity_of_Tribal_development
    Tribe_cum_score_df['Total_C_Intensity_of_Tribal_development'] = Total_C_Intensity_of_Tribal_development
    Tribe_cum_score_df['Total_G_Intensity_of_Tribal_development'] = Total_G_Intensity_of_Tribal_development
    Tribe_cum_score_df['Total_Intensity_of_Tribal_development'] = Total_Intensity_of_Tribal_development

    Tribe_cum_score_df['H_DI'] = round((Tribe_cum_score_df['Total_H_Incidence_of_Tribal_development'] * Tribe_cum_score_df['Total_H_Intensity_of_Tribal_development']),2)
    Tribe_cum_score_df['E_DI'] = round((Tribe_cum_score_df['Total_E_Incidence_of_Tribal_development'] * Tribe_cum_score_df['Total_E_Intensity_of_Tribal_development']),2)
    Tribe_cum_score_df['S_DI'] = round((Tribe_cum_score_df['Total_S_Incidence_of_Tribal_development'] * Tribe_cum_score_df['Total_S_Intensity_of_Tribal_development']),2)
    Tribe_cum_score_df['C_DI'] = round((Tribe_cum_score_df['Total_C_Incidence_of_Tribal_development'] * Tribe_cum_score_df['Total_C_Intensity_of_Tribal_development']),2)
    Tribe_cum_score_df['G_DI'] = round((Tribe_cum_score_df['Total_G_Incidence_of_Tribal_development'] * Tribe_cum_score_df['Total_G_Intensity_of_Tribal_development']),2)
    Tribe_cum_score_df['TDI'] = round((Tribe_cum_score_df['Total_Incidence_of_Tribal_development'] * Tribe_cum_score_df['Total_Intensity_of_Tribal_development']),2)




    HH_score_df.to_excel(settings.EXCEL_FILE_PATH3, index=False)
    print("Result Excel file saved successfully.")

    Tribe_cum_score_df.to_excel(settings.EXCEL_FILE_PATH4, index=False)
    print("Result Excel file saved successfully.")

    import math


    year_list = [year]*total_tribes
    Final_Excel = pd.DataFrame({
        'Year' : year_list,
        'Tribe_N' : unique_tribes,
        'Sum_of_HH_S' : Total_Sum_of_HH_S,
        'H_DI' : Tribe_cum_score_df['H_DI'],
        'E_DI' : Tribe_cum_score_df['E_DI'],
        'S_DI' : Tribe_cum_score_df['S_DI'],
        'C_DI' : Tribe_cum_score_df['C_DI'],
        'G_DI' : Tribe_cum_score_df['G_DI'],
        'Tribal_Incidence' : Tribe_cum_score_df['Total_Incidence_of_Tribal_development'],
        'Tribal_Intensity' : Tribe_cum_score_df['Total_Intensity_of_Tribal_development'],
        'TDI' : Tribe_cum_score_df['TDI']
    })




    UNC_CD_score=[0]*total_tribes
    UNC_IM_score=[0]*total_tribes
    UNC_MC_score=[0]*total_tribes
    UNC_CM_score=[0]*total_tribes
    UNC_FS_score=[0]*total_tribes
    UNC_LE_score=[0]*total_tribes
    UNC_DRO_score=[0]*total_tribes
    UNC_IC_score=[0]*total_tribes
    UNC_OW_score=[0]*total_tribes
    UNC_SANI_score=[0]*total_tribes
    UNC_FUEL_score=[0]*total_tribes
    UNC_DRWA_score=[0]*total_tribes
    UNC_ELECTR_score=[0]*total_tribes
    UNC_ASS_score=[0]*total_tribes
    UNC_LAN_score=[0]*total_tribes
    UNC_ARTS_score=[0]*total_tribes
    UNC_EV_score=[0]*total_tribes
    UNC_MEET_score=[0]*total_tribes

    CEN_CD_score=[0]*total_tribes
    CEN_IM_score=[0]*total_tribes
    CEN_MC_score=[0]*total_tribes
    CEN_CM_score=[0]*total_tribes
    CEN_FS_score=[0]*total_tribes
    CEN_LE_score=[0]*total_tribes
    CEN_DRO_score=[0]*total_tribes
    CEN_IC_score=[0]*total_tribes
    CEN_OW_score=[0]*total_tribes
    CEN_SANI_score=[0]*total_tribes
    CEN_FUEL_score=[0]*total_tribes
    CEN_DRWA_score=[0]*total_tribes
    CEN_ELECTR_score=[0]*total_tribes
    CEN_ASS_score=[0]*total_tribes
    CEN_LAN_score=[0]*total_tribes
    CEN_ARTS_score=[0]*total_tribes
    CEN_EV_score=[0]*total_tribes
    CEN_MEET_score=[0]*total_tribes

    HH_DS = HH_score_df['HH_DS']


    list_CD_contri_to_H = [0]*total_tribes 
    list_IM_contri_to_H = [0]*total_tribes 
    list_MC_contri_to_H = [0]*total_tribes 
    list_CM_contri_to_H = [0]*total_tribes  
    list_FS_contri_to_H = [0]*total_tribes 

    list_LE_contri_to_E = [0]*total_tribes 
    list_DRO_contri_to_E = [0]*total_tribes 

    list_IC_contri_to_S = [0]*total_tribes 
    list_OW_contri_to_S = [0]*total_tribes 
    list_SANI_contri_to_S = [0]*total_tribes 
    list_FUEL_contri_to_S = [0]*total_tribes 
    list_DRWA_contri_to_S = [0]*total_tribes 
    list_ELECTR_contri_to_S = [0]*total_tribes 
    list_ASS_contri_to_S = [0]*total_tribes 

    list_LAN_contri_to_C = [0]*total_tribes 
    list_ARTS_contri_to_C = [0]*total_tribes

    list_EV_contri_to_G = [0]*total_tribes 
    list_MEET_contri_to_G = [0]*total_tribes 

    list_H_contri_to_TDI = [0]*total_tribes 
    list_E_contri_to_TDI = [0]*total_tribes 
    list_S_contri_to_TDI = [0]*total_tribes 
    list_C_contri_to_TDI = [0]*total_tribes 
    list_G_contri_to_TDI = [0]*total_tribes 


    for i in range(total_tribes):

        total_HH_Score_H_CD = 0
        total_HH_Score_H_IMM = 0
        total_HH_Score_H_MC = 0
        total_HH_Score_H_U5CM = 0
        total_HH_Score_H_FS = 0
        total_H_DS = 0

        total_HH_Score_E_LE = 0
        total_HH_Score_E_DRO = 0
        total_E_DS = 0

        total_HH_Score_S_IC = 0
        total_HH_Score_S_OWN = 0
        total_HH_Score_S_SANI = 0
        total_HH_Score_S_Fuel = 0
        total_HH_Score_S_SoDrWa = 0
        total_HH_Score_S_ELECTR = 0
        total_HH_Score_S_ASS = 0
        total_S_DS = 0

        total_HH_Score_C_L = 0
        total_HH_Score_C_Arts = 0
        total_C_DS = 0

        total_HH_Score_G_EV = 0
        total_HH_Score_G_meeting = 0
        total_G_DS = 0

        total_HH_DS = 0

        Sum_of_HH_S = Final_Excel['Sum_of_HH_S'][i]

        if Sum_of_HH_S > 0 :
            for j in range(len(HH_tribe_list)):
                if HH_tribe_list[j] == unique_tribes[i]:
                
                        
                    HH_size = HH_score_df['Sum of HH_S'][j]


                    CD_score_value = (HH_score_df['HH_Score_H_CD'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_H_CD'][j]) or HH_score_df['HH_Score_H_CD'][j] is None) else 0
                    IM_score_value = (HH_score_df['HH_Score_H_IMM'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_H_IMM'][j]) or HH_score_df['HH_Score_H_IMM'][j] is None) else 0
                    MC_score_value = (HH_score_df['HH_Score_H_MC'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_H_MC'][j]) or HH_score_df['HH_Score_H_MC'][j] is None) else 0
                    CM_score_value = (HH_score_df['HH_Score_H_U5CM'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_H_U5CM'][j]) or HH_score_df['HH_Score_H_U5CM'][j] is None) else 0
                    FS_score_value = (HH_score_df['HH_Score_H_FS'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_H_FS'][j]) or HH_score_df['HH_Score_H_FS'][j] is None) else 0
                    LE_score_value = (HH_score_df['HH_Score_E_LE'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_E_LE'][j]) or HH_score_df['HH_Score_E_LE'][j] is None) else 0
                    DRO_score_value = (HH_score_df['HH_Score_E_DRO'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_E_DRO'][j]) or HH_score_df['HH_Score_E_DRO'][j] is None) else 0
                    IC_score_value = (HH_score_df['HH_Score_S_IC'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_S_IC'][j]) or HH_score_df['HH_Score_S_IC'][j] is None) else 0
                    OW_score_value = (HH_score_df['HH_Score_S_OWN'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_S_OWN'][j]) or HH_score_df['HH_Score_S_OWN'][j] is None) else 0
                    SANI_score_value = (HH_score_df['HH_Score_S_SANI'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_S_SANI'][j]) or HH_score_df['HH_Score_S_SANI'][j] is None) else 0
                    FUEL_score_value = (HH_score_df['HH_Score_S_Fuel'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_S_Fuel'][j]) or HH_score_df['HH_Score_S_Fuel'][j] is None) else 0
                    DRWA_score_value = (HH_score_df['HH_Score_S_SoDrWa'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_S_SoDrWa'][j]) or HH_score_df['HH_Score_S_SoDrWa'][j] is None) else 0
                    ELECTR_score_value = (HH_score_df['HH_Score_S_ELECTR'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_S_ELECTR'][j]) or HH_score_df['HH_Score_S_ELECTR'][j] is None) else 0
                    ASS_score_value = (HH_score_df['HH_Score_S_ASS'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_S_ASS'][j]) or HH_score_df['HH_Score_S_ASS'][j] is None) else 0
                    LAN_score_value = (HH_score_df['HH_Score_C_L'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_C_L'][j]) or HH_score_df['HH_Score_C_L'][j] is None) else 0
                    ARTS_score_value = (HH_score_df['HH_Score_C_Arts'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_C_Arts'][j]) or HH_score_df['HH_Score_C_Arts'][j] is None) else 0
                    EV_score_value = (HH_score_df['HH_Score_G_EV'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_G_EV'][j]) or HH_score_df['HH_Score_G_EV'][j] is None) else 0
                    MEET_score_value = (HH_score_df['HH_Score_G_meeting'][j] * HH_size / Sum_of_HH_S) if not (math.isnan(HH_score_df['HH_Score_G_meeting'][j]) or HH_score_df['HH_Score_G_meeting'][j] is None) else 0

                    UNC_CD_score[i] += CD_score_value
                    UNC_IM_score[i] += IM_score_value
                    UNC_MC_score[i] += MC_score_value
                    UNC_CM_score[i] += CM_score_value
                    UNC_FS_score[i] += FS_score_value
                    UNC_LE_score[i] += LE_score_value
                    UNC_DRO_score[i] += DRO_score_value
                    UNC_IC_score[i] += IC_score_value
                    UNC_OW_score[i] += OW_score_value
                    UNC_SANI_score[i] += SANI_score_value
                    UNC_FUEL_score[i] += FUEL_score_value
                    UNC_DRWA_score[i] += DRWA_score_value
                    UNC_ELECTR_score[i] += ELECTR_score_value
                    UNC_ASS_score[i] += ASS_score_value
                    UNC_LAN_score[i] += LAN_score_value
                    UNC_ARTS_score[i] += ARTS_score_value
                    UNC_EV_score[i] += EV_score_value
                    UNC_MEET_score[i] += MEET_score_value


                    total_HH_Score_H_CD += round((HH_score_df['HH_Score_H_CD'][j] * HH_score_df['H_weightage'][j]), 2) if not math.isnan(HH_score_df['HH_Score_H_CD'][j]) else 0
                    total_HH_Score_H_IMM += round((HH_score_df['HH_Score_H_IMM'][j] * HH_score_df['H_weightage'][j]), 2) if not math.isnan(HH_score_df['HH_Score_H_IMM'][j]) else 0
                    total_HH_Score_H_MC += round((HH_score_df['HH_Score_H_MC'][j] * HH_score_df['H_weightage'][j]), 2) if not math.isnan(HH_score_df['HH_Score_H_MC'][j]) else 0
                    total_HH_Score_H_U5CM += round((HH_score_df['HH_Score_H_U5CM'][j] * HH_score_df['H_weightage'][j]), 2) if not math.isnan(HH_score_df['HH_Score_H_U5CM'][j]) else 0
                    total_HH_Score_H_FS += round((HH_score_df['HH_Score_H_FS'][j] * HH_score_df['H_weightage'][j]), 2) if not math.isnan(HH_score_df['HH_Score_H_FS'][j]) else 0
                    total_H_DS += HH_score_df['H_DS'][j]

                    total_HH_Score_E_LE += round((HH_score_df['HH_Score_E_LE'][j] * HH_score_df['E_weightage'][j]), 2) if not math.isnan(HH_score_df['HH_Score_E_LE'][j]) else 0
                    total_HH_Score_E_DRO += round((HH_score_df['HH_Score_E_DRO'][j] * HH_score_df['E_weightage'][j]), 2) if not math.isnan(HH_score_df['HH_Score_E_DRO'][j]) else 0
                    total_E_DS += HH_score_df['E_DS'][j]

                    total_HH_Score_S_IC += round((HH_score_df['HH_Score_S_IC'][j] * HH_score_df['S_weightage'][j]), 2) if not math.isnan(HH_score_df['HH_Score_S_IC'][j]) else 0
                    total_HH_Score_S_OWN += round((HH_score_df['HH_Score_S_OWN'][j] * HH_score_df['S_weightage'][j]), 2) if not math.isnan(HH_score_df['HH_Score_S_OWN'][j]) else 0
                    total_HH_Score_S_SANI += round((HH_score_df['HH_Score_S_SANI'][j] * HH_score_df['S_weightage'][j]), 2) if not math.isnan(HH_score_df['HH_Score_S_SANI'][j]) else 0
                    total_HH_Score_S_Fuel += round((HH_score_df['HH_Score_S_Fuel'][j] * HH_score_df['S_weightage'][j]), 2) if not math.isnan(HH_score_df['HH_Score_S_Fuel'][j]) else 0
                    total_HH_Score_S_SoDrWa += round((HH_score_df['HH_Score_S_SoDrWa'][j] * HH_score_df['S_weightage'][j]), 2) if not math.isnan(HH_score_df['HH_Score_S_SoDrWa'][j]) else 0
                    total_HH_Score_S_ELECTR += round((HH_score_df['HH_Score_S_ELECTR'][j] * HH_score_df['S_weightage'][j]), 2) if not math.isnan(HH_score_df['HH_Score_S_ELECTR'][j]) else 0
                    total_HH_Score_S_ASS += round((HH_score_df['HH_Score_S_ASS'][j] * HH_score_df['S_weightage'][j]), 2) if not math.isnan(HH_score_df['HH_Score_S_ASS'][j]) else 0
                    total_S_DS += HH_score_df['S_DS'][j]

                    total_HH_Score_C_L += round((HH_score_df['HH_Score_C_L'][j] * HH_score_df['C_weightage'][j]), 2) if not math.isnan(HH_score_df['HH_Score_C_L'][j]) else 0
                    total_HH_Score_C_Arts += round((HH_score_df['HH_Score_C_Arts'][j] * HH_score_df['C_weightage'][j]), 2) if not math.isnan(HH_score_df['HH_Score_C_Arts'][j]) else 0
                    total_C_DS += HH_score_df['C_DS'][j]

                    total_HH_Score_G_EV += round((HH_score_df['HH_Score_G_EV'][j] * HH_score_df['G_weightage'][j]), 2) if not math.isnan(HH_score_df['HH_Score_G_EV'][j]) else 0
                    total_HH_Score_G_meeting += round((HH_score_df['HH_Score_G_meeting'][j] * HH_score_df['G_weightage'][j]), 2) if not math.isnan(HH_score_df['HH_Score_G_meeting'][j]) else 0
                    total_G_DS += HH_score_df['G_DS'][j]

                    total_HH_DS += HH_score_df['HH_DS'][j]


                    if HH_DS[j] > 0.33:
                        CEN_CD_score[i] +=     CD_score_value
                        CEN_IM_score[i] +=     IM_score_value
                        CEN_MC_score[i] +=     MC_score_value
                        CEN_CM_score[i] +=     CM_score_value
                        CEN_FS_score[i] +=     FS_score_value
                        CEN_LE_score[i] +=     LE_score_value
                        CEN_DRO_score[i] +=    DRO_score_value
                        CEN_IC_score[i] +=     IC_score_value
                        CEN_OW_score[i] +=     OW_score_value
                        CEN_SANI_score[i] +=   SANI_score_value
                        CEN_FUEL_score[i] +=   FUEL_score_value
                        CEN_DRWA_score[i] +=   DRWA_score_value
                        CEN_ELECTR_score[i] += ELECTR_score_value
                        CEN_ASS_score[i] +=    ASS_score_value
                        CEN_LAN_score[i] +=    LAN_score_value
                        CEN_ARTS_score[i] +=   ARTS_score_value 
                        CEN_EV_score[i] +=     EV_score_value
                        CEN_MEET_score[i] +=   MEET_score_value


            CD_contri_to_H = total_HH_Score_H_CD / total_H_DS if total_H_DS != 0 else 0
            IM_contri_to_H = total_HH_Score_H_IMM / total_H_DS if total_H_DS != 0 else 0
            MC_contri_to_H = total_HH_Score_H_MC / total_H_DS if total_H_DS != 0 else 0
            CM_contri_to_H = total_HH_Score_H_U5CM / total_H_DS if total_H_DS != 0 else 0
            FS_contri_to_H = total_HH_Score_H_FS / total_H_DS if total_H_DS != 0 else 0

            LE_contri_to_E = total_HH_Score_E_LE / total_E_DS if total_E_DS != 0 else 0
            DRO_contri_to_E = total_HH_Score_E_DRO / total_E_DS if total_E_DS != 0 else 0

            IC_contri_to_S = total_HH_Score_S_IC / total_S_DS if total_S_DS != 0 else 0
            OW_contri_to_S = total_HH_Score_S_OWN / total_S_DS if total_S_DS != 0 else 0
            SANI_contri_to_S = total_HH_Score_S_SANI / total_S_DS if total_S_DS != 0 else 0
            FUEL_contri_to_S = total_HH_Score_S_Fuel / total_S_DS if total_S_DS != 0 else 0
            DRWA_contri_to_S = total_HH_Score_S_SoDrWa / total_S_DS if total_S_DS != 0 else 0
            ELECTR_contri_to_S = total_HH_Score_S_ELECTR / total_S_DS if total_S_DS != 0 else 0
            ASS_contri_to_S = total_HH_Score_S_ASS / total_H_DS if total_H_DS != 0 else 0

            LAN_contri_to_C = total_HH_Score_C_L / total_C_DS if total_C_DS != 0 else 0
            ARTS_contri_to_C = total_HH_Score_C_Arts / total_C_DS if total_C_DS != 0 else 0

            EV_contri_to_G = total_HH_Score_G_EV / total_G_DS if total_G_DS != 0 else 0
            MEET_contri_to_G = total_HH_Score_G_meeting / total_G_DS if total_G_DS != 0 else 0

            H_contri_to_TDI = total_H_DS / total_HH_DS if total_HH_DS != 0 else 0
            E_contri_to_TDI = total_E_DS / total_HH_DS if total_HH_DS != 0 else 0
            S_contri_to_TDI = total_S_DS / total_HH_DS if total_HH_DS != 0 else 0
            C_contri_to_TDI = total_C_DS / total_HH_DS if total_HH_DS != 0 else 0
            G_contri_to_TDI = total_G_DS / total_HH_DS if total_HH_DS != 0 else 0

            UNC_CD_score[i]= round(UNC_CD_score[i],2)*100
            UNC_IM_score[i]= round(UNC_IM_score[i],2)*100
            UNC_MC_score[i]= round(UNC_MC_score[i],2)*100
            UNC_CM_score[i]= round(UNC_CM_score[i],2)*100
            UNC_FS_score[i]= round(UNC_FS_score[i],2)*100
            UNC_LE_score[i]= round(UNC_LE_score[i],2)*100
            UNC_DRO_score[i]= round(UNC_DRO_score[i],2)*100
            UNC_IC_score[i]= round(UNC_IC_score[i],2)*100
            UNC_OW_score[i]= round(UNC_OW_score[i],2)*100
            UNC_SANI_score[i]= round(UNC_SANI_score[i],2)*100
            UNC_FUEL_score[i]= round(UNC_FUEL_score[i],2)*100
            UNC_DRWA_score[i]= round(UNC_DRWA_score[i],2)*100
            UNC_ELECTR_score[i]= round(UNC_ELECTR_score[i],2)*100
            UNC_ASS_score[i]= round(UNC_ASS_score[i],2)*100
            UNC_LAN_score[i]= round(UNC_LAN_score[i],2)*100
            UNC_ARTS_score[i]= round(UNC_ARTS_score[i],2)*100
            UNC_EV_score[i]= round(UNC_EV_score[i],2)*100
            UNC_MEET_score[i]= round(UNC_MEET_score[i],2)*100
            CEN_CD_score[i]= round(CEN_CD_score[i],2)*100
            CEN_IM_score[i]= round(CEN_IM_score[i],2)*100
            CEN_MC_score[i]= round(CEN_MC_score[i],2)*100
            CEN_CM_score[i]= round(CEN_CM_score[i],2)*100
            CEN_FS_score[i]= round(CEN_FS_score[i],2)*100
            CEN_LE_score[i]= round(CEN_LE_score[i],2)*100
            CEN_DRO_score[i]= round(CEN_DRO_score[i],2)*100
            CEN_IC_score[i]= round(CEN_IC_score[i],2)*100
            CEN_OW_score[i]= round(CEN_OW_score[i],2)*100
            CEN_SANI_score[i]= round(CEN_SANI_score[i],2)*100
            CEN_FUEL_score[i]= round(CEN_FUEL_score[i],2)*100
            CEN_DRWA_score[i]= round(CEN_DRWA_score[i],2)*100
            CEN_ELECTR_score[i]= round(CEN_ELECTR_score[i],2)*100
            CEN_ASS_score[i]= round(CEN_ASS_score[i],2)*100
            CEN_LAN_score[i]= round(CEN_LAN_score[i],2)*100
            CEN_ARTS_score[i]= round(CEN_ARTS_score[i],2)*100
            CEN_EV_score[i]= round(CEN_EV_score[i],2)*100
            CEN_MEET_score[i]= round(CEN_MEET_score[i],2)*100

            list_CD_contri_to_H[i]= round(CD_contri_to_H*100,2)
            list_IM_contri_to_H[i]= round(IM_contri_to_H*100,2)
            list_MC_contri_to_H[i]= round(MC_contri_to_H*100,2)
            list_CM_contri_to_H[i]= round(CM_contri_to_H*100,2)
            list_FS_contri_to_H[i]= round(FS_contri_to_H*100,2)

            list_LE_contri_to_E[i]= round(LE_contri_to_E*100,2)
            list_DRO_contri_to_E[i]= round(DRO_contri_to_E*100,2)

            list_IC_contri_to_S[i]= round(IC_contri_to_S*100,2)
            list_OW_contri_to_S[i]= round(OW_contri_to_S*100,2)
            list_SANI_contri_to_S[i]= round(SANI_contri_to_S*100,2)
            list_FUEL_contri_to_S[i]= round(FUEL_contri_to_S*100,2)
            list_DRWA_contri_to_S[i]= round(DRWA_contri_to_S*100,2)
            list_ELECTR_contri_to_S[i]= round(ELECTR_contri_to_S*100,2)
            list_ASS_contri_to_S[i]= round(ASS_contri_to_S*100,2)

            list_LAN_contri_to_C[i]= round(LAN_contri_to_C*100,2)
            list_ARTS_contri_to_C[i]= round(ARTS_contri_to_C*100,2)

            list_EV_contri_to_G[i]= round(EV_contri_to_G*100,2)
            list_MEET_contri_to_G[i]= round(MEET_contri_to_G*100,2)

            list_H_contri_to_TDI[i] = round(H_contri_to_TDI*100,2)
            list_E_contri_to_TDI[i] = round(E_contri_to_TDI*100,2)
            list_S_contri_to_TDI[i] = round(S_contri_to_TDI*100,2)
            list_C_contri_to_TDI[i] = round(C_contri_to_TDI*100,2)
            list_G_contri_to_TDI[i] = round(G_contri_to_TDI*100,2)


    Final_Excel['UNC_CD_score'] = UNC_CD_score
    Final_Excel['UNC_IM_score'] = UNC_IM_score
    Final_Excel['UNC_MC_score'] = UNC_MC_score
    Final_Excel['UNC_CM_score'] = UNC_CM_score
    Final_Excel['UNC_FS_score'] = UNC_FS_score
    Final_Excel['UNC_LE_score'] = UNC_LE_score
    Final_Excel['UNC_DRO_score'] = UNC_DRO_score
    Final_Excel['UNC_IC_score'] = UNC_IC_score
    Final_Excel['UNC_OW_score'] = UNC_OW_score
    Final_Excel['UNC_SANI_score'] = UNC_SANI_score
    Final_Excel['UNC_FUEL_score'] = UNC_FUEL_score
    Final_Excel['UNC_DRWA_score'] = UNC_DRWA_score
    Final_Excel['UNC_ELECTR_score'] = UNC_ELECTR_score
    Final_Excel['UNC_ASS_score'] = UNC_ASS_score
    Final_Excel['UNC_LAN_score'] = UNC_LAN_score
    Final_Excel['UNC_ARTS_score'] = UNC_ARTS_score
    Final_Excel['UNC_EV_score'] = UNC_EV_score
    Final_Excel['UNC_MEET_score'] = UNC_MEET_score
    Final_Excel['CEN_CD_score'] = CEN_CD_score
    Final_Excel['CEN_IM_score'] = CEN_IM_score
    Final_Excel['CEN_MC_score'] = CEN_MC_score
    Final_Excel['CEN_CM_score'] = CEN_CM_score
    Final_Excel['CEN_FS_score'] = CEN_FS_score
    Final_Excel['CEN_LE_score'] = CEN_LE_score
    Final_Excel['CEN_DRO_score'] = CEN_DRO_score
    Final_Excel['CEN_IC_score'] = CEN_IC_score
    Final_Excel['CEN_OW_score'] = CEN_OW_score
    Final_Excel['CEN_SANI_score'] = CEN_SANI_score
    Final_Excel['CEN_FUEL_score'] = CEN_FUEL_score
    Final_Excel['CEN_DRWA_score'] = CEN_DRWA_score
    Final_Excel['CEN_ELECTR_score'] = CEN_ELECTR_score
    Final_Excel['CEN_ASS_score'] = CEN_ASS_score
    Final_Excel['CEN_LAN_score'] = CEN_LAN_score
    Final_Excel['CEN_ARTS_score'] = CEN_ARTS_score
    Final_Excel['CEN_EV_score'] = CEN_EV_score
    Final_Excel['CEN_MEET_score'] = CEN_MEET_score



    Final_Excel['CD_contri_to_H'] = list_CD_contri_to_H
    Final_Excel['IM_contri_to_H'] = list_IM_contri_to_H
    Final_Excel['MC_contri_to_H'] = list_MC_contri_to_H
    Final_Excel['CM_contri_to_H'] = list_CM_contri_to_H
    Final_Excel['FS_contri_to_H'] = list_FS_contri_to_H

    Final_Excel['LE_contri_to_E'] = list_LE_contri_to_E
    Final_Excel['DRO_contri_to_E'] = list_DRO_contri_to_E

    Final_Excel['IC_contri_to_S'] = list_IC_contri_to_S
    Final_Excel['OW_contri_to_S'] = list_OW_contri_to_S
    Final_Excel['SANI_contri_to_S'] = list_SANI_contri_to_S
    Final_Excel['FUEL_contri_to_S'] = list_FUEL_contri_to_S
    Final_Excel['DRWA_contri_to_S'] = list_DRWA_contri_to_S
    Final_Excel['ELECTR_contri_to_S'] = list_ELECTR_contri_to_S
    Final_Excel['ASS_contri_to_S'] = list_ASS_contri_to_S

    Final_Excel['LAN_contri_to_C'] = list_LAN_contri_to_C
    Final_Excel['ARTS_contri_to_C'] = list_ARTS_contri_to_C

    Final_Excel['EV_contri_to_G'] = list_EV_contri_to_G
    Final_Excel['MEET_contri_to_G'] = list_MEET_contri_to_G

    Final_Excel['H_contri_to_TDI'] = list_H_contri_to_TDI
    Final_Excel['E_contri_to_TDI'] = list_E_contri_to_TDI
    Final_Excel['S_contri_to_TDI'] = list_S_contri_to_TDI
    Final_Excel['C_contri_to_TDI'] = list_C_contri_to_TDI
    Final_Excel['G_contri_to_TDI'] = list_G_contri_to_TDI
        
                
    Final_Excel.to_excel(settings.EXCEL_FILE_PATH5, index=False)
    print("Result Excel file saved successfully.")


    unique_Block_name = []
    unique_village_name = []
    unique_District_name = []


    for x in Block_name:
        if x not in unique_Block_name:
            unique_Block_name.append(x)
    for x in village_name:
        if x not in unique_village_name:
            unique_village_name.append(x)
    for x in District_name:
        if x not in unique_District_name:
            unique_District_name.append(x)


    # HH_village_name_list = [""] * len(unique_fid)
    # HH_District_name_list = [""] * len(unique_fid)
    # HH_Block_name_list = [""] * len(unique_fid)

    # for i in range(len(unique_fid)):
    #     for j in range(len(total_fid)):

    #         if unique_fid[i] == total_fid[j]:
    #             HH_size_list[i] += 1
    #             if HH_tribe_list[i] == "":
    #                 HH_tribe_list[i] = tribes[j]
    #                 HH_village_name_list[i]=village_name[j]
    #                 HH_District_name_list[i]=District_name[j]
    #                 HH_Block_name_list[i]=Block_name[j]


    # HH_score_df['HH_village_name_list'] = HH_village_name_list
    # HH_score_df['HH_Block_name_list'] = HH_Block_name_list
    # HH_score_df['HH_District_name_list'] = HH_District_name_list

    # village_name_list = [""] * len(unique_tribes)
    # Block_name_list = [""] * len(unique_tribes)
    # District_name_list = [""] * len(unique_tribes)
    # for i in range(len(unique_tribes)):
    #     for j in range(len(tribes)):
    #         if tribes[j] == unique_tribes[i] and village_name_list[i].find(village_name[j]) == -1:
    #             village_name_list[i] += village_name[j] + ', '
    #         if tribes[j] == unique_tribes[i] and Block_name_list[i].find(Block_name[j]) == -1:
    #             Block_name_list[i] += Block_name[j] + ', '
    #         if tribes[j] == unique_tribes[i] and District_name_list[i].find(District_name[j]) == -1:
    #             District_name_list[i] += District_name[j] + ', '


    
    from .models import Tribe
    from accounts.models import Report_Excel
    from django.http import HttpResponse
    from .forms import TribeForm
    from django.db import IntegrityError
    from io import BytesIO
    from django.core.files.base import ContentFile

        

    for index, row in Final_Excel.iterrows():
        slug = row['Tribe_N'].strip()
        
            
        
        
        if not slug in unique_tribes:
            print( HttpResponse(f'Tribe with slug "{slug}" not found. Check your Excel for valid tribe name.'))
        
                
            # try:
            #     tribe, created = Tribe.objects.get_or_create(user=user, year=year, name=slug)
            #     if created:
            #         # The tribe was created successfully
            #         return HttpResponse('Tribe created successfully!')
            #     else:
            #         # The tribe already exists
            #         return HttpResponse('Tribe already exists. Cannot create duplicate.')
            # except IntegrityError:
            #     # Handle other potential database integrity errors
            #     return HttpResponse('Error creating tribe. Please try again.')

        
        tribe_data = {
            'user' : user,
            'year' : year,
            'name' : row['Tribe_N'],
            'total_tribals' : row['Sum_of_HH_S'],
            'H_DI' : row['H_DI'],
            'E_DI' : row['E_DI'],
            'S_DI' : row['S_DI'],
            'C_DI' : row['C_DI'],
            'G_DI' : row['G_DI'],
            'tribal_incidence' : row['Tribal_Incidence'],
            'tribal_intensity' : row['Tribal_Intensity'],
            'TDI' : row['TDI'],
            'UNC_CD_score' : row['UNC_CD_score'],
            'UNC_IM_score' : row['UNC_IM_score'],
            'UNC_MC_score' : row['UNC_MC_score'],
            'UNC_CM_score' : row['UNC_CM_score'],
            'UNC_FS_score' : row['UNC_FS_score'],
            'UNC_LE_score' : row['UNC_LE_score'],
            'UNC_DRO_score' : row['UNC_DRO_score'],
            'UNC_IC_score' : row['UNC_IC_score'],
            'UNC_OW_score' : row['UNC_OW_score'],
            'UNC_SANI_score' : row['UNC_SANI_score'],
            'UNC_FUEL_score' : row['UNC_FUEL_score'],
            'UNC_DRWA_score' : row['UNC_DRWA_score'],
            'UNC_ELECTR_score' : row['UNC_ELECTR_score'],
            'UNC_ASS_score' : row['UNC_ASS_score'],
            'UNC_LAN_score' : row['UNC_LAN_score'],
            'UNC_ARTS_score' : row['UNC_ARTS_score'],
            'UNC_EV_score' : row['UNC_EV_score'],
            'UNC_MEET_score' : row['UNC_MEET_score'],
            'CEN_CD_score' : row['CEN_CD_score'],
            'CEN_IM_score' : row['CEN_IM_score'],
            'CEN_MC_score' : row['CEN_MC_score'],
            'CEN_CM_score' : row['CEN_CM_score'],
            'CEN_FS_score' : row['CEN_FS_score'],
            'CEN_LE_score' : row['CEN_LE_score'],
            'CEN_DRO_score' : row['CEN_DRO_score'],
            'CEN_IC_score' : row['CEN_IC_score'],
            'CEN_OW_score' : row['CEN_OW_score'],
            'CEN_SANI_score' : row['CEN_SANI_score'],
            'CEN_FUEL_score' : row['CEN_FUEL_score'],
            'CEN_DRWA_score' : row['CEN_DRWA_score'],
            'CEN_ELECTR_score' : row['CEN_ELECTR_score'],
            'CEN_ASS_score' : row['CEN_ASS_score'],
            'CEN_LAN_score' : row['CEN_LAN_score'],
            'CEN_ARTS_score' : row['CEN_ARTS_score'],
            'CEN_EV_score' : row['CEN_EV_score'],
            'CEN_MEET_score' : row['CEN_MEET_score'],
            'CD_contri_to_H': row['CD_contri_to_H'],
            'IM_contri_to_H': row['IM_contri_to_H'],
            'MC_contri_to_H': row['MC_contri_to_H'],
            'CM_contri_to_H': row['CM_contri_to_H'],
            'FS_contri_to_H': row['FS_contri_to_H'],

            'LE_contri_to_E': row['LE_contri_to_E'],
            'DRO_contri_to_E': row['DRO_contri_to_E'],

            'IC_contri_to_S': row['IC_contri_to_S'],
            'OW_contri_to_S': row['OW_contri_to_S'],
            'SANI_contri_to_S': row['SANI_contri_to_S'],
            'FUEL_contri_to_S': row['FUEL_contri_to_S'],
            'DRWA_contri_to_S': row['DRWA_contri_to_S'],
            'ELECTR_contri_to_S': row['ELECTR_contri_to_S'],
            'ASS_contri_to_S': row['ASS_contri_to_S'],

            'LAN_contri_to_C': row['LAN_contri_to_C'],
            'ARTS_contri_to_C': row['ARTS_contri_to_C'],

            'EV_contri_to_G': row['EV_contri_to_G'],
            'MEET_contri_to_G': row['MEET_contri_to_G'],

            'H_contri_to_TDI': row['H_contri_to_TDI'],
            'E_contri_to_TDI': row['E_contri_to_TDI'],
            'S_contri_to_TDI': row['S_contri_to_TDI'],
            'C_contri_to_TDI': row['C_contri_to_TDI'],
            'G_contri_to_TDI': row['G_contri_to_TDI'],
        }

        tribe_form = TribeForm(tribe_data)
        if tribe_form.is_valid():
            tribe_object = tribe_form.save(commit=False)
            tribe_object.save()

        else:
            print(tribe_form.errors)

    for i in range(len(unique_tribes)):
        slug = unique_tribes[i].strip()
        
        try:
            tribe = Tribe.objects.get(name=slug, user=user, year=year)
            details_list = [
            {"Block_name_list": village_block_list[i], "District_name_list": District_name_list[i]}
        ]

            tribe.village_details = details_list
            
            tribe.save()
        except Tribe.DoesNotExist:
            print(HttpResponse(f'Tribe with slug "{slug}" not found. Check your Excel for a valid tribe name.'))


    excel_buffer = BytesIO()
    Final_Excel.to_excel(excel_buffer, index=False)

    excel_file_instance = Report_Excel(user=user, year=year)
    excel_file_instance.file.save(f'reports/{user.username}_{year}.xlsx', ContentFile(excel_buffer.getvalue()))
    excel_file_instance.save()