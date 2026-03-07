import pandas as pd
import plotly.express as px

df = pd.read_csv("post_covid_health_effects_dataset.csv")

# Data Cleaning
df = df.replace({"Yes": 1, "No": 0})
df = df.drop_duplicates()
df = df.dropna()

figures = []

# 1. Age Distribution
fig1 = px.histogram(
    df,
    x="Age",
    title="Age Distribution of Post-COVID Patients",
    labels={'Age': 'Age', 'count': 'Number of Patients'}
)
figures.append(fig1)

# 2. COVID Severity vs Recovery
severity = df.groupby("COVID_Severity")["Days_to_Recovery"].mean()

fig2 = px.bar(
    x=severity.index,
    y=severity.values,
    title="Average Recovery Days by COVID Severity",
    labels={'x': 'COVID Severity', 'y': 'Average Recovery Days'}
)
figures.append(fig2)

# 3. Recovery Time vs Age
fig3 = px.scatter(
    df,
    x="Age",
    y="Days_to_Recovery",
    color="COVID_Severity",
    title="Recovery Time vs Age",
    labels={'Age': 'Age', 'Days_to_Recovery': 'Days to Recovery'}
)
figures.append(fig3)

# 4. Long COVID Risk
risk = df.groupby("Long_COVID_Risk")["Days_to_Recovery"].mean()

fig4 = px.pie(
    names=risk.index,
    values=risk.values,
    title="Long COVID Risk Distribution"
)
figures.append(fig4)

# 5. Mental Health Impact vs Age
activity = df.groupby("Mental_Health_Impact")["Age"].mean()

fig5 = px.line(
    x=activity.index,
    y=activity.values,
    title="Average Age by Mental Health Impact",
    labels={'x': 'Mental Health Impact', 'y': 'Average Age'}
)
figures.append(fig5)

# 6. Symptom Correlation Heatmap
symptoms = df[
    ["Fatigue_Level", "Breathing_Issue", "Brain_Fog", "Loss_of_Taste_Smell"]
]

symptoms = symptoms.replace({"Yes": 1, "No": 0})
corr = symptoms.corr()

fig6 = px.imshow(
    corr,
    text_auto=True,
    title="Correlation Between Post-COVID Symptoms"
)
figures.append(fig6)

with open("post_covid_analysis.html", "w") as f:
    for fig in figures:
        f.write(fig.to_html(full_html=False, include_plotlyjs='cdn')) #PlotlyScript CDN
