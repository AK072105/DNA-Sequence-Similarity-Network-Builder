def read_fasta(file):

    sequences = {}
    sequence_id = None
    current_sequence = []

    for line in file:

        line = line.strip()

        if not line:
            continue

        if line.startswith('>'):

            if sequence_id is not None:
                sequences[sequence_id] = ''.join(current_sequence)

            sequence_id = line[1:].split()[0]
            current_sequence = []

        else:
            if sequence_id is None:
                raise ValueError("Sequence found before FASTA header.")

            current_sequence.append(line.upper())

    if sequence_id is not None:
        sequences[sequence_id] = ''.join(current_sequence)

    if not sequences:
        raise ValueError("No sequences found in the FASTA file.")

    return sequences

