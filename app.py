import streamlit as st
import pandas as pd

# Retrieve the CSV URL from Streamlit secrets
CSV_URL = st.secrets["default"]["SHEET_URL"]

# Function to load data
@st.cache_data
def load_data(url):
    df = pd.read_csv(url, engine='python', on_bad_lines='skip', encoding='utf-8')
    return df

# Load data
df = load_data(CSV_URL)

# Clean and prepare data
df.columns = df.columns.str.strip()

df.rename(columns={
    'Authos': 'Author',
    'Link_for_docs:': 'Link for docs'
}, inplace=True)

# Ensure data types and strip spaces
for col in ['Year', 'Language', 'Month', 'Name of article', 'Field', 'Author']:
    df[col] = df[col].astype(str).str.strip()

# Sidebar navigation
page = st.sidebar.radio("Select Page", ["Home", "About"])

if page == "Home":
    st.title("Artikujt Sizinti - Ship")

    # Sidebar filters
    years = sorted(df['Year'].dropna().unique(), reverse=True)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_year = str(selected_year).strip()

    # Filter by year
    df_year = df[df['Year'] == selected_year]

    languages = df['Language'].dropna().unique()
    selected_language = st.sidebar.multiselect("Select Language", languages, default=languages)

    # Filter by language
    df_year = df_year[df_year['Language'].isin(selected_language)]

    fields = df['Field'].dropna().unique()
    selected_fields = st.sidebar.multiselect("Select Field", fields, default=fields)

    # Filter by field
    df_year = df_year[df_year['Field'].isin(selected_fields)]

    authors = df['Author'].dropna().unique()
    selected_authors = st.sidebar.multiselect("Select Author", authors, default=authors)

    # Filter by author
    df_year = df_year[df_year['Author'].isin(selected_authors)]

    # Define magazine order (months in Albanian)
    magazine_order = ["Janar", "Shkurt", "Mars", "Prill", "Maj", "Qershor",
                      "Korrik", "Gusht", "Shtator", "Tetor", "Nëntor", "Dhjetor"]

    magazines = df_year['Month'].dropna().unique()
    sorted_magazines = [mag for mag in magazine_order if mag in magazines]

    # Display articles by month
    for magazine in sorted_magazines:
        st.subheader(f"Muaji:  {magazine}")
        df_magazine = df_year[df_year['Month'] == magazine]
        
        articles = df_magazine[['Name of article', 'Link for docs', 'Author', 'Language', 'Field']].values.tolist()
        
        if articles:
            for idx, (title, link, author, language, field) in enumerate(articles, start=1):
                st.markdown(f"**{idx}. [{title}]({link})**")
                st.write(f" - *Author*: {author}")
                st.write(f" - *Language*: {language}")
                st.write(f" - *Field*: {field}")
                st.write("---")
        else:
            st.write("No articles available in this magazine.")

    # Button to refresh data
    if st.button('Refresh Data'):
        load_data.clear()
        df = load_data(CSV_URL)

elif page == "About":
    st.title("About")
    st.write("""
    **Artikujt Sizinti - Ship** is a curated list of articles sourced from a Google Sheet.
    
    This app allows users to filter articles by year, language, field, and author, and 
    display them month-by-month. The data source is updated dynamically from a Google Sheet.

    **Features:**
    - Pull data from a secure and configurable Google Sheet link stored in Streamlit Secrets.
    - Filter options and dynamic display for user convenience.
    - Straightforward refresh functionality.

    **Made With:**
    - [Streamlit](https://streamlit.io/)
    - [Pandas](https://pandas.pydata.org/)

    For questions or comments, please contact the developer.
    """)
