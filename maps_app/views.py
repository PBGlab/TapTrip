from django.shortcuts import render

def show_map(request):
    return render(request, "maps_app/map.html")  # 回傳 map.html
