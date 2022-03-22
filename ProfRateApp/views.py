from urllib import response
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login as auth_login, logout 
import json

from django.contrib.auth.models import User

from rest_framework.views import APIView
from . models import *
from . serializers import *
from django.db import connection



class list(APIView):
    def get(self,request):
        list = []
        list.append("CODE |       NAME      |  YEAR  |  SEMESTER |    Taught by")
        list.append("--------------------------------------------------------------------")
        data = Modules.objects.all()
        for mod in data:
            outString = (mod.code+" | "+mod.name + " | "+ str(mod.taughtYear)+ " | "+ str(mod.semester)+ " | ")
            for prof in mod.taughtBy.all():
                outString+=(prof.name+" | "+prof.code+" | ")
            list.append(outString)
            list.append("--------------------------------------------------------------------")
                   
        return Response(list)

class view(APIView):
    def get(self,request):
        staff = Professors.objects.raw("SELECT * FROM ProfRateApp_Professors")
        teacher_id = 0
        stars = ""
        return_list = []

        for prof in staff:
            teacher_id = prof.id
            data = Ratings.objects.raw("SELECT * FROM ProfRateApp_Ratings WHERE Professor_id = %s",[teacher_id])
            rating_tot = 0
            num_ratings = 0
            for a_rating in data:
                rating_tot = rating_tot + int(a_rating.rating)
                num_ratings = num_ratings+1
            
            if num_ratings > 0:
                average_rating = rating_tot/num_ratings
                if average_rating>=4.5:
                    average_rating = 5
                elif 3.5<=average_rating < 4.5:
                    average_rating = 4
                elif 2.5<=average_rating<3.5:
                    average_rating = 3
                elif 1.5<=average_rating<2.5:
                    average_rating = 2
                elif 0.5<=average_rating<1.5:
                    average_rating = 1
                else:
                    average_rating=0
            else:
                average_rating = 0
            
            if average_rating == 0:
                stars = "Unrated"
            elif average_rating == 1:
                stars = "*"
            elif average_rating == 2:
                stars = "**"
            elif average_rating == 3:
                stars = "***"
            elif average_rating == 4:
                stars = "****"
            elif average_rating == 5:
                stars = "*****"

            final_string = ("The rating of "+prof.name+" ("+prof.code+")"+" is " + stars)
            print(final_string)
            return_list.append(final_string)
          
        return Response(return_list) # return response 

class average(APIView):
    def post(self,request):
        test_professor_code = request.POST.get('prof')
        test_module_code = request.POST.get('mod')

        teacher_id = 0
        module_id = 0
        
        stars = ""

        module_codes = Modules.objects.raw("SELECT * FROM ProfRateApp_Modules WHERE code = %s",[test_module_code])
        staff = Professors.objects.raw("SELECT * FROM ProfRateApp_Professors WHERE code = %s",[test_professor_code])
        
        for member in staff:
            teacher_id = member.id
            teacher_name = member.name
        
        rating_tot = 0
        num_ratings = 0
        
        for mod in module_codes:
            module_name = mod.name
            
            module_id = mod.id

            
            staff_ratings = Ratings.objects.raw("SELECT * FROM ProfRateApp_Ratings WHERE Professor_id = %s AND Module_id = %s",[teacher_id, module_id])
            
            for a_rating in staff_ratings:
                rating_tot = rating_tot + int(a_rating.rating)
                num_ratings = num_ratings+1

        if num_ratings > 0:
                average_rating = rating_tot/num_ratings
                if average_rating>=4.5:
                    average_rating = 5
                elif 3.5<=average_rating < 4.5:
                    average_rating = 4
                elif 2.5<=average_rating<3.5:
                    average_rating = 3
                elif 1.5<=average_rating<2.5:
                    average_rating = 2
                elif 0.5<=average_rating<1.5:
                    average_rating = 1
                else:
                    average_rating=0
        else:
            average_rating = 0
        
        if average_rating == 0:
            stars = "Unrated"
        elif average_rating == 1:
            stars = "*"
        elif average_rating == 2:
            stars = "**"
        elif average_rating == 3:
            stars = "***"
        elif average_rating == 4:
            stars = "****"
        elif average_rating == 5:
            stars = "*****"

               
        final_string = ("The rating of "+teacher_name+" ("+test_professor_code+")"+" in "+module_name+ " is " + stars)
        print(final_string)
       
        return Response(json.dumps(final_string)) # return response 


class rate(APIView):
    def post(self,request): 
        
        test_professor_code = request.POST.get('prof') 
        test_module_code = request.POST.get('mod')
        test_year = request.POST.get('year')
        test_semester = request.POST.get('sem')
        test_rating = request.POST.get('rating')
        
        professor_id = Professors.objects.raw("SELECT id FROM ProfRateApp_Professors WHERE code = %s",[test_professor_code])
        module_id = Modules.objects.raw("SELECT id FROM ProfRateApp_Modules WHERE code = %s AND taughtYear = %s AND semester = %s",[test_module_code,test_year,test_semester])        

        print (professor_id)
        print(module_id)

        teacher_id1 = 0
        module_id1 = 0
        for prof in professor_id:
            teacher_id1 = prof.id
            print(f"teacher_id = {prof.id}")
        
        for mod in module_id:
            module_id1 = mod.id
            print((f"module_id = {mod.id}"))

        if request.user.is_authenticated:
            with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO ProfRateApp_Ratings(module_year, rating, Professor_id, module_id) VALUES (%s, %s, %s, %s)",[test_year,test_rating,teacher_id1,module_id1]#[test_year,test_rating,professor_id,module_id]#[2017,5,1,1] 
                        )

            return Response("complete")
        else:
            return Response("Please login to leave a rating")
        

class register(APIView):
    def post(self,request): 
      
        test_username = request.POST.get('username')
        test_email = request.POST.get('email')
        test_password = request.POST.get('password')

        user_check = User.objects.raw("SELECT * FROM auth_user WHERE username = %s OR email = %s",[test_username, test_email])
        for user in user_check:
            if user.id >= 1:
                return Response("Username or Email already exists!")

        user = User.objects.create_user(test_username,test_email, test_password)
        user.save()

        return Response("complete")
 

class login(APIView):
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password,backend='django.contrib.auth.backends.ModelBackend')
        if user is not None:
            auth_login(request, user)
            request.session.set_expiry(86400)
            response = {"Complete"}
            print(user.id)
        else: 
            response = {"Failed"}

        return Response(response)

class logout_user(APIView):
    def get(self,request):
        if request.user.is_authenticated:
            response = f"Logging you out..."
            logout(request)
            response += " ...logged out succesfully"
        else:
            response = "Error"
        return Response(response)
        