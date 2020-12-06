# views.py
from django.shortcuts import render, redirect
from .forms import UserForm, ProfileForm
import requests
from requests.structures import CaseInsensitiveDict
from django.contrib import messages


def register(request):

    # "aV4cM5PIhRFvnfP4tiN1Cx2TAa8s1sf0"
    #uickU1nHiAR1KFq8pYndm3SPLhNSZUAj
    if request.method == "POST":

        u_form = UserForm(request.POST)
        p_form = ProfileForm(request.POST)

        api_key = p_form.data['api_key']
        # print(p_form.data['api_key'])

        url = "https://airapi.airly.eu/v2/meta/indexes"
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["apikey"] = api_key
        resp = requests.get(url, headers=headers)

        print(resp.status_code)
        if resp.status_code is 200:

            if u_form.is_valid() and p_form.is_valid():
                user = u_form.save()
                p_form = p_form.save(commit=False)
                p_form.user = user
                p_form.save()  # commiting our data to database
                print("Form is valid")
                # messages.info(request, 'Registration complete! You may log in!')
                return redirect("/pollution")
        else:
            print('Wrong API key, API status code response: ', resp.status_code)
            messages.info(
                request, 'Wrong API key, API status code response: ')
    else:
        u_form = UserForm(request.POST)
        p_form = ProfileForm(request.POST)

        # context = {'u_form': u_form, 'p_form': p_form}
    return render(request, "register/register.html", {'u_form': u_form, 'p_form': p_form})
