"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""

# Program tested on Python 3.11

# Ver    Date        Author               Comment
# v0.1   04.12.2022  Bartlomiej Duda      -


# This script reads all hashes generated by ObsCure 2 HOOK
# and it creates new list without any duplicates


from operator import attrgetter
from dataclasses import dataclass

from objects import HashDumpObject

print("Starting to remove duplicates...")
hash_dump = open("obscure_2_hash_dump.txt", "rt")  # file generated by Obscure 2 Hook
hash_objects_from_dump: list = []
crc_list: list = []
hash_list_without_duplicates: list = []
orig_list_counter: int = 0
new_list_counter: int = 0

# reading hashes from original file (generated by ObsCure 2 Hook)
for line in hash_dump:
    line_entry = line.split("\t")

    hash_dump_obj = HashDumpObject(
        crc=line_entry[0].split("=")[-1],
        path_length=int(line_entry[1].split("=")[-1]),
        file_path=line_entry[2].split("=")[-1].rstrip("\n"),
    )
    hash_objects_from_dump.append(hash_dump_obj)
    orig_list_counter += 1


# removing duplicates
for hash_object in hash_objects_from_dump:
    if hash_object.crc not in crc_list:
        hash_list_without_duplicates.append(hash_object)
        new_list_counter += 1
    crc_list.append(hash_object.crc)


# sorting final list (by CRC32 value)
hash_list_without_duplicates: list[HashDumpObject] = sorted(hash_list_without_duplicates, key=attrgetter('crc'))


output_file = open("hash_lists/obscure_2_hash_clean_list.txt", "wt")

for hash_clean_entry in hash_list_without_duplicates:
    out_line = hash_clean_entry.crc + "|||" + str(hash_clean_entry.path_length) + "|||" +  hash_clean_entry.file_path + "\n"
    output_file.write(out_line)


output_file.close()
hash_dump.close()

print("OLD hash count: ", orig_list_counter)
print("NEW hash count: ", new_list_counter)
print("HASH DUPLICATES REMOVED SUCCESSFULLY!")
