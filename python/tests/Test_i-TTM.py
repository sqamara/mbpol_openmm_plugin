from simtk.openmm import app 
import simtk.openmm as mm
from simtk import unit
import sys 
import mbpol



pdb_file="./pdb_files/water_and_ion.pdb"
expected_energy=0



pdb = app.PDBFile(pdb_file)
nonbondedMethod=app.CutoffNonPeriodic  
forcefield = app.ForceField("../mbpol.xml", "../i-TTM_rep_no_overlap.xml")
nonbondedCutoff = 1e3*unit.nanometer



if (nonbondedMethod == app.CutoffPeriodic):
    boxsize = [50, 50, 50] 
    pdb.topology.setUnitCellDimensions( boxsize )



system = forcefield.createSystem(pdb.topology, nonbondedMethod=nonbondedMethod, nonBondedCutoff=nonbondedCutoff)
 



forcefield._forces



system.getNumForces()



for i in range(0, system.getNumForces()):
    print(system.getForce(i))



forcefield._forces = [forcefield._forces[0],forcefield._forces[4]]
forcefield._forces



system = forcefield.createSystem(pdb.topology, nonbondedMethod=nonbondedMethod, nonBondedCutoff=nonbondedCutoff)
for i in range(0, system.getNumForces()):
    print(system.getForce(i))



integrator = mm.VerletIntegrator(0.02*unit.femtoseconds)



platform = mm.Platform.getPlatformByName('Reference')



simulation = app.Simulation(pdb.topology, system, integrator, platform)



simulation.context.setPositions(pdb.positions)



simulation.context.computeVirtualSites()



state = simulation.context.getState(getForces=True, getEnergy=True, getPositions=True)
potential_energy = state.getPotentialEnergy()
potential_energy.in_units_of(unit.kilocalorie_per_mole)




unittest.main()
