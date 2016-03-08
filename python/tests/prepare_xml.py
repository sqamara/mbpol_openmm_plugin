
# In[ ]:

import binascii
import xml.etree.ElementTree as etree

def prepare_xml(percent_pol = 1):  # 1 or .5
    with open("../i-TTM_template.xml") as f:
        ForceField = etree.parse( f ).getroot()
    #etree.dump(ForceField)
    
    
    # In[ ]:
    
    MBPolElectrostaticsForce = ForceField.find("./MBPolElectrostaticsForce")
    
    
    # In[ ]:
    
    while MBPolElectrostaticsForce.find("./Atom") != None:
        MBPolElectrostaticsForce.remove( MBPolElectrostaticsForce.find("./Atom") )
    
    
    # In[ ]:
    
    parameters = [
        #type        charge         damp_fac   polariz
        ["MBPol-O", -5.1966000e-01,  0.00131,  0.00131],
        ["MBPol-H",  2.5983000e-01,  0.000294, 0.000294],
        ["MBPol-M",  0,              0.00131,  0],
        ["MBPol-Li" , 1, 0.02848e-3 ,0.02848e-3],
        ["MBPol-Na" , 1, 0.14759e-3 ,0.14759e-3],
        ["MBPol-F"  ,-1, 2.4669e-3  ,2.4669e-3 ],
        ["MBPol-Cl" ,-1, 5.3602e-3  ,5.3602e-3 ],
        ["MBPol-Br" ,-1, 7.1668e-3  ,7.1668e-3 ],
        ["MBPol-I"  ,-1, 10.1184e-3 ,10.1184e-3],
    ]
    
    
    # In[ ]:
    for x in range(0, len(parameters)):
        p = parameters[x]
        if x < 3 :
            value = "Atom type=\"{}\" charge=\"{}\" damping-factor=\"{}\" polarizability=\"{}\"".format(p[0],p[1],p[2],p[3])
            etree.SubElement(MBPolElectrostaticsForce, value)
        else :
            value = "Atom type=\"{}\" charge=\"{}\" damping-factor=\"{}\" polarizability=\"{}\"".format(p[0],p[1],p[2]*percent_pol,p[3]*percent_pol)
            etree.SubElement(MBPolElectrostaticsForce, value)
    #etree.dump(ForceField)
    
    
    # In[ ]:
    d6table_100 = [ # a**-1
    #     O        H        M       Li       Na        F       Cl       Br        I
    9.29548, 9.77520,       0, 4.02327, 3.76951, 3.58619, 3.27542, 3.05825, 2.72314,# O
    9.77520, 9.40647,       0, 4.00672, 3.82261, 2.69768, 2.78226, 2.79804, 2.79911,# H
          0,       0,       0,       0,       0,       0,       0,       0,       0,# M
    4.02327, 4.00672,       0, 6.63418,       0, 3.33069, 2.97021, 2.76135, 2.70532,# Li
    3.76951, 3.82261,       0,       0, 5.17793, 3.52363, 2.69336,  2.5252,  2.4457,# Na
    3.58619, 2.69768,       0, 3.33069, 3.52363, 2.04316,       0,       0,       0,#  F
    3.27542, 2.78226,       0, 2.97021, 2.69336,       0, 1.86699,       0,       0,# Cl
    3.05825, 2.79804,       0, 2.76135,  2.5252,       0,       0, 1.79922,       0,# Br
    2.72314, 2.79911,       0, 2.70532,  2.4457,       0,       0,       0, 1.79453,#  I
    ]
    
    Atable_100 = [
    #     O        H        M       Li       Na        F       Cl       Br        I
          0,       0,       0,   32318, 47827.7, 35920.3, 50180.4, 37682.2,   22210,  # 0
          0,       0,       0, 3245.78, 4992.61, 800.553, 2594.28, 3804.53,  6215.1,  # H 
          0,       0,       0,       0,       0,       0,       0,       0,       0,  # M 
      32318, 3245.78,       0, 26110.8,       0, 18959.5, 27202.5,   27815, 36470.8,  # Li
    47827.7, 4992.61,       0,       0,  134244, 37835.8, 26832.4, 26310.6, 31172.4,  # Na
    35920.3, 800.553,       0, 31172.4, 37835.8, 1687.14,       0,       0,       0,  # F 
    50180.4, 2594.28,       0, 27202.5, 26832.4,       0, 3246.54,       0,       0,  # Cl
    37682.2, 3804.53,       0,   27815, 26310.6,       0,       0, 3674.06,       0,  # Br
      22210,  6215.1,       0, 36470.8, 31172.4,       0,       0,       0, 6672.41,  # I 
    ]
    
    #btable_100 = d6table_100
    
    d6table_50 = [ # a**-1
    #     O        H        M       Li       Na        F       Cl       Br        I
    9.29548, 9.77520,       0, 4.06168, 3.83356, 3.62593, 3.27841, 3.06223, 2.71168,# O
    9.77520, 9.40647,       0, 4.11558, 3.84424, 2.88984, 2.91544, 2.91497, 2.88304,# H
          0,       0,       0,       0,       0,       0,       0,       0,       0,# M
    4.06168, 4.11558,       0, 7.44687,       0, 3.77161, 3.38928, 3.08093, 3.04602,# Li
    3.83356, 3.84424,       0,       0, 5.29883, 4.07891, 3.02363, 2.86367, 2.77949,# Na
    3.62593, 2.88984,       0, 3.77161, 4.07891, 3.32578,       0,       0,       0,#  F
    3.27841, 2.91544,       0, 3.38928, 3.02363,       0, 2.90742,       0,       0,# Cl
    3.06223, 2.91497,       0, 3.08093, 2.86367,       0,       0, 2.58457,       0,# Br
    2.71168, 2.88304,       0, 3.04602, 2.77949,       0,       0,       0, 2.90977,#  I
    ]
    
    Atable_50 = [
    #     O        H        M       Li       Na        F       Cl       Br        I
          0,       0,       0, 34093.9, 53268.8,   38290,   49488, 37542.7, 21343.5,  #O
          0,       0,       0, 3802.56, 5246.9,  1231.27, 3422.72,  4776.13, 7259.5,  # H
          0,       0,       0,       0,       0,       0,       0,       0,       0,  # M
    34093.9, 3802.56,       0, 53757.6,       0, 23994.7, 37001.3, 33460.7, 46676.4,  # Li
    53268.8,  5246.9,       0,       0,  148248, 71367.6, 40193.9, 40711.5, 48844.2,  # Na
      38290, 1231.27,       0, 23994.7, 71367.6, 12784.7,       0,       0,       0,  # F
      49488, 3422.72,       0, 37001.3, 40193.9,       0, 31623.2,       0,       0,  # Cl
    37542.7, 4776.13,       0, 33460.7, 40711.5,       0,       0, 22256.6,       0,  # Br
    21343.5,  7259.5,       0, 46676.4, 48844.2,       0,       0,       0,  150494,  # I
    ]
    
    #btable_50 = d6table_50
        
    # In[ ]:
    
    Script = ForceField.find("./Script") 
    #etree.dump(Script)
    
    
    # In[ ]:
    
    if percent_pol == 1:
        d6table = d6table_100
        Atable  = Atable_100
    elif percent_pol == .5:
        d6table = d6table_50
        Atable  = Atable_50
    to_add = "d6table = {}\nAtable = {}\n# split here".format(str(d6table),str(Atable))
    Script.text = to_add + Script.text.split('split here',1)[1]
    #etree.dump(Script)
    
    
    # In[ ]:
    
    #etree.dump(ForceField)
    
    
    # In[ ]:
    
    #bytes.decode(etree.tostring( ForceField ))
    
    
    # In[ ]:
    
    with open("../i-TTM_template.xml" , "w" ) as f:
        f.write(bytes.decode(etree.tostring( ForceField )))
    
    
    # In[ ]:
    
    
    
    
    # In[ ]:
    
    
    
