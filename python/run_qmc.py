from simtk.openmm import app
import simtk.openmm as mm
from simtk import unit
import sys
import mbpol
import os.path
import pandas as pd

pdb_filename = sys.argv[1]
pdb = app.PDBFile(pdb_filename)

tag = os.path.basename(pdb_filename).replace(".pdb", "")

# PME box size
if tag.startswith("H2O"):
    boxSize = 24.8343697144598003
elif tag.startswith("FM_25C") or tag.startswith("TIP5P_25C"):
    boxSize = 19.7316565863235596
else:
    boxSize = 19.3996888399961804
boxSize /= 10.
pdb.topology.setUnitCellDimensions((boxSize,boxSize,boxSize))

forcefield = app.ForceField("mbpol.xml")

system = forcefield.createSystem(pdb.topology, nonbondedMethod=app.PME, nonbondedCutoff=.9*unit.nanometer)
integrator = mm.VerletIntegrator(0.00001*unit.femtoseconds)

platform = mm.Platform.getPlatformByName('Reference')
simulation = app.Simulation(pdb.topology, system, integrator, platform)
simulation.context.setPositions(pdb.positions)
simulation.context.computeVirtualSites()

state = simulation.context.getState(getForces=True, getEnergy=True)
potential_energy = state.getPotentialEnergy()
energy_kcal_per_mol = potential_energy.value_in_unit(unit.kilocalorie_per_mole)

output = pd.DataFrame(dict(
                box_size = boxSize,
                energy_kcal_per_mol = energy_kcal_per_mol
                ), index=[tag])

#kilocalorie_per_mole_per_angstrom = unit.kilocalorie_per_mole/unit.angstrom
#for f in state.getForces():
#    print(f.in_units_of(kilocalorie_per_mole_per_angstrom))

forces = system.getForces()[:-1]

for num, force in enumerate(forces):
    force.setForceGroup(num)

state = simulation.context.getState(getForces=True, getEnergy=True, groups=2**0)
potential_energy = state.getPotentialEnergy()

force_labels = ["electrostatics", "onebody", "twobody", "threebody", "dispersion"]

for num, force in enumerate(forces):
    state = simulation.context.getState(getForces=True, getEnergy=True, groups=2**num)
    potential_energy = state.getPotentialEnergy()
    output[force_labels[num]] = potential_energy.value_in_unit(unit.kilocalorie_per_mole)

output.to_json(pdb_filename.replace(".pdb", "_out.json"), orient="index")
