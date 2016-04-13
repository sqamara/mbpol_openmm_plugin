from __future__ import print_function
from simtk.openmm import app
import simtk.openmm as mm
from simtk import unit
import sys
import mbpol

#pdb = app.PDBFile("./equilibrated_boxes/w256_01.pdb")
pdb = app.PDBFile("./equilibrated_boxes/FM_25C.0.pdb")
expected_energy = -1731.11187

forcefield = app.ForceField("mbpol.xml")
boxsize = [1.96288955551, 1.96288955551, 1.96288955551]
pdb.topology.setUnitCellDimensions( boxsize )
system = forcefield.createSystem(pdb.topology, nonbondedMethod=app.PME, nonbondedCutoff=1.96288955551/2*unit.nanometer)
#system = forcefield.createSystem(pdb.topology, nonbondedMethod=app.PME, nonbondedCutoff=.65*unit.nanometer)
#system = forcefield.createSystem(pdb.topology, nonbondedMethod=app.PME, nonbondedCutoff=.45*unit.nanometer)
integrator = mm.VerletIntegrator(0.00001*unit.femtoseconds)
platform = mm.Platform.getPlatformByName('Reference')
simulation = app.Simulation(pdb.topology, system, integrator, platform)
simulation.context.setPositions(pdb.positions)
simulation.context.computeVirtualSites()
simulation.context.setVelocitiesToTemperature(298*unit.kelvin)
state = simulation.context.getState(getForces=True, getEnergy=True)
potential_energy = state.getPotentialEnergy()
potential_energy.in_units_of(unit.kilocalorie_per_mole)

print("@ {} calculated energy = {}  expected energy = {}".format(str(sys.argv[0]), potential_energy.in_units_of(unit.kilocalorie_per_mole)._value, expected_energy))

#kilocalorie_per_mole_per_angstrom = unit.kilocalorie_per_mole/unit.angstrom
#
#for f in state.getForces():
#    print(f.in_units_of(kilocalorie_per_mole_per_angstrom))
#
#from simtk.openmm import LocalEnergyMinimizer
#LocalEnergyMinimizer.minimize(simulation.context, 1e-1)
#
#state = simulation.context.getState(getForces=True, getEnergy=True, getPositions=True)
#potential_energy = state.getPotentialEnergy()
#potential_energy.in_units_of(unit.kilocalorie_per_mole)
#
#kilocalorie_per_mole_per_angstrom = unit.kilocalorie_per_mole/unit.angstrom
#for f in state.getForces():
#    print(f.in_units_of(kilocalorie_per_mole_per_angstrom))
#
#state.getPositions()
#
#simulation.context.setVelocitiesToTemperature(298*unit.kelvin)
#simulation.step(10)
#simulation.reporters.append(app.StateDataReporter(sys.stdout, 10, step=True, 
#    potentialEnergy=True, temperature=True, progress=True, remainingTime=True, 
#    speed=True, totalSteps=110, separator='\t'))
#
#
#simulation.reporters.append(app.PDBReporter('.equilibrated_boxes/w256_01_trajectory.pdb', 20))
#
#simulation.step(100)



