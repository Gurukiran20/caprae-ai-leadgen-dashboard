# 🧠 Smart Lead & Insights Dashboard  

This project was developed as part of **Caprae Capital’s AI-Readiness Pre-Screening Challenge**.  
It is a practical and lightweight AI-powered toolthat helps sales and investing teams:
- **Detect and remove duplicate company leads**
- **prioritize companies based on key metrics**
- **visualize meaningful insights** through an interactive dashboard.

---

##  Features  

✅ **Duplicate Lead Detection & Cleaning**  
Automatically detects and removes near-duplicate company names using fuzzy string matching (`fuzzywuzzy`).  
Helps maintain clean lead data and prevents redundant outreach.  

✅ **Lead Prioritization**  
Implements a smart scoring algorithm that prioritizes leads based on factors such as:
- **Annual Revenue**
- **Marketing Spend**
- **Conversion Rate**
Ranks the highest potential leads for faster targeting.

✅ **Interactive Insights Dashboard**  
A simple and intuitive **Streamlit dashboard** built with **Plotly** for data visualization.  
Includes filters by
- **Industry**
- **Region**
- **District**
  which helps to explore patterns in the data.  

✅ **Top Insights Section**  
Displays key insights such as:  
- Total number of companies  
- Average revenue  
- Top-performing industry
- Regional conversion trends 

---

##  Tech Stack  

- **Python 3.10+**  
- **pandas**  
- **fuzzywuzzy**  
- **Streamlit**  
- **Plotly**  
- **Synthetic B2B CRM & Marketing Dataset** - dataset which is used in this project
---
---
## Folder structure

<img width="955" height="421" alt="image" src="https://github.com/user-attachments/assets/24a1e472-d731-42cb-a539-f6890c78afb0" />

---

## Dashboard preview

Below is a screenshot of the working Streamlit dashboard with filters, lead scores, and insights:

<img width="1901" height="966" alt="Screenshot 2025-10-13 151517" src="https://github.com/user-attachments/assets/154bd08d-fed1-44cd-a539-5856db9bb00a" />


screenshot of Top insights and Top 10 rows after cleaning and Ranking:

<img width="1889" height="967" alt="Screenshot 2025-10-13 151553" src="https://github.com/user-attachments/assets/ff312176-0008-4434-a4f7-c7c235609d88" />

---

##  How to Run Locally

1. **Clone the repository**

```bash
git clone https://github.com/Gurukiran20/caprae-ai-leadgen-dashboard.git
cd caprae-ai-leadgen-dashboard/leadscoreapp
```
2. **Create and activate virtual environment**
   - python -m venv venv
   - venv\Scripts\activate

3. **Install dependencies**
   - pip install -r requirements.txt

4. **Run the Streamlit app**
   - streamlit run main.py
 ---

 ---
#### License

This project is shared for evaluation and educational purposes only.  
For commercial use, please contact the author.
 ---
   
