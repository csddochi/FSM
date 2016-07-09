# written by Charlotte
# for read and parse vcd file format

class FSM:
    s_moduleName = ""
    dic_inputVal = {}
    li_states = []

    #print the header part of verilog file
    def printHeader(self, output):
        output.write("module " + self.s_moduleName + "(reset, clk, " + self.makeInputVarString() + ");\n")
        output.write("\tinput reset, clk, " + self.makeInputVarString() + ";\n")
        output.write("\tparameter " + self.makeStateString() + ";\n")
        output.write("\treg[1:0] state, nextState;\n\n")

    # print the initialize part of verilog file
    def printInitialize(self, output):
        string = '\t' + 'always @(posedge clk) begin\n'
        string += '\t\t' + 'if(reset) begin\n'
        string += '\t\t\t' + 'state <= ' + self.li_states[0].s_name + ';\n'
        string += '\t\t\t'
        for v in self.dic_inputVal.values():
            string = string + v + ' = 0, '
        string = string[:-2]
        string += ';\n\t\t' + 'end\n\t\t' + 'else begin\n'
        string += '\t\t\t' + 'state <= nextState;\n\t\t' + 'end\n\t'
        string += 'end\n\n'
        output.write(string)

    # print the state changes & transition part of verilog file
    def printTransition(self, output):
        output.write('\t' + 'always @(' + self.makeInputVarString() + ') begin\n\t\t' + 'case(state)\n')
        for i in range(1, len(self.li_states)):
            curState = self.li_states[i]
            string = '\t\t' + self.li_states[i-1].s_name + ' : begin\n'
            string += '\t\t\t' + 'if(' + curState.li_transitions[0].s_variable + ' == ' + curState.li_transitions[0].s_value + ') '
            string += 'nextState <= ' + curState.s_name + ';\n'
            string +='\t\t' + 'end\n'
            output.write(string)

        output.write('\t\t' + 'endcase\n\t' + 'end\n' + 'endmodule')

    # make the input value string (e.g. i1, i2, i3)
    def makeInputVarString(self):
        s = ""
        for v in self.dic_inputVal.values():
            s += (v + ", ")
        s = s[:-2]
        return s

    # make the state string (e.g. s1 = 0, s2 = 10, s3 = 30)
    def makeStateString(self):
        s = ""
        for state in self.li_states:
            s += (state.s_name + " = " + state.i_value + ", ")
        s = s[:-2]
        return s

    # getters and setters
    def setModuleName(self, n):
        self.s_moduleName = n

    def setInputValue(self, k, v):
        self.dic_inputVal[k] = v

    def setState(self, s):
        self.li_states.append(s)

    def getInputVal(self, k):
        return self.dic_inputVal[k]


class State:
    s_name = ""
    i_value = 0
    li_transitions = []

    def __init__(self, n, t):
        self.s_name = n
        self.i_value = t
        self.li_transitions = []

    def setTransition(self, var, val):
        self.li_transitions.append(Transition(var, val))


class Transition:
    s_variable = ""
    s_value = '0'
    #s_dest = ""

    def __init__(self, var, val):
        self.s_variable = var
        self.s_value = val
        #self.s_dest = d


# set FSM class
def setFSM(lines, fsm):
    idx = 2
    linesIdx = 0

    while linesIdx != len(lines):
        line = lines[linesIdx]
        linesIdx += 1

        if line[0] == '$':
            line = line[1:]
            words = line.split()

            if words[0] == 'scope':
                fsm.setModuleName(words[2])

            elif words[0] == 'var' and words[1] == 'reg':
                print(words[4], "is assigned to", words[3])
                fsm.setInputValue(words[3], words[4])
            else:
                """nothing"""

        if line[0] == '#' and line[1] == '0':
            stat = State("s1", '0')
            for v in fsm.dic_inputVal.values():
                stat.setTransition(v, '0')
            fsm.setState(stat)

        elif line[0] == '#':
            time = line[1:-1]
            stat = State("s" + str(idx), time)
            idx += 1

            # go to the next line
            line = lines[linesIdx]
            linesIdx += 1

            value = line[0]
            var = fsm.getInputVal(line[1])
            print(var + " changes to " + value + " in " + time + "ps")
            stat.setTransition(var, value)
            fsm.setState(stat)
    return fsm



if __name__ == "__main__":
    rf = open("test.vcd", "r")
    wf = open("output.v", "w")
    fsm = FSM()

    lines = rf.readlines()
    lines = lines[10:]
    fsm = setFSM(lines, fsm)

    fsm.printHeader(wf)
    fsm.printInitialize(wf)
    fsm.printTransition(wf)

    print("done")

    rf.close()
    wf.close()





