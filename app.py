import streamlit as st
import pandas as pd

# Zëvendësoni me URL-në tuaj aktuale të CSV
# CSV_URL = 'https://docs.google.com/spreadsheets/d/1LDDs_-O4Z87EH1Wy9OGZ9Qwf9s4N9PGzG26oHrteAwU/edit?usp=sharing'
CSV_URL = 'https://docs.google.com/spreadsheets/d/1LDDs_-O4Z87EH1Wy9OGZ9Qwf9s4N9PGzG26oHrteAwU/export?format=csv'

# Function to load data
@st.cache_data
def load_data(url):
    df = pd.read_csv(url, engine='python', on_bad_lines='skip', encoding='utf-8')
    return df

df = load_data(CSV_URL)

st.title("Artikujt Sizinti - Ship")

# Remove any leading/trailing whitespace from column names
df.columns = df.columns.str.strip()

# Correct the column names if necessary
df.rename(columns={
    'Authos': 'Author',
    'Link_for_docs:': 'Link for docs'
}, inplace=True)

# Ensure data types are consistent and strip spaces
df['Year'] = df['Year'].astype(str).str.strip()
df['Language'] = df['Language'].astype(str).str.strip()
df['Month'] = df['Month'].astype(str).str.strip()
df['Name of article'] = df['Name of article'].astype(str).str.strip()
df['Field'] = df['Field'].astype(str).str.strip()
df['Author'] = df['Author'].astype(str).str.strip()

# Sidebar for year selection
years = sorted(df['Year'].dropna().unique(), reverse=True)
selected_year = st.sidebar.selectbox("Select Year", years)

# Convert selected_year to string to match data type
selected_year = str(selected_year).strip()

# Filter data for the selected year
df_year = df[df['Year'] == selected_year]

# Sidebar for language selection (optional)
languages = df['Language'].dropna().unique()
selected_language = st.sidebar.multiselect("Select Language", languages, default=languages)

# Filter data based on selected language(s)
df_year = df_year[df_year['Language'].isin(selected_language)]

# Sidebar for field selection
fields = df['Field'].dropna().unique()
selected_fields = st.sidebar.multiselect("Select Field", fields, default=fields)

# Filter data based on selected field(s)
df_year = df_year[df_year['Field'].isin(selected_fields)]

# Sidebar for author selection
authors = df['Author'].dropna().unique()
selected_authors = st.sidebar.multiselect("Select Author", authors, default=authors)

# Filter data based on selected author(s)
df_year = df_year[df_year['Author'].isin(selected_authors)]

# Get unique magazines (months) for the selected year
magazines = df_year['Month'].dropna().unique()

# Sort magazines if they are months
# magazine_order = [
#     "January", "February", "March", "April", "May", "June",
#     "July", "August", "September", "October", "November", "December"
# ]

# If months are in another language, adjust the order accordingly
# For example, if months are in Albanian:
magazine_order = ["Janar", "Shkurt", "Mars", "Prill", "Maj", "Qershor",
                  "Korrik", "Gusht", "Shtator", "Tetor", "Nëntor", "Dhjetor"]

sorted_magazines = [mag for mag in magazine_order if mag in magazines]

# Display magazines and their articles
for magazine in sorted_magazines:
    st.subheader(f"Muaji:  {magazine}")
    df_magazine = df_year[df_year['Month'] == magazine]
    
    articles = df_magazine[['Name of article', 'Link for docs', 'Author', 'Language', 'Field']].values.tolist()
    
    if articles:
        for idx, (title, link, author, language, field) in enumerate(articles, start=1):
            st.markdown(f"**{idx}. [{title}]({link})**")
            # Uncomment the lines below if you want to display additional details
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
