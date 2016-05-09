
/* Portions copyright (c) 2006 Stanford University and Simbios.
 * Contributors: Pande Group
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject
 * to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 * OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS, CONTRIBUTORS OR COPYRIGHT HOLDERS BE
 * LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 * WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

#include "MBPolReferenceOneBodyForce.h"
#include <vector>
#include "mbpol_interaction_constants.h"
#include "MBPolReferenceTwoBodyForce.h"

using std::vector;
using OpenMM::RealVec;



/**---------------------------------------------------------------------------------------

   Calculate MBPol stretch bend angle ixn (force and energy)

   pot_nasa in mbpol

   @return energy

   --------------------------------------------------------------------------------------- */


MBPolReferenceOneBodyForce::MBPolReferenceOneBodyForce( ) : _nonbondedMethod(NonPeriodic) {

    _periodicBoxDimensions = RealVec( 0.0, 0.0, 0.0 );
}

void MBPolReferenceOneBodyForce::setPeriodicBox( const RealVec& box ){
    _periodicBoxDimensions = box;
}

RealVec MBPolReferenceOneBodyForce::getPeriodicBox( void ) const {
    return _periodicBoxDimensions;
}


MBPolReferenceOneBodyForce::NonbondedMethod MBPolReferenceOneBodyForce::getNonbondedMethod( void ) const {
    return _nonbondedMethod;
}

void MBPolReferenceOneBodyForce::setNonbondedMethod( MBPolReferenceOneBodyForce::NonbondedMethod nonbondedMethod ){
    _nonbondedMethod = nonbondedMethod;
}

#include <iostream>

double MBPolReferenceOneBodyForce::calculateOneBodyIxn(const RealVec& positionO, const RealVec& positionH1, const RealVec& positionH2,
        RealVec& forceO, RealVec& forceH1, RealVec& forceH2) const
{
    double ROH1[3], ROH2[3], RHH[3], dROH1(0), dROH2(0), dRHH(0);

    double c5z[245];
    // scaling factors for contributions to emperical potential
    const double f5z = 0.999677885;
    const double fbasis = 0.15860145369897;
    const double fcore = -1.6351695982132;
    const double frest = 1.0;

    for (size_t i = 0; i < 3; ++i) {
        ROH1[i] = positionH1[i] - positionO[i]; // H1 - O
        ROH2[i] = positionH2[i] - positionO[i]; // H2 - O
        RHH[i] = positionH1[i] - positionH2[i]; // H1 - H2

        // nm -> A
        ROH1[i] *= 10.;
        ROH2[i] *= 10.;
        RHH[i] *= 10.;

        dROH1 += ROH1[i]*ROH1[i];
        dROH2 += ROH2[i]*ROH2[i];
        dRHH += RHH[i]*RHH[i];
    }

    dROH1 = std::sqrt(dROH1);
    dROH2 = std::sqrt(dROH2);
    dRHH = std::sqrt(dRHH);
    
    const double costh =
        (ROH1[0]*ROH2[0] + ROH1[1]*ROH2[1] + ROH1[2]*ROH2[2])/(dROH1*dROH2);

        for (size_t i = 0; i < 245; ++i)
            c5z[i] = f5z*c5zA[i] + fbasis*cbasis[i]
                   + fcore*ccore[i] + frest*crest[i];

    const double deoh = f5z*deohA;
    const double phh1 = f5z*phh1A*std::exp(phh2);

    const double costhe = -.24780227221366464506;

    const double exp1 = std::exp(-alphaoh*(dROH1 - roh));
    const double exp2 = std::exp(-alphaoh*(dROH2 - roh));

    const double Va = deoh*(exp1*(exp1 - 2.0) + exp2*(exp2 - 2.0));
    const double Vb = phh1*std::exp(-phh2*dRHH);

    const double dVa1= 2.0*alphaoh*deoh*exp1*(1.0 - exp1)/dROH1;
    const double dVa2= 2.0*alphaoh*deoh*exp2*(1.0 - exp2)/dROH2;
    const double dVb = -phh2*Vb/dRHH;

    const double x1 = (dROH1 - reoh)/reoh;
    const double x2 = (dROH2 - reoh)/reoh;
    const double x3 = costh - costhe;

    double fmat[3][16];

    for (size_t i = 0; i < 3; ++i) {
        fmat[i][0] = 0.0;
        fmat[i][1] = 1.0;
    }

    for (size_t j = 2; j < 16; ++j) {
        fmat[0][j] = fmat[0][j - 1]*x1;
        fmat[1][j] = fmat[1][j - 1]*x2;
        fmat[2][j] = fmat[2][j - 1]*x3;
    }

    const double efac = std::exp(-b1*(std::pow((dROH1 - reoh), 2)
                                    + std::pow((dROH2 - reoh), 2)));

    double sum0(0), sum1(0), sum2(0), sum3(0);

    for (size_t j = 1; j < 245; ++j) {
        const size_t inI = idx1[j];
        const size_t inJ = idx2[j];
        const size_t inK = idx3[j];

        sum0 += c5z[j]*(fmat[0][inI]*fmat[1][inJ]
                      + fmat[0][inJ]*fmat[1][inI])*fmat[2][inK];

        sum1 += c5z[j]*((inI - 1)*fmat[0][inI - 1]*fmat[1][inJ]
                      + (inJ - 1)*fmat[0][inJ - 1]*fmat[1][inI])*fmat[2][inK];

        sum2 += c5z[j]*((inJ - 1)*fmat[0][inI]*fmat[1][inJ - 1]
                      + (inI - 1)*fmat[0][inJ]*fmat[1][inI - 1])*fmat[2][inK];

        sum3 += c5z[j]*(fmat[0][inI]*fmat[1][inJ] + fmat[0][inJ]*fmat[1][inI])
                      *(inK - 1)*fmat[2][inK - 1];
    }

    // energy
    const double Vc = 2*c5z[0] + efac*sum0;
    double e1 = Va + Vb + Vc;

    e1 += 0.44739574026257; // correction
    e1 *= cm1_kcalmol; // cm-1 --> Kcal/mol

    // derivatives

    const double dVcdr1 =
        (-2*b1*efac*(dROH1 - reoh)*sum0 + efac*sum1/reoh)/dROH1;

    const double dVcdr2 =
        (-2*b1*efac*(dROH2 - reoh)*sum0 + efac*sum2/reoh)/dROH2;

    const double dVcdcth = efac*sum3;

    double cal2joule = 4.184;

    double fH1, fH2;

    for (size_t i = 0; i < 3; ++i) {
        // H1

        fH1 = (dVa1*ROH1[i] + dVb*RHH[i] + dVcdr1*ROH1[i]
        + dVcdcth*(ROH2[i]/(dROH1*dROH2) - costh*ROH1[i]/(dROH1*dROH1))) * cm1_kcalmol  * cal2joule * 10;

        forceH1[i] -= fH1;

        fH2 = (dVa2*ROH2[i] - dVb*RHH[i] + dVcdr2*ROH2[i]
        + dVcdcth*(ROH1[i]/(dROH1*dROH2) - costh*ROH2[i]/(dROH2*dROH2))) * cm1_kcalmol  * cal2joule * 10;

        // H2
        forceH2[i] -= fH2;

        // O
        forceO[i] -= -(fH1 + fH2);
    }
    
//    std::cout << "\tenergy: " << e1 << std::endl;
//    std::cout << "dROH: " << dROH1 << std::endl;
//    std::cout << "dROH: " << dROH2 << std::endl;
//    std::cout << "dROH: " << dRHH << std::endl;
   
    return e1 * cal2joule;
}


RealOpenMM MBPolReferenceOneBodyForce::calculateForceAndEnergy( int numOneBodys, const std::vector<RealVec>& particlePositions, const std::vector<std::vector<int> >& allParticleIndices,
                                                                       vector<RealVec>& forces) const {
    RealOpenMM energy      = 0.0; 
    for (unsigned int ii = 0; ii < static_cast<unsigned int>(numOneBodys); ii++) {
        std::vector<RealVec> allPositions;

        for (unsigned int i=0; i < 3; i++)
            allPositions.push_back(particlePositions[allParticleIndices[ii][i]]);

//        std::cout << ii << std::endl;
//        std::cout << "before imaging" << std::endl;
//        std::cout << allPositions[0] << std::endl;
//        std::cout << allPositions[1] << std::endl;
//        std::cout << allPositions[2] << std::endl;
        if( _nonbondedMethod == Periodic )
            imageMolecules(_periodicBoxDimensions, allPositions);
//        std::cout << "after imaging" << std::endl;
//        std::cout << allPositions[0] << std::endl;
//        std::cout << allPositions[1] << std::endl;
//        std::cout << allPositions[2] << std::endl;
        energy                 +=  calculateOneBodyIxn(allPositions[0], allPositions[1], allPositions[2],
                forces[allParticleIndices[ii][0]], forces[allParticleIndices[ii][1]], forces[allParticleIndices[ii][2]]);

    }   
    return energy;
}

