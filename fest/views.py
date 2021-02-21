from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .form import CreateUserForm, DashboardForm, DashboardCrewForm
from .models import *
from django.contrib.auth.models import User

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.info(request, 'Username or password is incorrect')
    return render(request, 'login.html')




# def index(request):
#     print(request.user)
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect("dashboard-user")
#         else:
#             print('incorrect paswword')
#     return render(request, 'index.html')



def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # print(Users.objects.filter(id=request.user.id))
            # So you'd create a view function for dashboard - in it, you'd be able to get request.user.id
            return redirect("dashboard-user") # this can now take the user to their dashboard
        else:
            return render(request, 'index.html', context={ 'error': 'incorrect password'})
    return render(request, 'index.html')




def auth(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            users = Users(user=user, email=email)
            users.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'auth.html', context)


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            instance = Balance(user=user, balance=0)
            bonus = Bonus(user=user, five_ref=0, ten_ref=0)
            bonus.save()
            instance.save()
            messages.success(request, 'Success: Account created for ' + username + '\n was successful.')
            return redirect('login')
    context = {'form': form}
    return render(request, 'register.html', context)

def connectcrews(request):
    crew = Crew.objects.all()
    cw = Crew.objects.all().count()
    user = Users.objects.all()

    group = Crew.objects.get(id=request.user.id)
    return render(request, 'connect-crews.html', {'crew': crew, 'cw': cw,})


def connectusers(request):
    users = Users.objects.all()
    return render(request, 'connect-users.html', {'users': users,})



def dashboardcrew(request):
    userid = request.user.id
    user = get_object_or_404(Users, id=userid)
    #user = Users.objects.get(id=userid)
    if request.method == "POST":
        form = DashboardCrewForm(user, request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('name')
            #hall.landlord = request.user
            user.save()
            return redirect('dashboard-user')
    else:
        form = DashboardCrewForm(instance=user)
    
    user = User.objects.get(username=request.user)
    context = {'form': form, 'user':user.netnet, }

    return render(request, 'dashboard-crew.html', context)

@login_required
def dashboarduser(request):
    userid = request.user.id
    user = get_object_or_404(Users, id=userid)
    #user = Users.objects.get(id=userid)
    if request.method == "POST":
        form = DashboardForm(user, request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            #hall.landlord = request.user
            user.save()
            return redirect('dashboard-user')
    else:
        form = DashboardCrewForm(instance=user)
    context = {'form': form}
    return render(request, 'dashboard-user.html', context)



@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)  # request.FILES is show the selected image or file

        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('fest:view_profile')
    else:
        form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)
        args = {}
        # args.update(csrf(request))
        args['form'] = form
        args['profile_form'] = profile_form
        return render(request, 'dashboard-user.html', args)



