"""
!!!Now only support one type!!!
"""
from src import CountNeighborsModifier, TypeCutoff
import matplotlib.pyplot as plt
import random

# file_path = "/mnt/data/fuzhao.1.xyz"  # 文件路径
# output_path = "/mnt/data/fuzhao.1.xyz"
file_path = "..."  # 文件路径
output_path = "..."
cutoff = 1.7            # 截断半径


from ovito.io import import_file, export_file
from ovito.modifiers import ColorCodingModifier

pipeline = import_file(file_path)
        

tc = TypeCutoff().set(1,1,cutoff)
pipeline.modifiers.append(CountNeighborsModifier(tc=tc, count_ring=True, count_many_member_ring=[6]))
pipeline.modifiers.append(ColorCodingModifier(
    property='Neighbors',
    gradient=ColorCodingModifier.Hot(),
    auto_adjust_range=False,
    start_value=0, end_value=5
))

export_file(data=pipeline, file=output_path+"_main", format="lammps/dump", columns=
            ["Particle Identifier", "Particle Type", "Position.X", "Position.Y", "Position.Z", "Color", "Neighbors", "AtomInHowMany6MemberRing"], 
            multiple_frames=False)

## Plot attribute
attributes:dict[str, list[str]] = {}
for i in range(len(pipeline.frames)):
    data = pipeline.compute(i)
    keys = data.attributes.keys()

    # add key to attributes
    for key in keys:
        v = attributes.get(key)
        if v == None:
            attributes[key] = [data.attributes[key]]
        else:
            attributes[key].append(data.attributes[key])
        

timestep = attributes['SourceFrame']

atom_in_three_six_ring = attributes['atom_in_three_six_ring']

atom_in_ring_and_sp =  attributes['atom_in_ring_and_sp']
atom_in_ring_and_sp2 = attributes['atom_in_ring_and_sp2']
atom_in_ring_and_sp3 = attributes['atom_in_ring_and_sp3']

atom_outside_ring_and_sp =  attributes['atom_outside_ring_and_sp']
atom_outside_ring_and_sp2 = attributes['atom_outside_ring_and_sp2']
atom_outside_ring_and_sp3 = attributes['atom_outside_ring_and_sp3']

# sort by timestep
# def swap_all(i):
#     swap(timestep, i)
#     swap(atom_in_three_six_ring, i)
#     swap(atom_in_ring_and_sp, i)
#     swap(atom_in_ring_and_sp2, i)
#     swap(atom_in_ring_and_sp3, i)
#     swap(atom_outside_ring_and_sp, i)
#     swap(atom_outside_ring_and_sp2, i)
#     swap(atom_outside_ring_and_sp3, i)

# def swap(l:list, i:int):
#     temp = l[i]
#     l[i] = l[i+1]
#     l[i+1] = temp

# while True:
#     ok = True
#     for i,v in enumerate(timestep):
#         if i != len(timestep) -1:
#             if v > timestep[i+1]:
#                 swap_all(i)
#                 ok = False
#     if ok:
#         break


fig, ax = plt.subplots()

ax.plot(timestep, atom_in_three_six_ring, color='b') # 蓝色

ax.plot(timestep, atom_in_ring_and_sp, color='g') # 绿色
ax.plot(timestep, atom_in_ring_and_sp2, color='r') # 红色
ax.plot(timestep, atom_in_ring_and_sp3, color='c') # 蓝绿色

ax.plot(timestep, atom_outside_ring_and_sp, color='m') # 品红
ax.plot(timestep, atom_outside_ring_and_sp2, color='y') # 黄
ax.plot(timestep, atom_outside_ring_and_sp3, color='k') # 黑


fig.savefig(output_path+"_main.png")