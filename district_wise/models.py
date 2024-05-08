from django.db import models
from django.utils.text import slugify
import math
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class District(models.Model):
    code = models.FloatField(null=True, blank=True)
    name = models.CharField(null=True, blank=True,max_length=30)
    slug = models.SlugField(null=True, blank=True)
    year=models.IntegerField(null=True, blank=True)
    st_population = models.FloatField(null=True, blank=True,)
    total_population = models.FloatField(null=True, blank=True,)
    #HEALTH
    W_BMI = models.FloatField(null=True, blank=True,)
    C_UW = models.FloatField(null=True, blank=True,)
    AN_W = models.FloatField(null=True, blank=True,)
    AN_C = models.FloatField(null=True, blank=True,)  
    AHC_ANC = models.FloatField(null=True, blank=True,)
    AHC_Full_ANC = models.FloatField(null=True, blank=True,)
    AHC_PNC = models.FloatField(null=True, blank=True,)
    AHC_HI = models.FloatField(null=True, blank=True,)
    
    #EDUCATION
    Enrollment = models.FloatField(null=True, blank=True,)
    Equity = models.FloatField(null=True, blank=True,)
    E_DropRate = models.FloatField(null=True, blank=True,)

    #SOL
    S_Sani = models.FloatField(null=True, blank=True,)
    S_CoFu = models.FloatField(null=True, blank=True,)
    S_DrWa = models.FloatField(null=True, blank=True,)
    S_Elec = models.FloatField(null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='districts',default=settings.ADMIN_USER_PHONE_NUMBER)

    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(District, self).save(*args, **kwargs)
    
    
    def __str__(self):
        return f"{self.name} - {self.year}"

    def get_multiplier(self):
        if self.st_population and self.total_population:
            ans = self.st_population/self.total_population
            return ans
    

    def get_indicator_st_scores(self):
        multiplier = self.get_multiplier()

        #HEALTH
        W_BMI_score = self.W_BMI*multiplier
        C_UW_score = self.C_UW*multiplier
        AN_W_score = self.AN_W*multiplier
        AN_C_score = self.AN_C*multiplier
        AHC_ANC_score = self.AHC_ANC*multiplier
        AHC_Full_ANC_score = self.AHC_Full_ANC*multiplier
        AHC_PNC_score = self.AHC_PNC*multiplier
        AHC_HI_score = self.AHC_HI*multiplier

        #EDUCATION
        Enrollment_score = self.Enrollment
        Equity_score = self.Equity
        E_DropRate_score = self.E_DropRate

        #SOL
        S_Sani_score = self.S_Sani*multiplier
        S_CoFu_score = self.S_CoFu*multiplier
        S_DrWa_score = self.S_DrWa*multiplier
        S_Elec_score = self.S_Elec*multiplier

        ind_arr = [
            W_BMI_score,C_UW_score,AN_W_score,AN_C_score,AHC_ANC_score,AHC_Full_ANC_score,AHC_PNC_score,AHC_HI_score,Enrollment_score, Equity_score, E_DropRate_score,S_Sani_score,S_CoFu_score,S_DrWa_score,S_Elec_score
            ]  #Index 0 to 6 are subindicators of health

        rounded_ind_arr = [round(value, 1) for value in ind_arr]
        return rounded_ind_arr
    
    #get all districts
    @classmethod
    def get_all_objects(cls):
        return cls.objects.all()
    

    # Class-level variables to store the calculated values
    _max_arr = None
    _min_arr = None

    #Get max and min scores for all indicators/sub I
    def get_max_min_ind_scores(self):
        # Check if the values have already been calculated and stored
        if District._max_arr is not None and District._min_arr is not None:
            return District._max_arr, District._min_arr

        districts = self.get_all_objects()
        max_arr = [0.0] * 15
        min_arr = [0.0] * 15

        for i in range(15):
            one_ind_scores = []
            for district in districts:
                score = district.get_indicator_st_scores()[i]
                one_ind_scores.append(score)
            max_val = max(one_ind_scores)
            min_val = min(one_ind_scores)
            max_arr[i] = round(max_val,1)
            min_arr[i] = round(min_val,1)

        # Store the calculated values in class-level variables
        District._max_arr = max_arr
        District._min_arr = min_arr

        return [max_arr, min_arr]

        
    
    def get_normalized_ind_scores(self):

        max_arr = self.get_max_min_ind_scores()[0]
        min_arr = self.get_max_min_ind_scores()[1]
        norm_arr = [0.0]*15
        scores = self.get_indicator_st_scores()

        for i in range(15):
            max = max_arr[i]
            min = min_arr[i]
            act_val = scores[i]
            if(i>=0 and i<4 or i==9 or i==10):
                norm_value = (max-act_val)/(max-min)
            else:
                norm_value = (act_val-min)/(max-min)
            norm_arr[i] = norm_value
        
        return norm_arr
        x = 6  # Round off number

    def  get_normalized_final_ind_scores(self):
            x = 2
            norm_arr=self.get_normalized_ind_scores()
            norm_arr_final = [
                round(norm_arr[0],x),round(norm_arr[1],x),round((norm_arr[0] + norm_arr[1]) / 2, x), round(norm_arr[2],x),round(norm_arr[3],x),round((norm_arr[2] + norm_arr[3]) / 2, x),round(norm_arr[4],x), round(norm_arr[5],x), round(norm_arr[6],x),round((norm_arr[4] + norm_arr[5] + norm_arr[6]) / 3, x), round(norm_arr[7], x),
                round(norm_arr[8], x), round(norm_arr[9], x), round(norm_arr[10], x),
                round(norm_arr[11], x), round(norm_arr[12], x), round(norm_arr[13], x), round(norm_arr[14], x)]
            
            return norm_arr_final
    
    def get_avg_ind_scores(self):
        norm_arr=self.get_normalized_ind_scores()
        norm_arr_final = [
        [(norm_arr[0] + norm_arr[1]) / 2, (norm_arr[2] + norm_arr[3]) / 2, (norm_arr[4] + norm_arr[5] + norm_arr[6]) / 3,
        norm_arr[7]],
        [norm_arr[8], norm_arr[9], norm_arr[10]],
        [norm_arr[11], norm_arr[12], norm_arr[13], norm_arr[14]]
        ]
        return norm_arr_final
    
    def get_dimension_scores(self):
        norm_arr = self.get_avg_ind_scores()
        dimension_arr = []
        for i in norm_arr:
            sum =0
            for j in i:
                sum += j
            avg = sum/len(i)
            dimension_arr.append(round(avg,2))

        return dimension_arr
    
    # def get_score(self):
    #     dimension_scores = self.get_dimension_scores()
    #     normalized_final_ind_scores=self.get_normalized_final_ind_scores()
    #     avg_ind_scores=self.get_avg_ind_scores()
    #     arr=[dimension_scores]



    def get_tdi_score(self):
        dimension_scores = self.get_dimension_scores()
        total = sum(dimension_scores)
        length = len(dimension_scores)
        prod = 1

        for i in dimension_scores:
            prod = prod*i

        arithmetic_tdi = round(total/length,2)
        geometric_tdi = round(pow(prod,1/3),2)

        return [geometric_tdi, arithmetic_tdi]
    

    def get_indicator_contri_to_dimension(self):
        normalized_ind_scores = self.get_avg_ind_scores()
        ind_sum = []
        
        for i in normalized_ind_scores:
            sum = 0
            for j in i:
                sum += j
            ind_sum.append(sum)
        

        indicator_contri_to_dimension = []

        for i in range(0,3):
            ind_contri_arr = []
            for k in range(len(normalized_ind_scores[i])):
                if ind_sum[i]!=0:
                 ind_contri = normalized_ind_scores[i][k] / ind_sum[i]
                 ind_contri_arr.append(ind_contri*100)
            indicator_contri_to_dimension.append(ind_contri_arr)
        
        return indicator_contri_to_dimension
    
    def get_dimension_contribution_tdi(self):
        dimension_arr = self.get_dimension_scores()
        total = sum(dimension_arr)
        ans = [round((dimension_arr[0]/total)*100), round((dimension_arr[1]/total)*100), round((dimension_arr[2]/total)*100)]
        return ans
    

    def get_score(self):
        dimension_scores = self.get_dimension_scores()
        normalized_final_ind_scores=self.get_normalized_final_ind_scores()
        arr=[normalized_final_ind_scores[0],normalized_final_ind_scores[1],normalized_final_ind_scores[2],normalized_final_ind_scores[3],normalized_final_ind_scores[4],normalized_final_ind_scores[5],normalized_final_ind_scores[6],normalized_final_ind_scores[7],normalized_final_ind_scores[8],normalized_final_ind_scores[9],normalized_final_ind_scores[10],dimension_scores[0],normalized_final_ind_scores[11],normalized_final_ind_scores[12],normalized_final_ind_scores[13],dimension_scores[1],normalized_final_ind_scores[14],normalized_final_ind_scores[15],normalized_final_ind_scores[16],normalized_final_ind_scores[17],dimension_scores[2]]
        return arr