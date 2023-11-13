from django.shortcuts import render, redirect
from .models import UploadImg
from django.contrib import messages
from keras.preprocessing import image
import numpy as np
from tensorflow.keras.applications import InceptionResNetV2
import tensorflow as tf
import threading

def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def manage(request):
    return render(request, 'manage.html', {})

def about(request):
    return render(request, 'about.html', {})

def dashboard(request):
    image_tbl = UploadImg.objects.all()
    return render(request, 'dashboard.html', {'image_tbl': image_tbl})

def upload_images(request):
    if request.method == "POST":
        patient_id = request.POST['pid']
        patient_name = request.POST['pname']
        patient_age = request.POST['page']
        brainpics = request.FILES['brainpics']
        img = UploadImg(pid=patient_id, patient_name=patient_name, page=patient_age,
                        brainpics=brainpics)
        img.save()
        print("Newly saved item id:", img.id)
        messages.success(request, "Detail has been uploaded to Database.Please go to report section.")

        ## Start New Thread
        t = threading.Thread(target=run_prediction, args=(img.id,))
        t.setDaemon(True)
        t.start()
        return render(request, 'manage.html')
    else:
        return render(request, 'manage.html')

def update_model_data(request):
    if request.method == "POST":
        reg_id = request.POST['rid']
        brainpics = request.FILES['brainpics']
        img = UploadImg.objects.get(pk=reg_id)
        img.brainpics = brainpics
        img.save()
        messages.success(request, "Detail has been updated to Database.Please go to report section.")

        ## Start New Thread
        t = threading.Thread(target=run_prediction, args=(img.id,))
        t.setDaemon(True)
        t.start()
        return render(request, 'manage.html')
    else:
        return render(request, 'manage.html')

def rerun_prediction(request, patient_id):
    # Rerun prediction
    t = threading.Thread(target=run_prediction, args=(patient_id,))
    t.setDaemon(True)
    t.start()
    messages.success(request, "Re-running the model on the data. Please go to report section")
    return redirect('dashboard')

def delete_pics(request, patient_id):
    item = UploadImg.objects.filter(pk=patient_id)
    item.delete()
    messages.success(request, "Deleted Successfully!!!")
    return redirect('dashboard')

def update_pics(request, patient_id):
    item = UploadImg.objects.filter(pk=patient_id)
    return render(request, 'update.html', {'items': item})

def create_model(input_shape, n_out):
    InceptionResNet = InceptionResNetV2(weights='imagenet', include_top=False, input_shape=input_shape)
    model = InceptionResNet.output
    model = tf.keras.layers.GlobalAveragePooling2D()(model)
    model = tf.keras.layers.Dropout(rate=0.5)(model)
    model = tf.keras.layers.Dense(n_out, activation='softmax')(model)
    model = tf.keras.models.Model(inputs=InceptionResNet.input, outputs=model)
    model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])

    return model

def run_prediction(record_id):
    item = UploadImg.objects.filter(pk=record_id)
    brain_files = item[0].brainpics
    brain_pred = {0: 'Glioma Tumor', 1: 'Normal', 2: 'Meningioma Tumor', 3: 'Pituitary Tumor'}

    # Load Model
    SIZE = 150
    NUM_CLASSES = 4
    model = create_model(
        input_shape=(SIZE, SIZE, 3),
        n_out=NUM_CLASSES)

    # Load Model
    model.load_weights('models/InceptionResNet.h5')
    print("model_loaded")

    img = image.load_img(brain_files, target_size=(SIZE, SIZE))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    prediction = model.predict(img)

    print('Brain Tumor Prediction: ', prediction)
    brain_score_predict = brain_pred[np.argmax(prediction)]
    brain_score = np.max(prediction)
    print('Prediction: ', brain_score_predict, brain_score)

    get_patient_rec = UploadImg.objects.get(pk=record_id)
    get_patient_rec.brain_prediction = brain_score_predict
    get_patient_rec.brain_score = round(brain_score * 100, 2)
    get_patient_rec.save()

    # Clear backend for next prediction
    from keras import backend as K
    K.clear_session()
    return redirect('dashboard')

def run_report(request, patient_id):
    item = UploadImg.objects.filter(pk=patient_id)

    return render(request, 'report.html', {'items': item})