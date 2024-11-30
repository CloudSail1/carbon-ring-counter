class FixPeriod:
    _atoms: list[tuple[float, float, float]]
    _bound: list[tuple[float, float]]
    _detect_radius: float
    _ghosts: list[list[float, float, float]]
    _ghost_affine: dict # ghost -> atom

    def __init__(self,
                 atoms:list[list[int, int, float, float, float]],
                 bound:list[tuple[float, float]],
                 detect_radius: float):
        self._atoms = atoms
        self._bound = bound
        self._detect_radius = detect_radius

        x_len = self._bound[0][1] - self._bound[0][0]
        y_len = self._bound[1][1] - self._bound[1][0]
        z_len = self._bound[2][1] - self._bound[2][0]

        x_lower = bound[0][0]+detect_radius
        x_upper = bound[0][1]-detect_radius
        y_lower = bound[1][0]+detect_radius
        y_upper = bound[1][1]-detect_radius
        z_lower = bound[2][0]+detect_radius
        z_upper = bound[2][1]-detect_radius
        self._ghosts = []
        self._ghost_affine = dict()

        for i, atom in enumerate(self._atoms):
            if atom[0] < x_lower:
                self._ghosts.append([atom[0]+x_len, atom[1], atom[2]])
                self._append_affine(i)
            if atom[0] > x_upper:
                self._ghosts.append([atom[0]-x_len, atom[1], atom[2]])
                self._append_affine(i)
            if atom[1] < y_lower:
                self._ghosts.append([atom[0], atom[1]+y_len, atom[2]])
                self._append_affine(i)
            if atom[1] > y_upper:
                self._ghosts.append([atom[0], atom[1]-y_len, atom[2]])
                self._append_affine(i)
            if atom[2] < z_lower:
                self._ghosts.append([atom[0], atom[1], atom[2]+z_len])
                self._append_affine(i)
            if atom[2] > z_upper:
                self._ghosts.append([atom[0], atom[1], atom[2]-z_len])
                self._append_affine(i)

        self._atoms.extend(self._ghosts)


    def get(self) -> list[list[int, int, float, float, float]]:
        return self._atoms


    def delete_ghost(self) -> list[list[int, int, float, float, float]]:
        return self._atoms[0:len(self._atoms)-len(self._ghosts)]
    

    def adjust_neighbors(self, neighbors:list[list[int]]) -> list[list[int]]:
        n = 0
        for ii, i in enumerate(neighbors):
            for ij, j in enumerate(i):
                    n += 1
                    ghost = self._ghost_affine.get(j)
                    if ghost != None:
                        neighbors[ii][ij] = ghost

        return neighbors[0:len(self._atoms)-len(self._ghosts)]


    def _append_affine(self, i):
        self._ghost_affine.get(len(self._atoms)+len(self._ghosts)-1)
        self._ghost_affine[len(self._atoms)+len(self._ghosts)-1] = i
        # ghost = self._ghost_affine[str(len(self._atoms)+len(self._ghosts)-1)]
        # ghost = str(i)