from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.decorators.csrf import csrf_exempt

from tensorflow import keras
import cv2
import os
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.metrics import classification_report

from django.conf import settings
import json


class MainView(TemplateView):
    template_name = 'neuralNetwork/index.html'


@csrf_exempt
def image_analysis_view(request):
    result = ' '
    if request.method == 'POST':
        # neural network
        img_size = 150
        model = load_model(os.path.join(settings.BASE_DIR, "neuralNetwork/static/neuralNetwork/pneumoniaa.h5"))
        labels = ['PNEUMONIA', 'NORMAL']
        data = []
        my_image = request.FILES.get('file').read()
        # if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        #     print("Yes, AJAX!")
        # else:
        #     print("No")
        # print(request.FILES.get('file').read())
        # data = json.loads(request.body.decode('utf-8'))
        # print(data)
        # my_image = request.POST['files']
        npimg = np.fromstring(my_image, np.uint8)
        img_arr = cv2.imdecode(npimg, cv2.IMREAD_GRAYSCALE)
        # img_arr = cv2.imdecode(np.fromstring(str(my_image.read()), np.uint8), cv2.IMREAD_UNCHANGED)
        # img_arr = cv2.imread(str(my_image), cv2.IMREAD_GRAYSCALE)
        resized_arr = cv2.resize(img_arr, (img_size, img_size))
        x_test = []
        x_test = np.array(resized_arr, dtype=np.float)
        x_test = np.array(x_test) / 255
        x_test = x_test.reshape(-1, img_size, img_size, 1)
        predictions = model.predict(x_test)
        predictions = np.where(predictions > 0.5, 1, 0)
        predictions = predictions.reshape(1, -1)[0]
        print(predictions)
        # #print(classification_report(y_test, predictions, target_names=['Pneumonia (Class 0)', 'Normal (Class 1)']))
        # return render(request, 'neuralNetwork/res.html', {'string': predictions[0]})
        print(JsonResponse({'string': int(predictions[0])}))
        if predictions[0] == 0:
            result = 'Pneumonia detected'
        if predictions[0] == 1:
            result = 'Pneumonia is not detected'
        return HttpResponse(JsonResponse({'result': result}), content_type='application/json')
    return render(request, 'neuralNetwork/res.html', {'string': 0})
    # return JsonResponse({'post':'correct'})
