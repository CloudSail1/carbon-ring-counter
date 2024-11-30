class TypeCutoff:
    def __init__(self) -> None:
        # index = particle_type -1
        self.tc = [[]]
        self.total_types = 0
        self.max_cutoff:float = 0.0


    def set(self, type_1: int, type_2: int, cutoff: float):
        type_max = max(type_1, type_2)
        # this would be delete after fix one type support
        if type_max > 1: raise ValueError("Only support one type used.")

        if type_max > self.total_types:
            self._expand_tc(type_max-self.total_types)
        
        if cutoff > self.max_cutoff:
            self.max_cutoff = cutoff

        self.tc[type_1-1][type_2-1] = cutoff**2
        self.tc[type_2-1][type_1-1] = cutoff**2

        return self
    

    def _expand_tc(self, num=1) -> None:
        self.total_types = self.total_types + num

        for i in self.tc:
            for _ in range(num):
                i.append(0)

        for _ in range(num):
            self.tc.append([0]*self.total_types)