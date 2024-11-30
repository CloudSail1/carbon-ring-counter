import unittest
from src import CountNeighborsModifier, TypeCutoff

from ovito.io import import_file, export_file
from ovito.modifiers import ColorCodingModifier, ColorByTypeModifier
from ovito.data import DataCollection
import random
import numpy as np


class TestCountNeighbors(unittest.TestCase):
    def __init__(self, methodName = "runTest"):
        self.file_path = "..."
        self.cutoff = 1.7
        self.pipeline = import_file(self.file_path)
        self.output_path = "..." + "_c" + str(self.cutoff)
        super().__init__(methodName)


    def test_count_neighbors(self):
        self.pipeline.modifiers.clear()
        self.pipeline.modifiers.append(CountNeighborsModifier(
            TypeCutoff().set(1,1,cutoff=self.cutoff)
        ))
        self.pipeline.modifiers.append(ColorCodingModifier(
            property='Neighbors',
            gradient=ColorCodingModifier.Hot(),
            auto_adjust_range=False,
            start_value=0, end_value=5
        ))
        export_file(data=self.pipeline, file=self.output_path+"_onlyNeighbor", format="lammps/dump", columns=
                    ["Particle Identifier", "Particle Type", "Position.X", "Position.Y", "Position.Z", "Color", "Neighbors"], multiple_frames=True)


    # def test_count_multitype(self):
    #     self.pipeline.modifiers.clear()

    #     def gen_diffrent_type(frame, data:DataCollection):
    #         count = data.particles.count
    #         types = []
    #         for _ in range(count):
    #             types.append(random.choice([1,2]))
    #         types = np.array(types)
    #         data.particles_["Particle Type_"][...] = types

    #     self.pipeline.modifiers.append(gen_diffrent_type)
    #     self.pipeline.modifiers.append(CountNeighborsModifier(
    #         TypeCutoff().set(1,1,cutoff=self.cutoff).set(1,2,cutoff=self.cutoff).set(2,2,cutoff=10)
    #     ))
    #     self.pipeline.modifiers.append(ColorByTypeModifier())
    #     export_file(data=self.pipeline, file=self.output_path+"_multiType", format="lammps/dump", columns=
    #                 ["Particle Identifier", "Particle Type", "Position.X", "Position.Y", "Position.Z", "Color", "Neighbors"], multiple_frames=True)
        

    def test_count_six_member_ring(self):
        self.pipeline.modifiers.clear()
        self.pipeline.modifiers.append(CountNeighborsModifier(
            tc=TypeCutoff().set(1,1,cutoff=self.cutoff), count_ring=True, count_many_member_ring=[6]
        ))
        self.pipeline.modifiers.append(ColorCodingModifier(
            property='Neighbors',
            gradient=ColorCodingModifier.Hot(),
            auto_adjust_range=False,
            start_value=0, end_value=5
        ))

        data = self.pipeline.compute()
        self.assertIn("AtomInHowMany6MemberRing", list(data.particles.keys()))
        self.assertIn("total_number_of_atom_in_6_member_ring", data.attributes)

        export_file(data=self.pipeline, file=self.output_path+"_6mr", format="lammps/dump",
                    columns=["Particle Identifier", "Particle Type", "Position.X", "Position.Y", "Position.Z", "Color", "Neighbors", "AtomInHowMany6MemberRing"],
                    multiple_frames=True)
        

    def test_count_5_6_7_8_member_ring(self):
        self.pipeline.modifiers.clear()
        self.pipeline.modifiers.append(CountNeighborsModifier(
            tc=TypeCutoff().set(1,1,cutoff=self.cutoff), count_ring=True, count_many_member_ring=[5,6,7,8]
        ))
        self.pipeline.modifiers.append(ColorCodingModifier(
            property='Neighbors',
            gradient=ColorCodingModifier.Hot(),
            auto_adjust_range=False,
            start_value=0, end_value=5
        ))


        data = self.pipeline.compute()
        self.assertIn("AtomInHowMany5MemberRing", list(data.particles.keys()))
        self.assertIn("AtomInHowMany6MemberRing", list(data.particles.keys()))
        self.assertIn("AtomInHowMany7MemberRing", list(data.particles.keys()))
        self.assertIn("AtomInHowMany8MemberRing", list(data.particles.keys()))
        self.assertIn("total_number_of_atom_in_5_member_ring", data.attributes)
        self.assertIn("total_number_of_atom_in_6_member_ring", data.attributes)
        self.assertIn("total_number_of_atom_in_7_member_ring", data.attributes)
        self.assertIn("total_number_of_atom_in_8_member_ring", data.attributes)

        export_file(data=self.pipeline, file=self.output_path+"_5678mr", format="lammps/dump",
                    columns=["Particle Identifier", "Particle Type", "Position.X", "Position.Y", "Position.Z", "Color", "Neighbors", 
                             "AtomInHowMany5MemberRing", "AtomInHowMany6MemberRing", "AtomInHowMany7MemberRing", "AtomInHowMany8MemberRing"],
                    multiple_frames=True)
