import os
from collections import defaultdict

# Folder with PLIP TXT outputs
input_folder = "TXT_outputs"
reference_file = "CD1d_aGalCer.txt"
total_detergents = 13  # exclude α-GalCer from count

# 3-letter to 1-letter amino acid mapping
aa3_to_1 = {
    'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D',
    'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G',
    'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
    'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S',
    'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V',
    # fallback for unknown residues
    'UNK': 'X'
}

# Data structure to track interactions
residue_data = defaultdict(lambda: {
    'Hydrophobic': {'count': 0, 'ligands': set()},
    'Hydrogen Bond': {'count': 0, 'ligands': set()},
    'Salt Bridge': {'count': 0, 'ligands': set()},
    'aGalCer': False
})

# Convert to 1-letter residue ID
def format_residue(resnr, restype3):
    restype = aa3_to_1.get(restype3.upper(), 'X')
    return f"{restype}{resnr}"

# Get ligand/detergent name from filename
def get_ligand_name(filename):
    return filename.replace("CD1d_", "").replace(".txt", "")

# Extract interactions from block
def parse_block(lines, interaction_type, residue_set):
    for line in lines:
        if line.startswith("|") and not line.startswith("+") and not line.startswith("="):
            cols = [col.strip() for col in line.strip("|").split("|")]
            if len(cols) < 2:
                continue
            resnr = cols[0]
            restype = cols[1]
            if not resnr.isdigit() or restype.upper() in {"RESTYPE", ""}:
                continue
            residue = format_residue(resnr, restype)
            residue_set.add(residue)

# Parse each file
for filename in os.listdir(input_folder):
    if not filename.endswith(".txt"):
        continue

    filepath = os.path.join(input_folder, filename)
    ligand_name = get_ligand_name(filename)
    is_aGalCer = (filename == reference_file)

    with open(filepath, 'r') as file:
        lines = file.readlines()

    residues_by_type = {
        'Hydrophobic': set(),
        'Hydrogen Bond': set(),
        'Salt Bridge': set()
    }

    for i, line in enumerate(lines):
        if "**Hydrophobic Interactions**" in line:
            parse_block(lines[i + 3:], 'Hydrophobic', residues_by_type['Hydrophobic'])
        elif "**Hydrogen Bonds**" in line:
            parse_block(lines[i + 3:], 'Hydrogen Bond', residues_by_type['Hydrogen Bond'])
        elif "**Salt Bridges**" in line:
            parse_block(lines[i + 3:], 'Salt Bridge', residues_by_type['Salt Bridge'])

    for interaction_type, residues in residues_by_type.items():
        for residue in residues:
            if not is_aGalCer:
                residue_data[residue][interaction_type]['count'] += 1
                residue_data[residue][interaction_type]['ligands'].add(ligand_name)
            else:
                residue_data[residue]['aGalCer'] = True

# Write output
output_file = "conserved_residue_summary.tsv"
with open(output_file, "w") as out:
    out.write("Residue\tType of interaction\t# of complexes (out of 13)\tInteracts with α-GalCer?\tLigands\n")
    for residue, data in sorted(
        residue_data.items(),
        key=lambda x: max(x[1]['Hydrophobic']['count'], x[1]['Hydrogen Bond']['count'], x[1]['Salt Bridge']['count']),
        reverse=True
    ):
        for interaction_type in ['Hydrophobic', 'Hydrogen Bond', 'Salt Bridge']:
            count = data[interaction_type]['count']
            if count > 0:
                ligands = ", ".join(sorted(data[interaction_type]['ligands']))
                out.write(f"{residue}\t{interaction_type}\t{count}/{total_detergents}\t{'✓' if data['aGalCer'] else '❌'}\t{ligands}\n")

print(f"✅ TSV summary written to: {output_file}")
