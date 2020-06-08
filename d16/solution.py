import re


class VirtualMachine:
    def __init__(self):
        self.registers = [0 for _ in range(4)]

    def addr(self, a, b, c):
        self.registers[c] = self.registers[a] + self.registers[b]

    def addi(self, a, b, c):
        self.registers[c] = self.registers[a] + b

    def mulr(self, a, b, c):
        self.registers[c] = self.registers[a] * self.registers[b]

    def muli(self, a, b, c):
        self.registers[c] = self.registers[a] * b

    def banr(self, a, b, c):
        self.registers[c] = self.registers[a] & self.registers[b]

    def bani(self, a, b, c):
        self.registers[c] = self.registers[a] & b

    def borr(self, a, b, c):
        self.registers[c] = self.registers[a] | self.registers[b]

    def bori(self, a, b, c):
        self.registers[c] = self.registers[a] | b

    def setr(self, a, b, c):
        self.registers[c] = self.registers[a]

    def seti(self, a, b, c):
        self.registers[c] = a

    def gtir(self, a, b, c):
        self.registers[c] = 1 if a > self.registers[b] else 0

    def gtri(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] > b else 0

    def gtrr(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] > self.registers[b] else 0
    
    def eqir(self, a, b, c):
        self.registers[c] = 1 if a == self.registers[b] else 0

    def eqri(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] == b else 0

    def eqrr(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] == self.registers[b] else 0


def analyze_samples(samples):
    operations = [VirtualMachine.addr, VirtualMachine.addi,
                  VirtualMachine.mulr, VirtualMachine.muli,
                  VirtualMachine.banr, VirtualMachine.bani,
                  VirtualMachine.borr, VirtualMachine.bori,
                  VirtualMachine.setr, VirtualMachine.seti,
                  VirtualMachine.gtir, VirtualMachine.gtri, VirtualMachine.gtrr,
                  VirtualMachine.eqir, VirtualMachine.eqri, VirtualMachine.eqrr]
    vm = VirtualMachine()
    results = []
    for before, (opcode, a, b, c), after in samples:
        matches = set()
        for operation in operations:
            vm.registers = before.copy()
            operation(vm, a, b, c)
            if all(actual == expected for actual, expected in zip(vm.registers, after)):
                matches.add(operation)
        results.append((opcode, matches))
    return results


def identify_operations(results):
    possible_mappings = {}
    for i in range(16):
        for opcode, matches in results:
            if opcode == i:
                if not i in possible_mappings:
                    possible_mappings[i] = matches.copy()
                else:
                    possible_mappings[i].intersection(matches)
    operations = {}
    while len(operations) < 16:
        opcode, operation = next((opcode, matches.pop())
                                 for opcode, matches in possible_mappings.items()
                                 if len(matches) == 1)
        operations[opcode] = operation
        del possible_mappings[opcode]
        for _, matches in possible_mappings.items():
            matches.discard(operation)
    return operations


def execute(program, operations):
    vm = VirtualMachine()
    for opcode, a, b, c in program:
        operations[opcode](vm, a, b, c)
    return vm.registers[0]


if __name__ == "__main__":
    with open('input.txt') as file:
        content = file.read()
    sections = content.split('\n\n\n\n', 1)

    regex = re.compile(r'[BeforeAfter\[,\]\n]|(: +)')
    samples = [tuple([int(number) for number in regex.sub('', line).split()]
                     for line in sample.splitlines())
               for sample in sections[0].split('\n\n')]
    results = analyze_samples(samples)
    print(sum(1 for _, matches in results if len(matches) >= 3))

    operations = identify_operations(results)
    program = [tuple(int(number) for number in line.strip().split())
               for line in sections[1].splitlines()]
    print(execute(program, operations))