from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User,BillingInfo
from .forms import SignUpForm, SignInForm, UserUpdateForm, BillingInfoForm
from django.contrib.auth.decorators import login_required





def signIn(request):
    if request.method == 'POST':
        signInForm = SignInForm(request.POST)
        if signInForm.is_valid():
            email = signInForm.cleaned_data['email']
            password = signInForm.cleaned_data['password']

            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('videos:home')
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            for field, errors in signInForm.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:
        signInForm = SignInForm()

    return render(request, 'accounts/login.html', {'signInForm': signInForm})


def signOut(request):
    logout(request)
    return redirect('userauth:signin')  



def signUp(request):
    if request.method == 'POST':        
        signUpForm = SignUpForm(request.POST)
        if signUpForm.is_valid():
            user = signUpForm.save()
            
            # Log in the user after registration
            user = authenticate(username=user.email, password=request.POST['password1'])
            if user is not None:
                login(request, user)
                #messages.success(request, 'Registration successful. Welcome!')
                return redirect('videos:home')
        else:
            for field, errors in signUpForm.errors.items():
                for error in errors:
                    #messages.error(request, 'Invalid email or password.')
                    messages.error(request, f'{field.capitalize()}: {error}')

    else:
        signUpForm = SignUpForm()

    return render(request, 'accounts/register.html', {'signUpForm': signUpForm})







@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('userauth:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserUpdateForm(instance=request.user)

    context = {
        'user_form': user_form
    }
    return render(request, 'accounts/profile.html', context)





@login_required
def update_billing_info(request):
    billing_info, created = BillingInfo.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = BillingInfoForm(request.POST, instance=billing_info)
        if form.is_valid():
            form.save()
            #return redirect('billing_success')  # Change this to the URL name you want to redirect to after success
            messages.success(request, 'Billing information updated successfully.')
    else:
        form = BillingInfoForm(instance=billing_info)
    return render(request, 'accounts/billing.html', {'form': form})

