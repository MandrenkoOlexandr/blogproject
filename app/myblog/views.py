from django.shortcuts import render

def index(request):
    # тимчасово без БД; далі додамо вибірку 3 останніх опублікованих статей
    return render(request, "myblog/index.html")
