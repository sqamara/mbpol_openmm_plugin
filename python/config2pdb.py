import re
import sys

### usage
### python config2pdb.py filename
### makes a pdb file of same name in same directory

filename = str(sys.argv[1])
#filename = './water256/CONFIG.01'

f = open(filename, 'r')
atomsXYZ = []
for line in f:
    if "OW" in line or "HW" in line:
        location = f.readline()
        xyz = re.findall("-?\d+.\d+[[eE]?[-+]?\d+]?", location)
        atomsXYZ.append(xyz)
 #       print (xyz)
        if len(atomsXYZ)%4 == 3: #add m sites
            atomsXYZ.append([0,0,0])
        for i in range(0, len(xyz)):
            xyz[i] = float(xyz[i])

f.close()

pdb_filename_pieces = filename.split(".")
pdb_filename = pdb_filename_pieces[0] + "_" + pdb_filename_pieces[1] + ".pdb"


f = open(pdb_filename, 'w')

for i in range(0, len(atomsXYZ)):
    atom_type = " "
    if i%4 == 0:
        atom_type = "O"
        mol_atom_id = "O"
    elif i%4 == 1:
        atom_type = "H"
        mol_atom_id = "H1"
    elif i%4 == 2:
        atom_type = "H" 
        mol_atom_id = "H2"
    else:
        atom_type = " " 
        mol_atom_id = "M"

    pdb_template = "HETATM{num:>5} {atom:>4} HOH  {molnum:>4}    {x:>8.3f}{y:>8.3f}{z:>8.3f}  1.00  0.00          {element:>2}\n".format(num=i+1, atom=mol_atom_id, molnum=int(i/4+1), x=atomsXYZ[i][0], y=atomsXYZ[i][1], z=atomsXYZ[i][2], element=atom_type )

    f.write(pdb_template)

f.close()

