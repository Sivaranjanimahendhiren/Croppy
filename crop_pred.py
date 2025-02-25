
import streamlit as st
import PyPDF2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# File uploader for CSV
uploaded_csv = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_csv is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_csv)
    
    # Display the DataFrame
    st.subheader("📊 Uploaded CSV Data:")
    st.dataframe(df)
if uploaded_csv is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_csv)
    
    # Display the DataFrame
    st.subheader("📊 Uploaded CSV Data:")
    st.dataframe(df)

# Function to check if the uploaded file is a valid PDF
def is_valid_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        return len(pdf_reader.pages) > 0
    except Exception:
        return False

# Function to extract metadata from PDF
def extract_pdf_metadata(file):
    pdf_reader = PyPDF2.PdfReader(file)
    metadata = pdf_reader.metadata

    return {
        "Title": metadata.title if metadata and metadata.title else "N/A",
        "Author": metadata.author if metadata and metadata.author else "N/A",
        "Total Pages": len(pdf_reader.pages),
    }

# Function to extract text from all pages of the PDF
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = "\n\n".join([page.extract_text() or "" for page in pdf_reader.pages])
    return text.strip()

# Function to map extracted data into a DataFrame
def map_data_to_dataframe(extracted_data):
    columns = [
        "Year", "Soil pH", "Moisture (%)", "Nitrogen (N)", "Phosphorus (P)", "Potassium (K)", "Organic Matter (%)", 
        "Temperature (°C)", "Rainfall (mm)", "Sunlight (hrs/day)", "Soil Salinity (dS/m)", "Microbial Activity", 
        "Pesticide Use (kg/ha)", "Crop Type", "Yield (tons/ha)", "Revenue ($)", "Best Fertilizer", 
        "Yield Trend", "Pest Incidents", "Disease Cases", "Water Usage (L/ha)", "Crop Rotation Suggestion"
    ]

    corrected_data = [row + [''] * (len(columns) - len(row)) for row in extracted_data]
    df = pd.DataFrame(corrected_data, columns=columns)

    for col in ["Year", "Soil pH", "Moisture (%)", "Temperature (°C)", "Rainfall (mm)", "Yield (tons/ha)", "Water Usage (L/ha)"]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

# Streamlit UI
st.title("📄 PDF Upload, Metadata & Dashboard")

uploaded_file = st.file_uploader("Upload your document", type=["pdf"])

if uploaded_file is not None:
    if is_valid_pdf(uploaded_file):
        st.success("✅ You uploaded a valid PDF!")
        
        pdf_details = extract_pdf_metadata(uploaded_file)
        st.subheader("📑 PDF Details:")
        st.write(f"**File Name:** {uploaded_file.name}")
        st.write(f"**Title:** {pdf_details['Title']}")
        st.write(f"**Author:** {pdf_details['Author']}")
        st.write(f"**Total Pages:** {pdf_details['Total Pages']}")
        
        extracted_text = extract_text_from_pdf(uploaded_file)
        
        if extracted_text:
            st.subheader("📜 Extracted Text:")
            st.text_area("Text from your PDF", extracted_text, height=300)
        else:
            st.warning("⚠️ No extractable text found in this PDF.")
        
        # Sample extracted data (Replace with actual parsed data)
        extracted_data = [
            ["2019", "6.8", "21", "Medium", "Medium", "High", "4.2", "25", "850", "6.5", "1.2", "High", "1.5", "Maize", "5.2", "10,000", "NPK 15-15-15", "Stable", "Low", "2", "4,500", "Rotate with Legumes"],
            ["2020", "6.5", "20", "High", "Medium", "Low", "4.0", "24", "900", "6.2", "1.4", "Medium", "2.0", "Wheat", "4.8", "9,500", "NPK 10-20-10", "Increasing", "Medium", "3", "4,800", "Rotate with Vegetables"],
            ["2021", "6.4", "18", "Medium", "High", "Medium", "3.8", "26", "880", "6.8", "1.5", "High", "1.8", "Corn", "5.5", "10,200", "Urea 46-0-0", "Stable", "Low", "1", "4,700", "Rotate with Pulses"],
        ]

        df = map_data_to_dataframe(extracted_data)

        st.subheader("📊 Crop Data Insights:")
        st.dataframe(df)

        st.subheader("📊 Visualizations & Reports")
        
        st.write("### 📊 Yield Trends Over the Years")
        fig1 = px.bar(df, x="Year", y="Yield (tons/ha)", title="Yearly Crop Yield", color="Crop Type")
        st.plotly_chart(fig1)
        
        st.write("### 🌦️ Temperature & Rainfall Trends")
        fig2 = px.line(df, x="Year", y=["Temperature (°C)", "Rainfall (mm)"], title="Temperature & Rainfall Over Years")
        st.plotly_chart(fig2)
        
        st.write("### 🌾 Crop Type Distribution")
        fig3 = px.pie(df, names="Crop Type", title="Crop Distribution by Type", hole=0.3)
        st.plotly_chart(fig3)
        
        st.write("### 🧪 Soil pH Variations")
        fig4, ax = plt.subplots()
        sns.boxplot(data=df, x="Year", y="Soil pH", ax=ax)
        ax.set_title("Soil pH Distribution Over Years")
        st.pyplot(fig4)
        
        st.write("### 💧 Yield vs. Water Usage")
        fig5 = px.scatter(df, x="Water Usage (L/ha)", y="Yield (tons/ha)", color="Crop Type", title="Yield vs. Water Usage")
        st.plotly_chart(fig5)
        
    else:
        st.error("❌ Invalid PDF document. Please upload a valid PDF.")

