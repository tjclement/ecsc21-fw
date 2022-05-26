import display, easydraw, flags

def solve(program):
    # solution = ">[-]>[-]<,+>>[-]<<[->>+<<]>>[[-<<+>>]<<->>]>[-]>[-]<<<<[->>>>+<<<<]>>>>[-<+<<<+>>>>][-]<<[-]>>>[-]>[-]<<<[->>>+<<<]>>>[[-<<<+>>>]>[-]<<<[->>>+<<<]>>>[[-<<<+>>>]<<[-]+>>]<]<[<<->->[-]>[-]<<<[->>>+<<<]>>>[[-<<<+>>>]>[-]<<<[->>>+<<<]>>>[[-<<<+>>>]<<[-]+>>]<]<][-]<<[->>+<<]>>[[-<<+>>]<<<[-]+>>>][-]<[->+<]>[[-<+>]<<<[-]+>>>]<<<[>[-]<<<[->>>+<<<]>>>[-<<<+>+>>]<<<,+>>>[-]<<<[->>>+<<<]>>>[[-<<<+>>>]<<<->>>][-]>[-]<<<<[->>>>+<<<<]>>>>[-<+<<<+>>>>][-]<<[-]>>>[-]>[-]<<<[->>>+<<<]>>>[[-<<<+>>>]>[-]<<<[->>>+<<<]>>>[[-<<<+>>>]<<[-]+>>]<]<[<<->->[-]>[-]<<<[->>>+<<<]>>>[[-<<<+>>>]>[-]<<<[->>>+<<<]>>>[[-<<<+>>>]<<[-]+>>]<]<][-]<<[->>+<<]>>[[-<<+>>]<<<[-]+>>>][-]<[->+<]>[[-<+>]<<<[-]+>>>]<<<]<.>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    import esp, gc
    solution_program = program
    class Membrain(object):
        DATA_SIZE = 250
        ALPHABET = '+-,.[]<>'
        REPEATABLE = '+-<>'
        CLEAR_CMD = 'C'
        def __init__(self, program: str):
            self.program, self.dataspots = self.__preprocess_program(program)
            self.looptargets = self.__validate_loops(self.program)
            self.data = bytearray(self.DATA_SIZE)
            self.stepcount = 0
            gc.collect()

        def run(self, input, output, maxsteps=1000):
            self.__reset(input, output)
            try:
                while True:
                    self.__step()
                    if (self.stepcount > maxsteps):
                        return False
            except StopIteration:
                pass
            return True

        def __step(self):
            if self.ip >= len(self.program):
                raise StopIteration('Reached the end of the program')
            command = self.program[self.ip]
            optimized = self.dataspots.get(self.ip, (command, 1, 1))
            command, count, ipdist = optimized
            self.ip += ipdist
            if command == self.CLEAR_CMD:
                # Clear command
                self.__write_data(0)
            else:
                routine = self.__TRANSITION_MAP[command]
                routine(self, command, count)
            if (self.stepcount % 100) == 0:
                # FIXME: this doesn't suppress the WDT reset messages
                # Feed the watchdog
                esp.wdt_reset()
            self.stepcount += 1
        
        def __reset(self, input, output):
            self.outbuf = output
            self.inpbuf = input
            self.input_idx = 0
            self.output_idx = 0
            self.ip = 0
            self.dp = 0
            self.stepcount = 0

        def __preprocess_program(self, program: str):
            ds = {}
            i = 0
            while i < len(program):
                p = program[i]
                if p not in self.ALPHABET:
                    raise ValueError('Illegal program. Unknown command: %s' % p)
                if p == '[':
                    if i + 2 < len(program):
                        if program[i+1] == '-' and program[i+2] == ']':
                            # Cache the clear subpattern to simplify processing
                            ds[i] = (self.CLEAR_CMD, 0, 3)
                if p in self.REPEATABLE:
                    location = i
                    while i < len(program) and p == program[i]:
                        i += 1
                    distance = (i - location)
                    if distance >= 5:
                        ds[location] = (p, distance, distance)
                        continue
                    else:
                        i = location
                i += 1
            return program, ds

        def __validate_loops(self, program: str):
            loopstack = []
            looptargets = {}
            for i in range(len(program)):
                p = program[i]
                if p == '[':
                    loopstack.append(i)
                elif p == ']':
                    if not loopstack:
                        raise ValueError('Illegal program: unmatched loop end marker')
                    initial = loopstack.pop()
                    looptargets[initial] = i
                    looptargets[i] = initial
                else:
                    pass
            if loopstack:
                raise ValueError('Illegal program: unmatched loop start marker')
            return looptargets

        def __validate_mem_ptr(self):
            if self.dp >= len(self.data):
                raise ValueError('Invalid state: data overflow')
            if self.dp < 0:
                raise ValueError('Invalid state: data underflow')

        def __write_data(self, d):
            self.data[self.dp] = d

        def __read_data(self):
            return self.data[self.dp]

        def __io_transition(self, command, count=1):
            if command == ',':
                if self.input_idx >= len(self.inpbuf):
                    raise ValueError('Invalid state: input buffer overread')
                d = self.inpbuf[self.input_idx]
                self.input_idx += 1
                self.__write_data(d)
            elif command == '.':
                if self.output_idx >= len(self.outbuf):
                    raise ValueError('Invalid state: output buffer overflow')
                self.outbuf[self.output_idx] = self.__read_data()
                self.output_idx += 1
            else:
                raise ValueError('Invalid state: instruction command not matching routine')

        def __dp_transition(self, command, count=1):
            if command == '>':
                self.dp += count
            elif command == '<':
                self.dp -= count
            else:
                raise ValueError('Invalid state: instruction command not matching routine')
            self.__validate_mem_ptr()

        def __arith_transition(self, command, count=1):
            d = self.__read_data()
            if command == '+':
                self.__write_data((d + count) & 0xFF)
            elif command == '-':
                self.__write_data((d - count) & 0xFF)
            else:
                raise ValueError('Invalid state: instruction command not matching routine')

        def __ip_transition(self, command, count=1):
            d = self.__read_data()
            cur_ip = self.ip - 1
            if command == '[':
                if d == 0:
                    self.ip = self.looptargets[cur_ip] + 1
            elif command == ']':
                if d != 0:
                    self.ip = self.looptargets[cur_ip] + 1
            else:
                raise ValueError('Invalid state: instruction command not matching routine')

        __TRANSITION_MAP = {
            '.': __io_transition,
            ',': __io_transition,
            '>': __dp_transition,
            '<': __dp_transition,
            '+': __arith_transition,
            '-': __arith_transition,
            '[': __ip_transition,
            ']': __ip_transition
        }
    
    # NOTICE: quite slow to emulate BF
    # on something like the ESP. So keep it
    # very simple!
    inputs = [
        bytes([4, 3, 0]),
        bytes([2, 1, 0]),
        bytes([9, 101, 25, 0]),
        bytes([10, 13, 17, 21, 0])
    ]
    answers = [
        7,
        3,
        135,
        61
    ]
    output = bytearray(100)
    print("Running in the Membrain. This may take a couple of minutes..")
    solutions = []

    try:
        interpreter = Membrain(solution_program)
        for i in range(len(inputs)):
            if not interpreter.run(input=inputs[i], output=output, maxsteps=50000):
                raise ValueError('Your program took too long!')
            solutions.append(output[0])
    except ValueError as e:
        print('Something went wrong: ', end='')
        print(e.args[0])
        return

    same = True
    for i in range(len(answers)):
        if solutions[i] != answers[i]:
            same = False
            break
    if same:
        flag = 'CTF{%s}' % '771bce26ac7b238bbb6220cd795501d2f547a3ba1ca235f1'
        print('Sequence pass! Here is the flag: %s' % flag)
        flags.submit_flag(flag)
    else:
        print('Incorrect sequence. Please try again.')

_message_ui = 'You must know about our BrainSuck language, so prove that you know how to use it.\n' + \
        'Provide a program according to the specifications shown in your terminal.\n\n' + \
        'You can paste snippets using CTRL+E and CTRL+D.\n\n' + \
        'You can submit the flag by calling flags.submit_flag("CTF{xxxx}").'

_message_console = 'Call solve(program="><[]+-,.") to provide a BrainSuck program\n' + \
        'that can add sequences of bytes that end in a null byte. For example:\n\n' + \
        'Input (hex): "010200". Output (hex): "03"\n' + \
        'Inputs and outputs are treated as byte values - not ASCII and not hex-encoded\n\n'

display.drawFill(0x0)
easydraw.messageCentered('Insane in the Membrain\n\n\n' + _message_ui)


def help():
    print(_message_console)

help()
