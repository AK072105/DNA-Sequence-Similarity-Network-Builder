import streamlit as st
from io import StringIO
import pandas as pd
from fasta_reader import read_fasta

from network_builder import build_network, identify_clusters

from network_visualizer import create_network_figure

from similarity import compare_all_sequences, passes_thresholds


# Website title
st.title("DNA Sequence Similarity Network Builder")

st.write(
    "Upload a FASTA file to extract DNA sequences "
    "and view their corresponding sequence IDs."
)


# File upload section
uploaded_file = st.file_uploader(
    "Upload your FASTA file",
    type=["fasta", "fa", "fna"]
)



# Process uploaded file
if uploaded_file is not None:

    try:


        # Read uploaded file
        fasta_text = uploaded_file.getvalue().decode("utf-8")

        # Convert text into a file-like object
        fasta_file = StringIO(fasta_text)

        # Extract sequences
        sequences = read_fasta(fasta_file)
        st.success("FASTA file successfully processed!")

        # Display total number of sequences
        st.write("Total number of sequences:", len(sequences))

        # Display extracted sequences
        st.subheader("Extracted DNA Sequences")

        for seq_id, sequence in sequences.items():

            st.write("Sequence ID:", seq_id)
            st.write("Sequence:", sequence)
            st.write("Sequence Length:", len(sequence))

       # Compare all sequence pairs
        all_results = compare_all_sequences(sequences)

        col1, col2 = st.columns([1, 2])

        with col1:
            # Adding sliders for similarity thresholds to the website.
            st.subheader("Similarity Thresholds")

            min_identity = st.slider(
                "Minimum Percentage Identity",
                min_value=0,
                max_value=100,
                value=70)
            min_coverage_a = st.slider(
                "Minimum Coverage of Sequence A",
                min_value=0,
                max_value=100,
                value=70)
            
            min_coverage_b = st.slider(
                "Minimum Coverage of Sequence B",
                min_value=0,
                max_value=100,
                value=70)
            max_gap_fraction = st.slider(
                "Maximum Gap Fraction",
                min_value=0,
                max_value=100,
                value=30)

        results_df = pd.DataFrame(all_results)
        results_df["status"] = results_df.apply(lambda row: "Similar" if passes_thresholds(
            row,
            min_identity,
            min_coverage_a,
            min_coverage_b,
            max_gap_fraction) else "Not Similar",
            axis=1)

        # Display comparison results
        st.subheader("Sequence Comparison Results")

        results_df = results_df[
            [ "sequence_a",
             "sequence_b",
             "percentage_identity",
             "coverage_a",
             "coverage_b",
             "gap_fraction",
             "alignment_length",
             "status"
             ]]

        results_df.index = range(1, len(results_df) + 1)
        
        st.dataframe(results_df, use_container_width=True,hide_index= True) 



        with col2:
            # Build the sequence similarity network
            graph = build_network(results_df, sequences)
            # Identify clusters
            clusters = identify_clusters(graph)
            # Create the network visualization
            fig = create_network_figure(graph)

            # Display network statistics
            st.subheader("Network Statistics")

            st.write("Total nodes/sequences:", graph.number_of_nodes())

            st.write("Total connections:", graph.number_of_edges())

            st.write("Number of clusters:", len(clusters))


            # Display network visualization
            st.subheader("Sequence Similarity Network:")

            st.plotly_chart(fig, use_container_width=True)

       

    except Exception as e:

        st.error(f"Error processing FASTA file: {e}")


        