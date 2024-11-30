from .type_cutoff import TypeCutoff
from .count_ring import CountRing
from .fix_period import FixPeriod

from ovito.pipeline import ModifierInterface
from ovito.data import DataCollection
from scipy.spatial import cKDTree

class CountNeighborsModifier(ModifierInterface):
    def __init__(self, tc: TypeCutoff, count_ring:bool = False, count_many_member_ring:list[int] = []):
        """
        example:
        ```python
        type_cutoff = TypeCutoff().set(1,1,c1).set(1,2,c2).set(...).set(...)
        count_neighbors = CountNeighborsModifier(type_cutoff)
        ```
        If you want to count six member ring, use:
        ```python
        count_neighbors = CountNeighborsModifier(type_cutoff, true, [6])
        ```
        The property named `AtomInHowMany6MemberRing` will be writed to `DataCollection`, then you can output it.
        
        At mean time the attribute will named `total_number_of_atom_in_6_member_ring`.
        
        Or you want to count 5,6,7,8 member ring, use:
        ```python
        count_neighbors = CountNeighborsModifier(type_cutoff, count_many_member_ring=[5,6,7,8])
        ```
        """
        self.neighbors = []
        self.tc = tc.tc
        self.total_types = tc.total_types
        self.max_cutoff = tc.max_cutoff
        self.total_atom = 0
        self.count_ring = count_ring
        if count_ring:
            self.count_many_member_ring = count_many_member_ring


    def modify(self, data: DataCollection, *, frame, input_slots, data_cache, pipeline_node, **kwargs):
        self.total_atom = data.particles.count

        # period fix
        bound = [(data.cell[0][3],data.cell[0][0]+data.cell[0][3]),
                 (data.cell[1][3],data.cell[1][1]+data.cell[1][3]),
                 (data.cell[2][3],data.cell[2][2]+data.cell[2][3])]
        position: list[tuple[float, float, float]] = []
        for i in data.particles.positions:
            position.append((i[0],i[1],i[2]))

        fix_period = FixPeriod(position, bound,self.max_cutoff)

        kdtree = cKDTree(fix_period.get())
        # using the max cutoff to build a list
        neighbors_raw:list[list[int]] = kdtree.query_ball_point(x=data.particles.positions, r=self.max_cutoff, workers=-1)

        n_neighbors: list[int] = []  
        for i in neighbors_raw:
            n_neighbors.append(len(i)-1)

        self.neighbors = fix_period.adjust_neighbors(neighbors_raw)

        data.particles_.create_property(name="Neighbors",data=n_neighbors)

        if self.count_ring == True:
            CountRing(
                self.neighbors,
                self.count_many_member_ring, 
                self.total_atom)\
            .write_property(data)\
            .write_attribute(data)