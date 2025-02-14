import streamlit as st
import plotly.graph_objects as go
from sentence_transformers import SentenceTransformer, util

import warnings
warnings.filterwarnings("ignore")


# Load the smallest embedding model
model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L3-v2")

# Initialize session state for embeddings and click count
if "reference_embedding" not in st.session_state:
    st.session_state.reference_embedding = None
if "embedding_a" not in st.session_state:
    st.session_state.embedding_a = None
if "embedding_b" not in st.session_state:
    st.session_state.embedding_b = None
if "analyze_click_count" not in st.session_state:
    st.session_state.analyze_click_count = 0


# Collect user text inputs
st.title("Understanding Embedding Space")
st.markdown("Understand the relationship between texts based on their embeddings; How AI interpretes text/images. Enter a ***Reference*** Text along with ***Text-A*** and ***Text-B*** to visualize and compare their semantic closeness. 🚀")
reference_text = st.text_input("Reference Text", help="The main text to compare with Text-A and Text-B with.")
col1, col2 = st.columns(2)
with col1:
    text_a = st.text_input("Text-A", help="The first text to compare with the Reference Text... Could be something similar or different.")
with col2:
    text_b = st.text_input("Text-B", help="The second text to compare with the Reference Text... Could be something similar or different.")


if st.button("Analyze Texts"):
    try:
        # Ensure all text inputs are provided
        if not reference_text or not text_a or not text_b:
            # st.error("Please enter text in all three fields: Reference Text, Text-A, and Text-B.")
            raise ValueError("Missing text input")

        # Increment the click count
        st.session_state.analyze_click_count += 1

        if st.session_state.analyze_click_count == 3:
            st.success("If you're enjoying learning about embeddings, please consider giving the repo a star on [GitHub](https://github.com/wetrocloud/WetroLearn-TextEmbeddings)!")
            st.session_state.analyze_click_count = 0  # Reset the counter

        # Generate embeddings only if the text has changed
        if reference_text and (st.session_state.reference_embedding is None or st.session_state.reference_text != reference_text):
            st.session_state.reference_embedding = model.encode(reference_text, convert_to_tensor=True)
            st.session_state.reference_text = reference_text

        if text_a and (st.session_state.embedding_a is None or st.session_state.text_a != text_a):
            st.session_state.embedding_a = model.encode(text_a, convert_to_tensor=True)
            st.session_state.text_a = text_a

        if text_b and (st.session_state.embedding_b is None or st.session_state.text_b != text_b):
            st.session_state.embedding_b = model.encode(text_b, convert_to_tensor=True)
            st.session_state.text_b = text_b

        reference_embedding = st.session_state.reference_embedding
        embedding_a = st.session_state.embedding_a
        embedding_b = st.session_state.embedding_b

        reference_value = 0

        # Compute cosine similarity
        similarity_a = util.pytorch_cos_sim(reference_embedding, embedding_a).item()
        similarity_b = util.pytorch_cos_sim(reference_embedding, embedding_b).item()

        # Calculate distances
        distance_1 = abs(1 - similarity_a)
        distance_2 = abs(1 - similarity_b)

        # Create figure
        fig = go.Figure()

        # Add the reference point to the plot with hover text.
        fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers", name="Reference Text", marker=dict(color="blue", size=10), text=[reference_text], hoverinfo="text"))

        # Plot the lines... using abs and -ve or +ve values to plot the points on the correct side of the reference point.
        if distance_1 < distance_2:
            fig.add_trace(go.Scatter(x=[abs(distance_1)], y=[0], mode="markers", name="Text-A", marker=dict(color="green", size=10), text=[text_a], hoverinfo="text"))
            fig.add_trace(go.Scatter(x=[-abs(distance_2)], y=[0], mode="markers", name="Text-B", marker=dict(color="red", size=10), text=[text_b], hoverinfo="text"))

            fig.add_trace(go.Scatter(x=[reference_value, abs(distance_1)], y=[0, 0], mode="lines", line=dict(color="green", width=3), showlegend=False))
            fig.add_trace(go.Scatter(x=[reference_value, -abs(distance_2)], y=[0, 0], mode="lines", line=dict(color="red", width=3), showlegend=False))
        else:
            fig.add_trace(go.Scatter(x=[-abs(distance_1)], y=[0], mode="markers", name="Text-A", marker=dict(color="red", size=10), text=[text_a], hoverinfo="text"))
            fig.add_trace(go.Scatter(x=[abs(distance_2)], y=[0], mode="markers", name="Text-B", marker=dict(color="green", size=10), text=[text_b], hoverinfo="text"))

            fig.add_trace(go.Scatter(x=[reference_value, -abs(distance_1)], y=[0, 0], mode="lines", line=dict(color="red", width=3), showlegend=False))
            fig.add_trace(go.Scatter(x=[reference_value, abs(distance_2)], y=[0, 0], mode="lines", line=dict(color="green", width=3), showlegend=False))

        # Update layout
        fig.update_layout(title={"text": "Reference Text Similarity Compared To Text-A and Text-B", "x": 0.2},
                          xaxis_title="Value",
                          yaxis=dict(showgrid=False, zeroline=False),
                          showlegend=True)

        st.markdown("---")
        # Show figure in Streamlit
        st.markdown("### Analysis Results")
        if similarity_a > similarity_b:
            st.markdown(f"<p style='margin: 0;'><strong>Similarity between <em>Reference Text</em> and Text-A:</strong> <span style='color: green;'>{similarity_a*100:.2f}%</span></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='margin: 0;'><strong>Similarity between <em>Reference Text</em> and Text-B:</strong> <span style='color: red;'>{similarity_b*100:.2f}%</span></p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='margin: 0;'><strong>Similarity between <em>Reference Text</em> and Text-A:</strong> <span style='color: red;'>{similarity_a*100:.2f}%</span></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='margin: 0;'><strong>Similarity between <em>Reference Text</em> and Text-B:</strong> <span style='color: green;'>{similarity_b*100:.2f}%</span></p>", unsafe_allow_html=True)
        
        st.plotly_chart(fig)
    except ValueError as e:
        st.error(f"Please enter text in all three fields: Reference Text, Text-A, and Text-B.")