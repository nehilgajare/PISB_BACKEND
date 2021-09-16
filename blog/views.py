from django.shortcuts import render
# from django.urls.conf import include

from django.http import HttpResponse


    
    
def about(request):
    if request.method == "POST" :

        data=int(request.POST["num"])
        if(data>0 and data<500):
            result= [i for i in range(data,0,-1)]
            return render(request, 'blog/about.html', {"result":result })
    
        else:
            return HttpResponse('<h1> Enter number between 0 and 500 !!</h1>' )
    else:
        return render(request, 'blog/home.html')

    
