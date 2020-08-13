from django.shortcuts import render,redirect
from loanform.customerform import CustomerForm
import pandas as pnd
import joblib
from django.contrib import messages

# Create your views here.

def customer_form(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        #as the form data is useless in this way as the data is in the form of Querydict
        #need to convert it into Dict type
        form_data = (request.POST).dict()
        #as this data is going to be used for checking the loan status
        #must be changed into a dataframe

        df = pnd.DataFrame(form_data, index=[0])
        #need to one hot encode the data frame and
        #then pass to classifier
        #passing it to one hot encoder and classifier
        result = loanstatuspredictor(ohedataframe(df))
        if(int(df['LoanAmount']) > 40000):
            messages.success(request, 'Sorry we cannot process the loan more than $40000 ')
        else:
            messages.success(request,'Your application is {}' .format(result))
    form = CustomerForm()
    return render(request,'loanform/customer_form.html', {'form' : form})

def ohedataframe(df):
    ohecolumns =  joblib.load('ML_models/ohecolumns.pkl')
    df_dummies = pnd.get_dummies(df,columns=['Gender','Married','Education','Self_Employed','Property_Area'])
    print(ohecolumns)
    print(df_dummies.columns)

    #make a dictionary to fill the data and make a final dataframe to pass it to ml model
    final_dict = {}

    for i in ohecolumns:
        if i in df_dummies.columns:
            final_dict[i] = df_dummies[i].values
        else:
            final_dict[i] = 0

    final_df = pnd.DataFrame(final_dict)

    return final_df

def loanstatuspredictor(final_df):
    scalar = joblib.load('Ml_models/scalar.pkl')
    classifier = joblib.load('Ml_models/model.pkl')

    #scaling the data
    final_input =  scalar.transform(final_df)
    y_pred = classifier.predict(final_input)

    if (y_pred > 0.5):
        return 'Approved'
    else:
        return 'Rejected'








