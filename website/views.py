from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, AddRecordForm
from .models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()

    #check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.success(request, "Error logging in - please try again")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})

# def login_user(request):
#     pass

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            #authenticate and login user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f"Account created for {username}!")
            return redirect('home')
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    
    return render(request, 'register.html', {'form': form})
            

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'record': customer_record})
    else:
        messages.success(request, "Please log in to view the page")
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_record = Record.objects.get(id=pk)
        delete_record.delete()
        messages.success(request, "Record deleted successfully")
        return redirect('home')
    else:
        messages.success(request, "Please log in to view the page")
        return redirect('home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                record = form.save(commit=False)
                record.user = request.user
                record.save()
                messages.success(request, "Record added successfully")
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, "Please log in to view the page")
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)  
        form = AddRecordForm(request.POST or None, instance=current_record)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Record updated successfully")
                return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, "Please log in to view the page")
        return redirect('home')