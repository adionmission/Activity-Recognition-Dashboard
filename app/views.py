from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin
from camera1 import VideoCamera

@xframe_options_sameorigin
def index(request):

    vd = VideoCamera()
    vd.get_frame()

    context = {
        "text": vd.text
    }

    return render(request, "index.html", context)
