import streamlit as st
def display_dosha_results(results):
    st.success("Analysis Complete!")
    
    # Create three columns for the doshas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Vata", f"{results.get('vata_percentage', 0):.1f}%")
    with col2:
        st.metric("Pitta", f"{results.get('pitta_percentage', 0):.1f}%")
    with col3:
        st.metric("Kapha", f"{results.get('kapha_percentage', 0):.1f}%")
    
    st.markdown("### Your Dosha Profile")
    primary_dosha = results.get('primary_dosha', '')
    st.markdown(f"**Primary Dosha:** {primary_dosha.title()}")
    
    secondary_dosha = results.get('secondary_dosha')
    if secondary_dosha:
        st.markdown(f"**Secondary Dosha:** {secondary_dosha.title()}")
    
    st.markdown("---")
    st.info("""
        ℹ️ To get personalized health recommendations based on your dosha profile, 
        please visit the 'Personal Consultation' section.
    """) 