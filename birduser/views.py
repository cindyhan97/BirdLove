

from concurrent.futures import process
from urllib import request
from django.shortcuts import render
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, logout, login as birduser_login
from django.contrib.auth.decorators import login_required
from .models import *
from django.forms import modelformset_factory
from django.db.models import Q
from itertools import chain

def index(request):
    return render(request, 'birduser/index.html')

def gallery(request):
    adoptionRequest = petAdoption.objects.filter(progress = adoptionProgressionChoices.looking_for_adopter)
    birdslst = []
    for item in adoptionRequest:
        birdslst.append(bird.objects.get(id = item.birds.id))
    picts = birdPicture.objects.all()
    pictlst = []
    for obj in birdslst:
        for pict in picts:
            if pict.bird == obj:
                pictlst.append(pict)
                break
    context = {
        'birds': birdslst,
        'picts': pictlst
    }
    return render(request, 'birduser/gallery.html', context)

def registration(request):
    registered = False
    if request.method == 'POST':
        regForm = userRegis(request.POST)
        if regForm.is_valid():
            registed_user = regForm.save()
            registed_user.set_password(registed_user.password)
            registed_user.save()
            registered = True
            birduser_login(request, registed_user)
            return render(request, 'birduser/index.html')
        else:
            return render(request, 'birduser/registration.html', {'regForm': regForm, 'registered:':registered})
    else:
        regForm = userRegis()
        return render(request, 'birduser/registration.html', {'regForm': regForm, 'registered:':registered})
def simplemap(request):
    return render(request, 'birduser/simpleMap.html')
def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('../profile')
    if request.method == 'POST':
        userloginform= userAuthenticationForm(request, data = request.POST)
        if userloginform.is_valid():
            birduser_login(request, userloginform.get_user())
            return HttpResponseRedirect('../profile')
        else:
            return render(request, 'birduser/login.html',{'userloginForm': userloginform})
    else:
        userloginform = userAuthenticationForm()
        context={
            'userloginForm': userloginform
        }
        return render(request, 'birduser/login.html', context)

def helpBird(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            requestUser = request.user
            rescueform = rescueRequestForm(request.POST)
            addressform = addressForm(request.POST)
            if  rescueform.is_valid() and addressform.is_valid():
                addressInstance = addressform.save()
                requestSent = rescueRequest.objects.create(rescueRequester = requestUser,address = addressInstance,resuceDescription = rescueform.cleaned_data['resuceDescription'])
                requestSent.save()
                for i in range(0, 6):
                    if request.FILES.get('upload-'+str(i), False):
                        pictFile = request.FILES['upload-'+str(i)]
                        rescueBirdPicture.objects.create(rescue_pk = requestSent,pict = pictFile)
                return HttpResponseRedirect('../submitsuccess')
            else: 
                return render(request, 'birduser/helpForm.html', {'rescueform': rescueform, 'addressform': addressform})
        else:
            anoInfo = anoUserInfoForm(request.POST)
            rescueform = anonymousRequestForm(request.POST)
            addressform = addressForm(request.POST)
            if anoInfo.is_valid() and rescueform.is_valid() and addressform.is_valid():
                addressInstance = addressform.save()
                anoInstance = anoInfo.save()
                anoInstance.address = addressInstance
                anoInstance.save()
                anonyrequestSent = anonymousRequest.objects.create(rescueRequester= anoInstance,resuceDescription = rescueform.cleaned_data['resuceDescription'])
                anonyrequestSent.save()
                for i in range(0, 6):
                    if request.FILES.get('upload-'+str(i), False):
                        pictFile = request.FILES['upload-'+str(i)]
                        rescueBirdPicture.objects.create(anonymousRequest = anonyrequestSent,pict = pictFile)
                return HttpResponseRedirect('../submitsuccess')
            else: 
                return render(request, 'birduser/helpForm.html', {'anoInfo': anoInfo, 'rescueform': rescueform, 'addressform': addressform})
    else:
        anoInfo = anoUserInfoForm()
        rescueform = rescueRequestForm()
        addressform = addressForm()
        return render(request, 'birduser/helpForm.html', {'anoInfo': anoInfo, 'rescueform': rescueform, 'addressform': addressform })
def success(request):
    return render(request, 'birduser/submitjump.html')
def donate(request):
    return render(request, 'birduser/membership.html')
def loginRequire(request):
    return render(request, 'birduser/loginRequire.html')

@login_required
def donateform(request, level):
    if request.user.is_authenticated:
        min = 0
        max = 0
        if level == 1:
            min = 1
            max = 20
        elif level == 2:
            min = 21
            max = 100
        elif level == 3:
            min = 101
            max = 500
        context = {
            'min': min,
            'max': max,
            'level': level
        }
        if request.method == 'POST':
            userdonation = request.POST['amount']
            print(userdonation)
            userDonationRecord.objects.create(user =request.user,  amount = userdonation)
            return HttpResponseRedirect('../submitsuccess')
        else:
            return render(request, 'birduser/donate.html',context)
    else:
        return HttpResponseRedirect('../notlogin')
def passwordUpdate(request):
    updateuser = request.user
    if request.method == 'POST':
        password_updateForm =  userPasswordChanging(user = updateuser, data = request.POST)
        context = {
            'password_update': password_updateForm,
        }    
        return render(request, 'birduser/userProfile.html',context)
    else:
        password_updateForm = userPasswordChanging(user = updateuser)  
        context = {
            'password_update': password_updateForm,
        }
    return render(request, 'birduser/userProfile.html',context)

def myprofile(request):
    updateuser = request.user
    birdList = bird.objects.filter(applyer = updateuser)
    adoptionHistory = petAdoption.objects.filter(Q(adopter = updateuser) | Q(requester = updateuser))
    birdApplying = []
    adoptionHistoryWithapplying = petAdoption.objects.none()
    for item in birdList:
        birdApplying.append(petAdoption.objects.get(birds = item))
    adoptionHistoryWithapplying = list(chain(birdApplying, adoptionHistory))
    requestHistory = rescueRequest.objects.filter(rescueRequester = updateuser)
    donationHistory = userDonationRecord.objects.filter(user= updateuser)
    if request.method == 'POST':
        userProfile_data = userprofile.objects.get(user = updateuser)
        nameform = userRealNameForm(request.POST, instance = request.user)
        addressInstance_updating = address.objects.get(id = userProfile_data.address.id)
        addressform = addressForm(request.POST, instance = addressInstance_updating)
        profile_updating = userprofileForm(data=request.POST, files=request.FILES, instance = userProfile_data)
        context = {
                'user_profile': profile_updating,
                'addressform':addressform,
                'nameform': nameform,
                'adoptionHistory':adoptionHistoryWithapplying,
                'requestHistory':requestHistory,
                'donationHistory':donationHistory
            }
        if profile_updating.is_valid() and nameform.is_valid() and addressform.is_valid():
            nameform.save()
            profile_updating.save()
            addressform.save()
            return HttpResponseRedirect("../profile")
        else:
            return render(request, 'birduser/userProfile.html',context)
    else:
        userProfile_toupdate, _ = userprofile.objects.get_or_create(user = updateuser)
        nameform = userRealNameForm(instance = request.user)
        profileform = userprofileForm(instance = userProfile_toupdate)
        if userProfile_toupdate.address == None:
            userAddress = address.objects.create()
            userAddress.save()
            userProfile_toupdate.address = userAddress
            userProfile_toupdate.save()
            addressform = addressForm(instance = userAddress)
            print("address = none")
        else: 
            userAddress= address.objects.get(id = userProfile_toupdate.address.id)
            addressform = addressForm(instance = userAddress)
            print("address!=none")
        if userProfile_toupdate.avatar :
            userAvatar_url = userProfile_toupdate.avatar.url
            context = {
                'user_profile': profileform,
                'userAvatar_url': userAvatar_url,
                'addressform': addressform,
                'nameform': nameform,
                'adoptionHistory':adoptionHistoryWithapplying,
                'requestHistory':requestHistory,
                'donationHistory':donationHistory
            }
        else:
            context = {
                'user_profile': profileform,
                'addressform':addressform,
                'nameform': nameform,
                'adoptionHistory':adoptionHistoryWithapplying,
                'requestHistory':requestHistory,
                'donationHistory':donationHistory
            }
        return render(request, 'birduser/userProfile.html',context)

def adopt(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            requester = request.user
            birdinput =  birdForm(request.POST)
            birdinput.save()
            if birdinput.is_valid():
                birdInstance = birdinput.save()
                petAdoption.objects.create(requester = requester, birds = birdInstance)
                for i in range(0, 6):
                    if request.FILES.get('upload-'+str(i), False):
                        pictFile = request.FILES['upload-'+str(i)]
                        birdPicture.objects.create(pict= pictFile, bird = birdInstance)
                return HttpResponseRedirect('../submitsuccess')
            else:
                return render(request, 'birduser/adoptForm.html', {'birdAdoptForm': birdinput })
        else:
            birdAdoptForm = birdForm()
        return render(request, 'birduser/adoptForm.html', {'birdAdoptForm': birdAdoptForm})
    else:
        return HttpResponseRedirect('../notlogin')

def adoptapply(request, birdid):
    if request.user.is_authenticated:
        birdInstance = bird.objects.get(id = birdid)
        pictlst = birdPicture.objects.filter(bird = birdInstance.id)
        if request.method == 'POST':
            birdInstance.applyer.add(request.user)
            context = {
                "bird" : birdInstance,
                'pictlst' : pictlst
            }
            return render(request, 'birduser/adoptionApplyForm.html', context)
        else:
            print(birdInstance.applyer)
            context = {
                "bird" : birdInstance,
                'pictlst' : pictlst
            }
            return render(request, 'birduser/adoptionApplyForm.html', context)
    else:
        return HttpResponseRedirect('../notlogin')


def userlogout(request):
    logout(request)
    return HttpResponseRedirect('..')
def jumpIndex(request):
    return render(request, 'birduser/jumpIndex.html')



    

