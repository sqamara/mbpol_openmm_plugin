from __future__ import print_function
from simtk.openmm import app
import simtk.openmm as mm
from simtk import unit
import sys
import mbpol

pdb = app.PDBFile("./equilibrated_boxes/w512_01.pdb")
expected_energy = -3453.72854

forcefield = app.ForceField("mbpol.xml")
#forcefield = app.ForceField("tip4pew.xml")
#boxsize = [2.71863313515, 2.71863313515, 2.71863313515]
boxsize = [2.35614871713, 2.35614871713, 2.71863313515]
pdb.topology.setUnitCellDimensions( boxsize )
system = forcefield.createSystem(pdb.topology, nonbondedMethod=app.PME, nonbondedCutoff=2.3/2*unit.nanometer)
#system = forcefield.createSystem(pdb.topology, nonbondedMethod=app.PME, nonbondedCutoff=.65*unit.nanometer)
#system = forcefield.createSystem(pdb.topology, nonbondedMethod=app.PME, nonbondedCutoff=.45*unit.nanometer)
integrator = mm.VerletIntegrator(0.00001*unit.femtoseconds)
platform = mm.Platform.getPlatformByName('Reference')
simulation = app.Simulation(pdb.topology, system, integrator, platform)
simulation.context.setPositions(pdb.positions)
simulation.context.computeVirtualSites()
state = simulation.context.getState(getForces=True, getEnergy=True)
potential_energy = state.getPotentialEnergy()
potential_energy.in_units_of(unit.kilocalorie_per_mole)

print("@ {} calculated energy = {}  expected energy = {}".format(str(sys.argv[0]), potential_energy.in_units_of(unit.kilocalorie_per_mole)._value, expected_energy))



forces = system.getForces()[:-1]
for num, force in enumerate(forces):
    force.setForceGroup(num)
force_labels = ["electrostatics", "onebody", "twobody", "threebody", "dispersion"]
for num, force in enumerate(forces):
    state = simulation.context.getState(getForces=True, getEnergy=True, groups=2**num)
    potential_energy = state.getPotentialEnergy()
    print ("{} = {}".format(force_labels[num], potential_energy.value_in_unit(unit.kilocalorie_per_mole)))

