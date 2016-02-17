from __future__ import print_function

import unittest
from simtk.openmm import app
import simtk.openmm as mm
from simtk import unit
import sys
import mbpol

class TestCustomForce(unittest.TestCase):
    """Test the functionality of Custom Dispersion Force xml file."""

    def test_water_br(self, pdb_file="./pdb_files/water_br.pdb", expected_energy=-11.31415554):
        pdb = app.PDBFile(pdb_file)
        nonbondedMethod=app.CutoffNonPeriodic  
        forcefield = app.ForceField("../i-TTM_disp.xml")
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
        print("calculated energy = {}  expected energy = {}".format(potential_energy.in_units_of(unit.kilocalorie_per_mole)._value, expected_energy))
        
        
        self.assertTrue(abs(potential_energy.in_units_of(unit.kilocalorie_per_mole)._value - expected_energy) < .01)
    def test_water_br1(self):
        self.test_water_br(pdb_file="./pdb_files/water_br21.pdb", expected_energy=-22.87013473)
    def test_Cl_Na(self):
        self.test_water_br(pdb_file="./pdb_files/cl_na.pdb", expected_energy=-3.63642201)
    def test_I_Li(self):
        self.test_water_br(pdb_file="./pdb_files/i_li.pdb", expected_energy=-1.55391088)
       
if __name__ == '__main__':
    unittest.main()
