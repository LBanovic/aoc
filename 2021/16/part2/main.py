import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

input_file = Path(sys.argv[1])
hexa_line = input_file.open().readlines()[0].strip()


def operation(aggregator: Callable) -> Callable:
    return lambda x: x[0] if len(x) == 1 else aggregator(x)


operations = [
    operation(sum),
    operation(math.prod),
    operation(min),
    operation(max),
    None,
    operation(lambda x: int(x[0] > x[1])),
    operation(lambda x: int(x[0] < x[1])),
    operation(lambda x: int(x[0] == x[1]))
]


@dataclass
class Packet:
    binary: str

    def __post_init__(self):
        self.packet_version = int(self.binary[:3], 2)
        self.type_id = int(self.binary[3:6], 2)
        self.subpackets = []
        if self.type_id == 4:  # Literal
            self.number = ''
            for i in range(6, len(self.binary), 5):
                string = self.binary[i:i + 5]
                self.number += string[1:]
                if string.startswith('0'):
                    break
            self.number = int(self.number, 2)
            self.stopping_index = i + 5
        else:
            self.length_type_id = int(self.binary[6])
            if self.length_type_id == 0:
                self.subpacket_length = int(self.binary[7:22], 2)
                self.stopping_index = 22
                while self.subpacket_length != self.stopping_index - 22:
                    self.subpackets.append(Packet(self.binary[self.stopping_index:]))
                    self.stopping_index += self.subpackets[-1].stopping_index
            else:
                self.subpacket_number = int(self.binary[7:18], 2)
                self.stopping_index = 18
                while len(self.subpackets) < self.subpacket_number:
                    self.subpackets.append(Packet(self.binary[self.stopping_index:]))
                    self.stopping_index += self.subpackets[-1].stopping_index

    def __repr__(self):
        return f'(type {self.type_id}, version {self.packet_version})'

    @property
    def value(self):
        if self.type_id == 4:
            return self.number
        else:
            x = [p.value for p in self.subpackets]
            return operations[self.type_id](x)

    def get_versions(self):
        versions = [self.packet_version]
        for subpacket in self.subpackets:
            versions += subpacket.get_versions()
        return versions


def parse_packet(hexa_str: str) -> Packet:
    binary = ''
    for ch in hexa_str:
        val = f'{(int(ch, 16)):04b}'
        binary += val
    return Packet(binary)


packet = parse_packet(hexa_line)
print(packet.value)
