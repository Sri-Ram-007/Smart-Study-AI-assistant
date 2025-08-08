# app.py
import streamlit as st
from pdf_parser import extract_text
from topic_extractor import extract_topics
from resource_finder import fetch_all_resources
import time
import os

st.set_page_config(page_title="Syllabus Genius", page_icon="🚀", layout="centered")

st.title("Syllabus Genius 🚀")
st.write("Upload your course syllabus PDF and get a curated list of study resources in seconds.")

uploaded_file = st.file_uploader("Choose your syllabus PDF file", type="pdf")

if uploaded_file is not None:
    if st.button("Generate Study Guide"):
        # Save uploaded file temporarily to pass its path
        temp_file_path = os.path.join(".", uploaded_file.name)
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        with st.spinner("Reading your syllabus... 📄"):
            raw_text = extract_text(temp_file_path)
        
        with st.spinner("Identifying topics... 🧠"):
            time.sleep(1) # Just for effect
            topics = extract_topics(raw_text)

        if not topics:
            st.error("Could not extract topics. The PDF might be image-based or in an unrecognized format.")
        else:
            st.success(f"Found {len(topics)} topics! Now fetching resources...")
            
            all_results = []
            progress_bar = st.progress(0)
            for i, topic in enumerate(topics):
                resources = fetch_all_resources(topic)
                all_results.append((topic, resources))
                time.sleep(1) # API rate limiting
                progress_bar.progress((i + 1) / len(topics))

            st.balloons()
            st.header("✨ Your Personalized Study Guide ✨", divider="rainbow")

            for topic, resources in all_results:
                with st.expander(f"📚 {topic}"):
                    if resources:
                        for resource in resources:
                            st.markdown(resource)
                    else:
                        st.write("No specific resources found for this topic.")
        
        # Clean up the temporary file
        os.remove(temp_file_path)
