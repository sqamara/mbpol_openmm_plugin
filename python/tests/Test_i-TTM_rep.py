from __future__ import print_function

import unittest
from simtk.openmm import app
import simtk.openmm as mm
from simtk import unit
import sys
import mbpol

class TestCustomForce(unittest.TestCase):
    """Test the functionality of Custom Dispersion Force xml file."""

    def test_three_water(self, pdb_file="./pdb_files/water_br.pdb", expected_energy=0.03652582):
        pdb = app.PDBFile(pdb_file)
        nonbondedMethod=app.CutoffNonPeriodic  
        forcefield = app.ForceField("../i-TTM_rep_with_script.xml")
        nonbondedCutoff = 1e3*unit.nanometer
        
        if (nonbondedMethod == app.CutoffPeriodic):
            boxsize = [50, 50, 50]
            pdb.topology.setUnitCellDimensions( boxsize )
        system = forcefield.createSystem(pdb.topology, nonbondedMethod=nonbondedMethod, nonBondedCutoff=nonbondedCutoff)
      
        integrator = mm.VerletIntegrator(0.02*unit.femtoseconds)
        platform = mm.Platform.getPlatformByName('Reference')
        simulation = app.Simulation(pdb.topology, system, integrator, platform)
        simulation.context.setPositions(pdb.positions)
        simulation.context.computeVirtualSites()
        state = simulation.context.getState(getForces=True, getEnergy=True, getPositions=True)
        potential_energy = state.getPotentialEnergy()
        potential_energy.in_units_of(unit.kilocalorie_per_mole)
        #print("calculated energy = {}".format(potential_energy.in_units_of(unit.kilojoule_per_mole)._value))
        
        
        self.assertTrue(abs(potential_energy.in_units_of(unit.kilojoule_per_mole)._value - expected_energy) < .01)
    
    def test_Cl_Na(self):
        self.test_three_water(pdb_file="./pdb_files/cl_na.pdb", expected_energy=122.81085303)
    def test_I_Li(self):
        self.test_three_water(pdb_file="./pdb_files/i_li.pdb", expected_energy=162.97995526)
#    def test_water_Br(self):
#        self.test_three_water(pdb_file="./pdb_files/water_br.pdb", expected_energy=0.03652582)
       
if __name__ == '__main__':
    unittest.main()
