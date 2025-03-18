import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the datasets
hr_performance = pd.read_csv("data/HR_performance.csv", index_col=0)
hr_salary = pd.read_csv("data/HR_salary.csv", index_col=0)

#############################################
# Title, Course Info, and Author
#############################################
st.title("Simpson's Paradox")

st.markdown(
    """
    **Course**: Applied Management Research Methods
    
    **Teacher**: Dott. Federico Mangiò
    
    **Author**: Zuzanna Deszcz
    """
)

#############################################
# Intro and Data Samples
#############################################
st.markdown(
    """
    ## Introduction
    We use two datasets, `HR_performance` and `HR_salary`, which contain variables such as 
    Neuroticism, Performance, Salary, Education, and Job.
    """
)

st.subheader("Data Samples")
st.write("HR Performance:", hr_performance.head())
st.write("HR Salary:", hr_salary.head())

#####################
# Correlation Analysis
#####################
st.subheader("Overall Correlations")
if 'Neuroticism' in hr_performance.columns and 'Performance' in hr_performance.columns:
    corr_perf = hr_performance['Neuroticism'].corr(hr_performance['Performance'])
    st.write(f"Neuroticism vs Performance (overall): {corr_perf:.2f}")

if 'Neuroticism' in hr_salary.columns and 'Salary' in hr_salary.columns:
    corr_sal = hr_salary['Neuroticism'].corr(hr_salary['Salary'])
    st.write(f"Neuroticism vs Salary (overall): {corr_sal:.2f}")

########################################################
# Overall Scatter Plots with Regression Lines
########################################################
fig, ax = plt.subplots(1, 2, figsize=(14, 5))

# 1) Neuroticism vs Performance (overall)
if 'Neuroticism' in hr_performance.columns and 'Performance' in hr_performance.columns:
    sns.regplot(
        data=hr_performance,
        x='Neuroticism',
        y='Performance',
        ax=ax[0],
        scatter_kws={'alpha': 0.7},
        line_kws={'lw': 2}
    )
    ax[0].set_title("Overall: Neuroticism vs Performance")

# 2) Neuroticism vs Salary (overall)
if 'Neuroticism' in hr_salary.columns and 'Salary' in hr_salary.columns:
    sns.regplot(
        data=hr_salary,
        x='Neuroticism',
        y='Salary',
        ax=ax[1],
        scatter_kws={'alpha': 0.7},
        line_kws={'lw': 2}
    )
    ax[1].set_title("Overall: Neuroticism vs Salary")

st.pyplot(fig)

st.markdown(
    """
    At first glance, higher neuroticism might appear linked to higher performance or salary.
    Let us examine whether this pattern remains consistent when we introduce subgroup analysis 
    by Education or Job.
    """
)

########################################
# Subgroup Analysis: Education (Salary)
########################################
st.subheader("Salary vs Neuroticism by Education")

if all(col in hr_salary.columns for col in ['Neuroticism', 'Salary', 'Education']):
    g1 = sns.lmplot(
        data=hr_salary,
        x='Neuroticism',
        y='Salary',
        hue='Education',
        height=4,
        aspect=1.2,
        scatter_kws={'alpha': 0.7},
        line_kws={'lw': 2}
    )
    g1.set(title="Subgroups by Education")
    st.pyplot(g1.fig)
    st.write(
        "Here, some education levels may show a negative slope, reversing the initial positive correlation."
    )
else:
    st.write("Missing columns for Education analysis.")

##########################################
# Subgroup Analysis: Job (Performance)
##########################################
st.subheader("Performance vs Neuroticism by Job")

if all(col in hr_performance.columns for col in ['Neuroticism', 'Performance', 'Job']):
    g2 = sns.lmplot(
        data=hr_performance,
        x='Neuroticism',
        y='Performance',
        hue='Job',
        height=4,
        aspect=1.2,
        scatter_kws={'alpha': 0.7},
        line_kws={'lw': 2}
    )
    g2.set(title="Subgroups by Job")
    st.pyplot(g2.fig)
    st.write(
        "Different job types can drastically change the correlation between Neuroticism and Performance."
    )
else:
    st.write("Missing columns for Job analysis.")

########################################
# Conclusion
########################################
st.markdown(
    """
    ## Conclusion
    We have seen that a general correlation suggesting that higher neuroticism might 
    lead to higher salary or better performance can be overturned once we factor in 
    crucial subgroups such as Education or Job. This is the essence of Simpson's Paradox:
    an overall trend that reverses within certain categories. 

    Careful subgroup analysis is therefore essential before drawing conclusions about the 
    relationships in complex datasets.
    """
)