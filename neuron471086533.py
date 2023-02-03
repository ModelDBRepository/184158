'''
Defines a class, Neuron471086533, of neurons from Allen Brain Institute's model 471086533

A demo is available by running:

    python -i mosinit.py
'''
class Neuron471086533:
    def __init__(self, name="Neuron471086533", x=0, y=0, z=0):
        '''Instantiate Neuron471086533.
        
        Parameters:
            x, y, z -- position offset
            
        Note: if name is not specified, Neuron471086533_instance is used instead
        '''
             
        self._name = name
        # load the morphology
        from load_swc import load_swc
        load_swc('Sst-IRES-Cre_Ai14_IVSCC_-167638.05.02.01_397911799_m.swc', self,
                 use_axon=False, xshift=x, yshift=y, zshift=z)

        # custom axon (works because dropping axon during import)
        from neuron import h
        self.axon = [h.Section(cell=self, name='axon[0]'),
                     h.Section(cell=self, name='axon[1]')]
        for sec in self.axon:
            sec.L = 30
            sec.diam = 1
            sec.nseg = 1
        self.axon[0].connect(self.soma[0](0.5))
        self.axon[1].connect(self.axon[0](1))
        self.all += self.axon
   
        self._insert_mechanisms()
        self._discretize_model()
        self._set_mechanism_parameters()
    
    def __str__(self):
        if self._name is not None:
            return self._name
        else:
            return "Neuron471086533_instance"
                
    def _insert_mechanisms(self):
        from neuron import h
        for sec in self.all:
            sec.insert("pas")
        for mech in [u'CaDynamics', u'Ca_HVA', u'Ca_LVA', u'Ih', u'Im_v2', u'K_T', u'Kd', u'Kv2like', u'Kv3_1', u'NaV', u'SK']:
            self.soma[0].insert(mech)
    
    def _set_mechanism_parameters(self):
        from neuron import h
        for sec in self.all:
            sec.Ra = 117.86
            sec.e_pas = -92.921295166
        
        for sec in self.axon:
            sec.cm = 1.61
            sec.g_pas = 0.000379150415318
        for sec in self.dend:
            sec.cm = 1.61
            sec.g_pas = 6.98688301514e-07
        for sec in self.soma:
            sec.cm = 1.61
            sec.ena = 53.0
            sec.ek = -107.0
            sec.gbar_Ih = 3.61582e-05
            sec.gbar_NaV = 0.0370391
            sec.gbar_Kd = 0
            sec.gbar_Kv2like = 0.33075
            sec.gbar_Kv3_1 = 1.61412
            sec.gbar_K_T = 0.000493618
            sec.gbar_Im_v2 = 0.000594159
            sec.gbar_SK = 0
            sec.gbar_Ca_HVA = 4.20804e-05
            sec.gbar_Ca_LVA = 0.0010956
            sec.gamma_CaDynamics = 0.00989837
            sec.decay_CaDynamics = 653.479
            sec.g_pas = 2.62837e-06
    
    def _discretize_model(self):
        for sec in self.all:
            sec.nseg = 1 + 2 * int(sec.L / 40)

