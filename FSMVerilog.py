# written by Charlotte
# to make Verilog file from VCD format

vcd_p = dict()  # parameters in VCD format
pairs = {}
dataParse = 0
string = ""  # to write Verilog file

rf = open("tt_mod.vcd", 'r')
lines = rf.readlines()
lines = lines[10:]


class FSM:
    reset = "reset"
    clock = "clk"
    variables = []
    parameters = list()  # states' list

    def __init__(self, var):
        self.variables = [v for v in var]

    def addState(self, state):
        self.parameters.append(state)


class Transitions:  # I don't know this application.
    inputNum = 0  # input
    outputNm = 0  # output
    typeName = ""  # SDA or SCL

    def __init__(self, i, o, t):
        self.inputNum = i
        self.outputNm = o
        self.typeName = t


class State:
    sttName = ""
    varName = ""
    vrValue = 0  # default is zero, [0, 1]
    varTime = 0

    def __init__(self, s, n, v, t):
        self.sttName = s
        self.varName = n
        self.vrValue = v
        self.varTime = t

    def toString(self):
        temp = "state name is %s, " % self.sttName
        temp = temp + "name is %s, " % self.varName
        temp = temp + "value is %d " % int(self.vrValue)
        temp = temp + "and time is %d." % int(self.varTime)
        return temp


if __name__ == "__main__":

    for line in lines:
        words = line.split()
        if '$var' in words:

            # ignore 'scope'

            if words[1] == 'reg':
                vcd_p[words[3]] = words[4]  # insert dictionary

    fsm = FSM(vcd_p.values())  # create Finite State Machine

    # first line in Verilog file
    string = string + 'module FSM(' + fsm.reset + ', ' + fsm.clock + ', '
    for v in fsm.variables:
        string = string + v + ', '
    string = string[:-2]  # delete last ', '
    string = string + ');\n'

    # second line in Verilog file
    string = string + '\t' + 'input ' + fsm.reset + ', ' + fsm.clock + ', '
    for v in fsm.variables:
        string = string + v + ', '
    string = string[:-2]  # delete last ', '
    string = string + ';\n'

    # add state in Finite State Machine
    state = State('a', fsm.variables, 0, 0)  # initialize
    fsm.addState(state)

    i = 1
    for line in lines:
        if line[0] is '#':
            time = line[1:-1]
            if time is not '0':
                dataParse = 1
            continue
        if dataParse == 1:
            value = line[0]
            var = vcd_p[line[1]]
            state = State(chr(ord('a') + i), var, value, time)
            i = i + 1
            fsm.addState(state)
            dataParse = 0

    # third line in Verilog file
    string = string + '\t' + 'parameter '
    for p in fsm.parameters:
        string = string + p.sttName + '=' + str(p.varTime) + ', '
    string = string[:-2] + ';\n'

    # forth line in Verilog file
    string = string + '\t' + 'reg [1:0] state, nextState;\n\n'

    # add initializing part
    string = string + '\t' + 'always @(posedge ' + fsm.clock + ') begin' + '\n'
    string = string + '\t\t' + 'if(' + fsm.reset + ') begin' + '\n'
    string = string + '\t\t\t' + 'state <= ' + fsm.parameters[0].sttName + ';\n'
    string = string + '\t\t\t'
    for v in fsm.variables:
        string = string + v + '=0, '
    string = string[:-2]  # delete last ', '
    string = string + ';\n\t\t' + 'end\n\t\t' + 'else begin\n'
    string = string + '\t\t\t' + 'state <= nextState;\n\t\t' + 'end\n\t'
    string = string + 'end\n\n'

    # loop according to state
    string = string + '\t' + 'always @('
    for v in fsm.variables:
        string = string + v + ', '
    string = string[:-2]  # delete last ', '
    string = string + ') begin\n\t\t' + 'case(state)\n'
    for i in range(1, len(fsm.parameters)):
        string = string + '\t\t' + fsm.parameters[i - 1].sttName + ' : begin\n'
        string = string + '\t\t\t' + 'if(' + fsm.parameters[i].varName
        string = string + ' == ' + str(fsm.parameters[i].vrValue) + ') '
        string = string + 'nextState <= ' + fsm.parameters[i].sttName + ';\n'
        string = string + '\t\t' + 'end\n'

    string = string + '\t\t' + 'endcase\n\t' + 'end\n' + 'endmodule'

with open("output.v", 'w') as wf:
    wf.write(string)





