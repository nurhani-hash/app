import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("Student Test Score Analysis System")

# Simpan data pelajar antara rerun
if "students" not in st.session_state:
    st.session_state.students = []

count = len(st.session_state.students)

# ---------- (a) & (b) Input dan pengendalian pengecualian ----------
if count < 3:
    st.subheader(f"Enter details for student {count + 1} of 3")

    name = st.text_input("Student Name", key=f"name_{count}")
    gender = st.radio("Gender", ["Male", "Female"], key=f"gender_{count}")
    score = st.number_input("Scores", min_value=0, max_value=100,
                            step=1, key=f"score_{count}")

    if st.button("Submit"):
        try:
            if name.strip() == "":
                raise ValueError("Student name cannot be empty!")
            st.session_state.students.append(
                {"Student Name": name.strip(), "Gender": gender, "Score": score}
            )
            st.rerun()
        except ValueError as e:
            st.error(str(e))

# ---------- Selepas 3 pelajar dimasukkan ----------
else:
    # (c) Array NumPy
    scores = np.array([s["Score"] for s in st.session_state.students])
    st.subheader("Score Statistics")
    st.write(f"Mean score: {np.mean(scores):.2f}")
    st.write(f"Maximum score: {np.max(scores)}")

    # (d) Pandas DataFrame
    df = pd.DataFrame(st.session_state.students)
    df["Result"] = np.where(df["Score"] >= 50, "Pass", "Fail")

    # (e) Susun skor menaik
    df_sorted = df.sort_values(by="Score", ascending=True).reset_index(drop=True)
    st.subheader("Results (Sorted by Score, Ascending)")
    st.dataframe(df_sorted)

    # Graf visualisasi skor
    st.subheader("Student Scores Graph")
    fig, ax = plt.subplots()
    ax.bar(df_sorted["Student Name"], df_sorted["Score"], color="steelblue")
    ax.set_xlabel("Student Name")
    ax.set_ylabel("Score")
    ax.set_title("Student Test Scores")
    ax.set_ylim(0, 100)
    st.pyplot(fig)

    # Butang untuk mula semula
    if st.button("Reset"):
        st.session_state.students = []
        st.rerun()