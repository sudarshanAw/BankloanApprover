from django.shortcuts import render,redirect
from loanform.customerform import CustomerForm
import pandas as pnd
from django.contrib import messages
import pickle

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
        if(int(df['LoanAmount']) > 40000):
            messages.success(request, 'Sorry we cannot process the loan more than $40000 ')
        else:
            result = loanstatuspredictor(ohedataframe(df))
            messages.success(request,'Your application is {}' .format(result))
    form = CustomerForm()
    return render(request,'loanform/customer_form.html', {'form' : form})

def ohedataframe(df):
    ohecolumns =  pickle.load(open('ML_models/ohecolumns.pkl','rb'))
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
    print("################Inside Loan status predictor##################")
    try:
        print("################Inside Try##################")
        scalar = pickle.load(open('Ml_models/scalar.pkl','rb'))
        print("################Scalars Loaded##################")

        classifier = pickle.load(open('Ml_models/model.pkl','rb'))
        print("################Classifier Loaded Loaded##################")

        #scaling the data
        print("################Before Operation 1##################")

        final_input =  scalar.transform(final_df)
        print("################After Operation 1##################")

        y_pred = classifier.predict(final_input)
        print("################After Operation 2##################")


        if (y_pred > 0.5):
            print("Approved")
            return 'Approved'
        else:
            print("Rejected")
            return 'Rejected'

    except ValueError as e:
        print("################Inside Except##################")
        print(e.args[0])
        return (e.args[0])








