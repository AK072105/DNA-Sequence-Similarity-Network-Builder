from Bio.Align import PairwiseAligner
from itertools import combinations



def perform_global_alignment(seq_a, seq_b):
    
    aligner = PairwiseAligner()

    aligner.mode = "global"

    aligner.match_score = 2
    aligner.mismatch_score = -1

    aligner.open_gap_score = -2
    aligner.extend_gap_score = -0.5

    alignment = aligner.align(seq_a, seq_b)[0]

    return alignment

def extract_aligned_sequences(alignment):

    aligned_a = alignment[0]
    aligned_b = alignment[1]

    return aligned_a, aligned_b




# The above code performs a global alignment of two DNA sequences using the Biopython library's PairwiseAligner. 
# It defines functions to perform the alignment and extract the aligned sequences. The aligned sequences have gaps introduced to maximize the alignment score.


def calculate_percentage_identity(aligned_a, aligned_b):

    match = 0

    total_positions = len(aligned_a)  # This gives the total number of aligned columns including gaps.

    for i in range(total_positions):

        if aligned_a[i] == aligned_b[i] and aligned_a[i] != "-":

            match += 1

    percentage_identity = (match / total_positions) * 100

    return percentage_identity

def calculate_coverage(aligned_a, aligned_b, seq_a, seq_b):

    paired_positions = 0

    for i in range(len(aligned_a)):

        if aligned_a[i] != "-" and aligned_b[i] != "-":

            paired_positions += 1

    coverage_a = (paired_positions / len(seq_a)) * 100

    coverage_b = (paired_positions / len(seq_b)) * 100

    return coverage_a, coverage_b

def gap_fraction(aligned_a, aligned_b):

    gap_columns = 0

    total_columns = len(aligned_a)

    for i in range(total_columns):

        if aligned_a[i] == "-" or aligned_b[i] == "-":

            gap_columns += 1

    gap_fraction = (gap_columns / total_columns) * 100

    return gap_fraction


def calculate_alignment_length(aligned_a):

    alignment_length = len(aligned_a)

    return alignment_length



def compare_sequences(seq_a, seq_b):

    alignment = perform_global_alignment(seq_a, seq_b)

    aligned_a, aligned_b = extract_aligned_sequences(alignment)

    identity = calculate_percentage_identity(aligned_a, aligned_b)

    coverage_a, coverage_b = calculate_coverage(aligned_a, aligned_b, seq_a, seq_b)

    gap_frac = gap_fraction(aligned_a, aligned_b)

    alignment_length = calculate_alignment_length(aligned_a)
    
    paired_positions = sum(
    1 for i in range(len(aligned_a))
    if aligned_a[i] != "-" and aligned_b[i] != "-"
)
    return {
        "percentage_identity": round(identity, 2),
        "coverage_a": round(coverage_a, 2),
        "coverage_b": round(coverage_b, 2),
        "gap_fraction": round(gap_frac, 2),
        "alignment_length": alignment_length,
        "paired_positions": paired_positions
    }


def compare_all_sequences(sequences):

    results = []

    for (id_a, seq_a), (id_b, seq_b) in combinations(sequences.items(), 2):

        comparison = compare_sequences(seq_a, seq_b)

        comparison["sequence_a"] = id_a
        comparison["sequence_b"] = id_b

        results.append(comparison)

    return results # A list of dictionaries.


def passes_thresholds(
    comparison,
    min_identity=70,
    min_coverage_a=70,
    min_coverage_b=70,
    max_gap_fraction=30
):

    if comparison["percentage_identity"] < min_identity:
        return False

    if comparison["coverage_a"] < min_coverage_a:
        return False

    if comparison["coverage_b"] < min_coverage_b:
        return False

    if comparison["gap_fraction"] > max_gap_fraction:
        return False

    return True

# main block 


if __name__ == "__main__":
    
    sequences = {
    "Seq1": "ATGCGTAC",
    "Seq2": "ATGCGTCC",
    "Seq3": "ATGCGTAA",
    "Seq4": "TTGGAACC"}

    all_results = compare_all_sequences(sequences)

    for result in all_results:
        print(result)
        
        if passes_thresholds(result): # if its True 
            
            print("Similar:", result["sequence_a"], result["sequence_b"])
            
        else: # if its False
            
            print("Not similar:", result["sequence_a"], result["sequence_b"])




