from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Prediction
import numpy as np
import joblib
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404,render


# Load the model
model = joblib.load('predictor/rf_model.pkl')


def predict_price(request):
    if request.method == 'POST':
        try:
            # Get and convert form values
            sqft_living = float(request.POST['sqft_living'])
            bedrooms = int(request.POST['bedrooms'])
            bathrooms = float(request.POST['bathrooms'])
            sqft_lot = float(request.POST['sqft_lot'])
            grade = int(request.POST['grade'])
            floors = int(request.POST['floors'])
            house_age = int(request.POST['house_age'])
            sqft_living15 = float(request.POST['sqft_living15'])
            lat = float(request.POST['lat'])
            long = float(request.POST['long'])

            # Feature array for prediction
            features = np.array([[sqft_living, bedrooms, grade, floors, sqft_lot,
                                  bathrooms, house_age, sqft_living15, lat, long]])

            # Predict and create price range
            predicted_price = model.predict(features)[0]
            lower_price = round(predicted_price * 0.95, 2)
            upper_price = round(predicted_price * 1.05, 2)

            # Save to database if user is authenticated
            if request.user.is_authenticated:
                Prediction.objects.create(
                    user=request.user,
                    sqft_living=sqft_living,
                    bedrooms=bedrooms,
                    bathrooms=bathrooms,
                    grade=grade,
                    floors=floors,
                    sqft_lot=sqft_lot,
                    house_age=house_age,
                    sqft_living15=sqft_living15,
                    lat=lat,
                    long=long,
                    predicted_price_min=lower_price,
                    predicted_price_max=upper_price,
                )

            # Pass prediction to result page
            return render(request, 'predictor/result.html', {
                'predicted_price_lower': lower_price,
                'predicted_price_upper': upper_price
            })

        except (ValueError, KeyError):
            return render(request, 'predictor/form.html', {
                'error': 'Invalid input. Please fill all fields correctly.'
            })

    # GET request
    return render(request, 'predictor/form.html')


@login_required
def my_predictions(request):
    predictions = Prediction.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'predictor/my_predictions.html', {'predictions': predictions})

# View for 'How the Model Works' page
def how_the_model_works(request):
    return render(request, 'predictor/model_works.html')

# View for 'Tips for Interpreting Predictions' page
def interpret_predictions(request):
    return render(request, 'predictor/pred_interpretation.html')

# View for 'FAQs' page
def faqs(request):
    return render(request, 'predictor/faqs.html')




def custom_logout(request):
    logout(request)
    return redirect('predict_price')

def prediction_detail(request, prediction_id):
    prediction = get_object_or_404(Prediction, id=prediction_id)
    return render(request, 'predictor/prediction_detail.html', {'prediction': prediction})



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after registration
            return redirect('predict_price')  # This is correct

    else:
        form = UserCreationForm()
    return render(request, 'predictor/register.html', {'form': form})
