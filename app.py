import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load the model and scaler
@st.cache_resource
def load_model():
    model = joblib.load('ecoli.model')
    scaler = joblib.load('scaler.pkl')
    return model, scaler

def main():
    st.title('E. coli Protein Localization Predictor')
    st.write("""
    This app predicts the localization site of E. coli proteins based on various cellular characteristics.
    """)
    
    # Create input form
    st.subheader('Enter Protein Characteristics:')
    
    col1, col2 = st.columns(2)
    
    with col1:
        mcg = st.number_input('MCG (McGeoch Signal Sequence)', min_value=0.0, max_value=1.0, value=0.5)
        gvh = st.number_input('GVH (von Heijne Signal Sequence)', min_value=0.0, max_value=1.0, value=0.5)
        lip = st.number_input('LIP (von Heijne Signal Peptidase II)', min_value=0.0, max_value=1.0, value=0.48)
        chg = st.number_input('CHG (Presence of Charge)', min_value=0.0, max_value=1.0, value=0.5)
        
    with col2:
        aac = st.number_input('AAC (Score of discriminant analysis)', min_value=0.0, max_value=1.0, value=0.5)
        alm1 = st.number_input('ALM1 (Score of ALOM program)', min_value=0.0, max_value=1.0, value=0.5)
        alm2 = st.number_input('ALM2 (Score of ALOM after excluding putative cleavable signal regions)', min_value=0.0, max_value=1.0, value=0.5)

    # Create a prediction button
    if st.button('Predict Localization'):
        try:
            # Load model and scaler
            model, scaler = load_model()
            
            # Prepare input data
            input_data = np.array([[mcg, gvh, lip, chg, aac, alm1, alm2]])
            input_scaled = scaler.transform(input_data)
            
            # Make prediction
            prediction = model.predict(input_scaled)
            probability = model.predict_proba(input_scaled)
            
            # Display results
            st.subheader('Prediction Results:')
            st.write(f'Predicted Localization Site: **{prediction[0]}**')
            
            # Create probability dataframe
            prob_df = pd.DataFrame(
                probability,
                columns=model.classes_
            )
            
            # Find the highest probability
            max_prob = prob_df.iloc[0].max()
            max_class = prob_df.iloc[0].idxmax()
            
            # Create a styled dataframe with highlighted maximum probability
            def highlight_max(s):
                is_max = s == max_prob
                return ['background-color: #90EE90' if v else '' for v in is_max]
            
            styled_df = prob_df.style.apply(highlight_max)
            
            # Display probabilities with location descriptions
            st.write('Prediction Probabilities:')
            st.dataframe(styled_df)
            
            # Display class descriptions
            st.subheader('Location Descriptions:')
            locations = {
                'cp': 'Sitoplasma',
                'im': 'Membran dalam tanpa urutan sinyal',
                'imS': 'Membran dalam dengan urutan sinyal',
                'imU': 'Membran dalam, urutan sinyal tidak dapat dipotong',
                'om': 'Membran luar',
                'omL': 'Lipoprotein membran luar',
                'pp': 'Periplasma'
            }
            
            # Highlight the predicted class
            for loc, desc in locations.items():
                if loc == prediction[0]:
                    st.markdown(f"**{loc}**: {desc} 🎯")
                else:
                    st.write(f"{loc}: {desc}")
            
        except Exception as e:
            st.error(f'An error occurred: {str(e)}')
            st.error('Please make sure the model files (ecoli.model and scaler.pkl) exist and are valid.')

if __name__ == '__main__':
    main()
