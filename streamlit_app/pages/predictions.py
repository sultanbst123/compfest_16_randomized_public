import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import joblib
import gspread
import pytz

st.cache_data.clear()


# layout config
st.set_page_config(page_title="Burnout Report", 
                   layout="wide", 
                   page_icon="📊")

# to using this you can uncomment this block code and change you key sheet and ghseet api 
# def get_data_to_gsheet(sheetname, data):
#     """
#     Insert a data
#     """
#     gc = gspread.service_account(filename="streamlit_app/key/my_key.json")
#     sh = gc.open_by_key("gsheet_key") # MP real

#     # # select sheet 
#     worksheet_1 = sh.worksheet(f"Sheet1") 
#     # worksheet_1.clear() # clear worksheet 

#     # worksheet_1.update([df.columns.values.tolist()] + df.fillna("").values.tolist()) # < this for update new format
#     worksheet_1.append_rows(data.values.tolist()) # append value when sumbit  


# helper function to get a recomendation
def get_burnout_recommendation(burnout_rate):
    """
    Provides a recommendation based on the burnout rate.
    """
    if burnout_rate < 0 or burnout_rate > 1:
        return "Invalid burnout rate. Please provide a value between 0.0 and 1.0."
    
    if 0.0 <= burnout_rate <= 0.2:
        return st.success("Low Burnout: The individual is likely well-balanced and managing stress effectively. "
                "Encourage continuation of current practices and occasional wellness check-ins.")
    
    elif 0.2 < burnout_rate <= 0.4:
        return st.info("Moderate Burnout: The individual may be experiencing mild stress or early signs of burnout. "
                "Recommend stress management techniques, regular breaks, mindfulness, and open communication.")
    
    elif 0.4 < burnout_rate <= 0.6:
        return st.warning("Approaching High Burnout: This suggests moderate burnout that may need attention. "
                "Implement robust stress management strategies, consider workload adjustments, and offer resources such as counseling.")
    
    elif 0.6 < burnout_rate <= 0.8:
        return st.warning("High Burnout: The individual is likely experiencing significant burnout. "
                "Immediate action is recommended, including workload reduction, providing time off, and offering mental health support.")
    
    elif 0.8 < burnout_rate <= 1.0:
        return st.error("Critical Burnout: This is a critical level of burnout that requires urgent intervention. "
                "Immediate steps should include medical evaluation, significant time off, and comprehensive mental health support.")

# disable when one click
def disable():
    st.session_state.disabled = True

if "disabled" not in st.session_state:
    st.session_state.disabled = False

# load weight model
pipeline = joblib.load('models/pipeline.pkl')
model = joblib.load('models/model_burnout.pkl')

# streamlit page

# this page for to make a data predictions
st.markdown("<h2 style='text-align: center;'>Are Your Employees Burning Out?</h2>", unsafe_allow_html=True)
st.caption('If the submit button is not active, you can press Ctrl+Shift+R.')
st.markdown('<br>', unsafe_allow_html=True)

# predictions form
with st.expander("Please complete the form here. 👈"):
    with st.form('form_1', border=False):

        # gender
        st.subheader('1. Gender*') # str
        gender = st.radio('Choose the Gender', ['Female', 'Male'], 
                            help = 'The gender of the employee.')
        st.markdown('<br>', unsafe_allow_html=True)

        # Company Type
        st.subheader('2. Company Type*') # str
        company_type = st.radio('Choose Company Type', ['Service', 'Product'], 
                                help = 'The type of company where the employee is working.')
        st.markdown('<br>', unsafe_allow_html=True)
        
        # WFH Setup Available
        st.subheader('3. WFH Setup Available*') # str
        is_wfh = st.radio('Choose WFH Setup Available', ['Yes', 'No'], 
                            help = 'Is the work from home facility available for the employee?')
        st.markdown('<br>', unsafe_allow_html=True)
        
        # Designation
        st.subheader('4. Designation*') # float
        designation = st.radio('Choose Designation', [i for i in range(6)], 
                                help = "The employee's job title within the organization, rated on a scale from 0 to 5, with higher numbers indicating a higher position.",
                                horizontal = True)
        st.markdown('<br>', unsafe_allow_html=True)
        
        # Resource Allocation
        st.subheader('5. Resource Allocation*') # float
        resource = st.radio('Choose the Resource Allocation', [i+1 for i in range(10)],
                            help = 'The number of work hours assigned to the employee, ranging from 1 to 10 (where a higher number means more hours)..',
                            horizontal = True)
        st.markdown('<br>', unsafe_allow_html=True)
        
        # Resource Allocation
        st.subheader('6. Mental Fatigue Score*') 
        mental = st.slider('Choose the Mental Fatigue Score', 
                            min_value=0.0, max_value=10.0, value=5.0, step=0.1,
                            help = 'The level of mental fatigue the employee is experiencing, rated on a scale from 0.0 to 10.0, where 0.0 indicates no fatigue and 10.0 indicates complete exhaustion.')
        st.markdown('<br>', unsafe_allow_html=True)
        

        # completion form button        
        b1 = st.form_submit_button('Submit Here 👈', on_click=disable, disabled=st.session_state.disabled)

# # result of completion form
if b1:
    # # Create input DataFrame
    input_data = {
        'Gender': [gender],
        'Company Type': [company_type],
        'WFH Setup Available': [is_wfh],
        'Designation': [designation],
        'Resource Allocation': [resource],
        'Mental Fatigue Score': [mental],
    }
    # st.dataframe(input_data) # testing
    # layer 
    col1_sb, col2_sb = st.columns([1, 4])

    # predictions
    with st.spinner(text="In progress..."):
        to_frame = pd.DataFrame(input_data)
        input_data = pipeline.transform(to_frame)
        predictions = model.predict(input_data)

        # to ghseet
        to_frame['Burn Rate'] = np.round(predictions[0],2)
        to_frame['Timestamp'] = '{:%Y-%m-%d %H:%M}'.format(datetime.now(tz = pytz.timezone('Asia/Jakarta')))
        get_data_to_gsheet('Sheet1', to_frame)
        with col1_sb:
            st.markdown(f"<h3 style='text-align: center;'>Burnout Rate : {predictions[0] * 100:.2f}%</h3>", unsafe_allow_html=True)
        with col2_sb:
            get_burnout_recommendation(predictions)
else:
    st.info('Please fill in the form to get better insight')





