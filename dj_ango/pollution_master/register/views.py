# views.py
from django.shortcuts import render, redirect
from .forms import UserForm, ProfileForm


def register(request):
    if request.method == "POST":

        u_form = UserForm(request.POST)
        p_form = ProfileForm(request.POST)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save()
            p_form = p_form.save(commit=False)
            p_form.user = user
            p_form.save()  # commiting our data to database
            print("Form is valid")
            # messages.info(request, 'Registration complete! You may log in!')
            return redirect("/pollution")
    else:
        u_form = UserForm(request.POST)
        p_form = ProfileForm(request.POST)

        # context = {'u_form': u_form, 'p_form': p_form}
    return render(request, "register/register.html", {'u_form': u_form, 'p_form': p_form})
