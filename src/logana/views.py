from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#from .forms import DocumentForm
from django.core.files.storage import FileSystemStorage
from .processes.scripts.bashRunner import runner







@login_required(login_url = '/login')
def rp_err(request):
        return render(request, 'logana/rcodes.html', {})
        
@login_required(login_url = '/login')
def project_dash(request):
        return render(request, 'logana/logadmin.html', {})    


@login_required(login_url = '/login')
def create(request):
        user = request.user
        if user.is_staff:
            return render(request, 'logana/create.html', {})  
        else:
            messages.info(request, 'You have been redirected because you don\'t have the credentials to view this page.')
            return redirect(project_dash)   


    

@login_required(login_url = '/login')
def upload(request):
        user = request.user
        if user.is_staff:
            if request.method == "POST" and request.FILES:
                 uploaded_file = request.FILES["files"]
                 print(uploaded_file)
                 fs = FileSystemStorage()
                 name = fs.save(uploaded_file.name, uploaded_file)
                 url = fs.url(name)
                 print(url) 
                 try:
                     runner(bashFile="logana/processes/scripts/moveInput.sh")
                 except:
                     print("Nothing to move")
                 try:      
                     runner(bashFile="logana/processes/scripts/runPreporcessing.sh")
                 except:
                     print("Preprocessing not performed!")                           
            return render(request, 'logana/upload.html', {})  
        else:    
            messages.info(request, 'You have been redirected because you don\'t have the credentials to view this page.')
            return redirect(create)
            

@login_required(login_url = '/login')
def processing_details(request):
        user = request.user
        if user.is_staff:
            return render(request, 'logana/processing-details.html', {})  
        else:    
            messages.info(request, 'You have been redirected because you don\'t have the credentials to view this page.')
            return redirect(project_dash)
         


@login_required(login_url = '/login')
def erp_details(request):
        return render(request, 'logana/rcodes.html', {})           

@login_required(login_url = '/login')
def googlebot_details(request):
        return render(request, 'logana/google.html', {})





