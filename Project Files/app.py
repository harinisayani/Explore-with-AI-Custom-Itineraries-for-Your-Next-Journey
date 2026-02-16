#libraries imported
import streamlit as st
import google.genai as gai
import pprint
import os
from datetime import datetime
from dotenv import load_dotenv
from fpdf import FPDF
from io import BytesIO

load_dotenv()

my_key = os.getenv("my_key")
client = gai.Client(api_key=my_key)
model=""
for m in client.models.list():
    model=m.name
    print(m.name)
    break
st.title("Travel Itinerary Generator")

#User Inputs
city=st.text_input("Enter the city you're visiting:")
start_date = st.date_input("Select the start date for your trip:", value=datetime.today())
end_date = st.date_input("Select the end date for your trip:", value=start_date)
days = (end_date - start_date).days
interets=st.multiselect(label="Choose your interests..",options=['Art','Museums','Outdoor Activities','Indoor','Good for Kids','Good for Young People'])
nights=st.number_input("Enter number of nights...",min_value=1,max_value=30)

prompt=""

if st.button("Generate Itinerary"):
    prompt = f"You are an travel expert. Give me an itenary for {city}, for {days} days and {nights} nights, assume each day starting at 10am and ending at 8pm having a buffer of 30 minutes between each activity. I like to"
    if "Art" in interets:
        prompt += " explore art,"
    if "Museums" in interets:
        prompt += " visit museums,"
    if "Outdoor Activities" in interets:
        prompt += " engage in outdoor activities,"
    if "Indoor" in interets:
        prompt += " explore indoor activities,"
    if "Good for Kids" in interets:
        prompt += " find places suitable for kids,"
    if "Good for Young People" in interets:
        prompt += " discover places suitable for young people,"
    prompt += """Format the itinerary exactly like this:

Day 1: Tour Place
Morning (10:00 AM - 1:00 PM):
- Activity name - short description

Afternoon (1:30 PM - 5:00 PM):
- Activity name - short description

Evening (5:30 PM - 7:00 PM):
- Activity name - short description

Night (7:30 PM - 9:00 PM):
- Activity name - short description

Optional:
- Optional suggestion

Repeat this format for each day. Ensure give only specified number of nights schedule only for nights.
"""

# Calling the OpenAI API
itinerary=""
if prompt!="":
    with st.spinner("Generating your itinerary... ⏳"):
        completion = client.models.generate_content(
            model=model,
            contents=prompt,
        )
    # Extract and display the generated itinerary
    itinerary = completion.text.strip()
    st.write(itinerary)
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)

    # Save PDF to memory
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    return BytesIO(pdf_bytes)

# Generate PDF
if itinerary!="":
    pdf_file = create_pdf(itinerary)
    # Download button
    st.download_button(
    label="📄 Download Itinerary as PDF",
    data=pdf_file,
    file_name="itinerary.pdf",
    mime="application/pdf"
    )


    