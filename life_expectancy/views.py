from django.shortcuts import render
import datetime
import requests
import math

# Create your views here.
def home(request):
    response = requests.get("https://datacommons.org/api/ranking/LifeExpectancy_Person/Country/asia?h=country%2FIND").json()
    placeName = []
    for i in response['LifeExpectancy_Person']['rankAll']['info']:
        placeName.append(i['placeName'])
    placeName.sort()
    if request.method == "POST":
        life_expectancy = 70
        dob = str(request.POST['dob'])
        print(str(request.POST['dob']))
        place = str(request.POST['country'])
        print(str(request.POST['country']))
        try:
            if dob != 'None':
                if datetime.datetime.strptime(dob, "%m/%d/%Y") < datetime.datetime.today():
                    if datetime.datetime.strptime(dob, "%m/%d/%Y"):
                        for i in response['LifeExpectancy_Person']['rankAll']['info']:
                            if i['placeName'].lower() == place.lower():
                                life_expectancy = math.ceil(i['value'])

                        birthday = datetime.datetime.strptime(dob, "%m/%d/%Y")
                        today = datetime.datetime.today()
                        completed = today - birthday
                        remaining = birthday.replace(birthday.year+life_expectancy) - today

                        completed_percentage = round(completed*100/(completed + remaining),2)


                        sleep = remaining*7/24
                        sleep_percantage = round(sleep*100/(completed + remaining),2)

                        work = remaining/3
                        work_percentage = round(work*100/(completed + remaining),2)

                        phone_usage = remaining/12
                        phone_usage_percentage = round(phone_usage*100/(completed + remaining),2)

                        freshup = remaining/8
                        freshup_percentage = round(freshup*100/(completed + remaining),2)

                        travel = remaining/24
                        travel_percentage = round(travel*100/(completed + remaining),2)

                        spend_with_people = remaining/24
                        spend_with_people_percentage = round(spend_with_people*100/(completed + remaining),2)

                        consolidated_spends_percentage = round(completed_percentage + sleep_percantage + work_percentage + phone_usage_percentage + freshup_percentage + travel_percentage + spend_with_people_percentage,2)

                        remaining_life_percentange = round(100 - consolidated_spends_percentage,2)

                        years = today.year - birthday.year
                        months = today.month - birthday.month
                        if months < 1:
                            years -= 1
                            months = 12 + months
                        context = {
                        'dob' : dob,
                        'years' : years,
                        'months' : months,
                        'placeName' : placeName,
                        'place' : place,
                        'life_expectancy' : life_expectancy,
                        'completed_percentage' : completed_percentage,
                        'sleep_percantage' : sleep_percantage,
                        'work_percentage' : work_percentage,
                        'phone_usage_percentage' : phone_usage_percentage,
                        'freshup_percentage' : freshup_percentage,
                        'travel_percentage' : travel_percentage,
                        'spend_with_people_percentage' : spend_with_people_percentage,
                        'consolidated_spends_percentage' : consolidated_spends_percentage,
                        'remaining_life_percentange' : remaining_life_percentange

                        }
                else:
                    context = {
                                'placeName' : placeName,
                                'message' : "Provided Date is in future, please enter past date.",
                            }

        except:
            context = {
                        'placeName' : placeName,
                        'message' : "Please enter the Date in required format(mm/dd/yyyy)",
                    }
    else:
        context = {
                    'placeName' : placeName,
                }

    return render(request, 'home.html', context)
