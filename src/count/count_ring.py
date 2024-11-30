from ovito.data import DataCollection

# TODO auto get number of types and atoms
class CountRing:
    # sys info
    _total_atom: int
    # input var
    _number_ring_to_count: list[int]
    _neighbors: list[list[int]]

    class _NMumberRing:
        number_in_ring: int
        total_number_ring: int
        atom_in_many_ring: list[int]
        _neighbors: list[list[int]]
        _total_atom: int

        def __init__(self, number_in_ring: int, _neighbors: list[list[int]], total_atom: int):
            self.number_in_ring = number_in_ring
            self._neighbors = _neighbors
            self._total_atom = total_atom

            (self.total_number_ring, self.atom_in_many_ring) = self._count_num_member_ring()


        def _count_num_member_ring(self) -> tuple[int,list[int]]:
            result_sum = 0
            result_list:list[int] = []
            for i in range(self._total_atom):
                result_list.append(self._atom_in_many_ring(i, scan_depth=self.number_in_ring))
                if result_list[-1]==3:
                    result_sum = result_sum + 1
            return (result_sum, result_list)
        

        def _atom_in_many_ring(self, index:int, scan_depth:int) -> int:
            num_in_ring = 0
            relatives = self._get_neighbor_with_scan_depth([index], scan_depth)
            for relative in relatives:
                if relative == index:
                    num_in_ring = num_in_ring + 1
            return num_in_ring / 2
        

        def _get_neighbor_with_scan_depth(self, indese:list[int], scan_depth:int, history:list[int]=[], depth=0) -> list[int]:
            result:list[int] = []
            if type(scan_depth) != int:
                raise TypeError('111'+format(scan_depth)+str(depth))
            if depth >= scan_depth:
                return indese
            for index in indese:
                is_included = False
                if depth != 0:
                    for i in history:
                        if i == index:
                            is_included = True
                            break
                
                if not is_included:
                    result.extend(
                        self._get_neighbor_with_scan_depth(
                            self._neighbors[index], scan_depth, history+[index], depth+1
                            )
                        )
            return result
        
    _list_n_member_ring: list[_NMumberRing]


    def __init__(self, neighbors:list[list[int]], number_ring_to_count:list[int], total_atom:int):
        self._neighbors = neighbors
        self._number_ring_to_count = number_ring_to_count
        self._total_atom = total_atom

        self._list_n_member_ring = []
        for num in self._number_ring_to_count:
            self._list_n_member_ring.append(
                self._NMumberRing(num, self._neighbors, self._total_atom)
            )
    

    def write_property(self, data: DataCollection):
        for n_member_ring in self._list_n_member_ring:
            particle_name = 'AtomInHowMany' + str(n_member_ring.number_in_ring) + 'MemberRing'
            data.particles_.create_property(name=particle_name, data=n_member_ring.atom_in_many_ring, dtype=int)

        return self
    

    def write_attribute(self, data: DataCollection):
        for n_member_ring in self._list_n_member_ring:
            attribute_name = 'total_number_of_atom_in_' + str(n_member_ring.number_in_ring) + '_member_ring'
            data.attributes[attribute_name] = n_member_ring.total_number_ring

            if n_member_ring.number_in_ring == 6:
                num_in_3_six_ring = 0   # number of atom in three six ring

                num_in_ring_bin_2 = 0   # number of atom in ring and sp
                num_in_ring_bin_3 = 0   # number of atom in ring and sp2
                num_in_ring_bin_4 = 0   # number of atom in ring and sp3

                num_no_ring_bin_2 = 0   # number of atom outside ring and sp
                num_no_ring_bin_3 = 0   # number of atom outside ring and sp2
                num_no_ring_bin_4 = 0   # number of atom outside ring and sp3

                for i, number_in_ring in enumerate(n_member_ring.atom_in_many_ring):
                    if number_in_ring == 3:
                        num_in_3_six_ring += 1

                    if number_in_ring != 0:
                        match len(n_member_ring._neighbors[i])-1:
                            case 2:
                                num_in_ring_bin_2 += 1
                            case 3:
                                num_in_ring_bin_3 += 1
                            case 4:
                                num_in_ring_bin_4 += 1
                            case _:
                                continue

                    if number_in_ring == 0:
                        match len(n_member_ring._neighbors[i])-1:
                            case 2:
                                num_no_ring_bin_2 += 1
                            case 3:
                                num_no_ring_bin_3 += 1
                            case 4:
                                num_no_ring_bin_4 += 1
                            case _:
                                continue

                data.attributes['atom_in_three_six_ring'] = num_in_3_six_ring

                data.attributes['atom_in_ring_and_sp'] = num_in_ring_bin_2
                data.attributes['atom_in_ring_and_sp2']= num_in_ring_bin_3
                data.attributes['atom_in_ring_and_sp3']= num_in_ring_bin_4

                data.attributes['atom_outside_ring_and_sp'] = num_no_ring_bin_2
                data.attributes['atom_outside_ring_and_sp2']= num_no_ring_bin_3
                data.attributes['atom_outside_ring_and_sp3']= num_no_ring_bin_4

        return self