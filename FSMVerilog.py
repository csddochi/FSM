# written by Charlotte, Yunho Kim
# make a state machine from .vcd file

class FSM:
    s_moduleName = ""
    dic_inputVal = {}
    li_states = []

    # print the header part of verilog file
    def printHeader(self, output):
        output.write("module " + self.s_moduleName + "(reset, clk, " + self.makeInputVarString() + ");\n")
        output.write("\tinput reset, clk, " + self.makeInputVarString() + ";\n")
        output.write("\tparameter " + self.makeStateString() + ";\n")
        output.write("\treg[16:0] state, nextState;\n\n") # change 1 bit into 16 bits

    # print the initialize part of verilog file
    def printInitialize(self, output):
        string = '\t' + 'always @(posedge clk) begin\n'
        string += '\t\t' + 'if(reset) begin\n'
        string += '\t\t\t' + 'state <= ' + self.li_states[0].s_name + ';\n'
        """
        string += '\t\t\t'
        for v in self.dic_inputVal.values():
            string = string + v + ' = 0, '
        string = string[:-2]
        """
        string += '\t\t' + 'end\n\t\t' + 'else begin\n'
        string += '\t\t\t' + 'state <= nextState;\n\t\t' + 'end\n\t'
        string += 'end\n\n'
        output.write(string)

    # print the state changes & transition part of verilog file
    def printTransition(self, output):
        output.write('\t' + 'always @(' + self.makeInputVarString() + ') begin\n\t\t' + 'case(state)\n')
        for i in range(0, len(self.li_states)):
            curState = self.li_states[i]
            if i == len(self.li_states) - 1:
                string = '\t\t' + curState.s_name + ' : begin\n\t\tend\n'
                output.write(string)

            else:
                string = '\t\t' + curState.s_name + ' : begin\n'
                string += '\t\t\tif('

                # if phrase
                for trans in curState.li_transitions:
                    for key in trans.dic_tranValue.keys():
                        string += key + ' == ' + trans.dic_tranValue[key] + ' && '
                string = string[:-4]

                string += ') nextState <= ' + self.li_states[i + 1].s_name + ';\n'
                
                """ # for comments
                # else if phrase
                if i is not 0:
                    prior = self.li_states[i - 1]
                    string += '\t\t\telse if('

                    for trans in prior.li_transitions:
                        for key in trans.dic_tranValue.keys():
                            string += key + ' == ' + trans.dic_tranValue[key] + ' && '
                    string = string[:-4]
                    string += ') nextState <= ' + self.li_states[i].s_name + ';\n'
                """ 
                string += "\t\t\telse nextState <= s1;\n"
                string += '\t\t' + 'end\n'
                output.write(string)
            curState.printState()

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

    def setTransition(self, valDic, d):
        self.li_transitions.append(Transition(valDic, d))

    def printState(self):
        print("STATE : " + self.s_name + "\t\tOccurrence time : " + self.i_value + "ps")
        for t in self.li_transitions:
            t.printTransitionInfo()
        if len(self.li_transitions) == 0:
            print("\tThis is the end state\n")
        else:
            print("\telse if neither variables change")
            print("\t\t--> Next State is " + self.s_name)
            print("\telse Next state is s1\n")


class Transition:
    # s_variable = ""
    # s_value = '0'
    dic_tranValue = {}
    s_dest = ""

    def __init__(self, dic, d):
        self.dic_tranValue = dic
        self.s_dest = d

    def printTransitionInfo(self):
        string = "\tif "
        for k in self.dic_tranValue.keys():
            string += k + " changes to " + self.dic_tranValue[k] + " and "
        string = string[:-4]
        print(string + "\n\t\t--> Next State is " + self.s_dest)


# set FSM class
def setFSM(lines, fsm):
    idx = 1
    stat = 0
    beforeStat = 0
    isVarSetting = 0
    tempdic = {}

    for line in lines:
        if line[0] == '$':
            line = line[1:]
            words = line.split()

            # read module name and original value names at .vcd and write on the FSM class
            if words[0] == 'scope':
                fsm.setModuleName(words[2])
            elif words[0] == 'var' and words[1] == 'reg':
                print(words[4], "is assigned to", words[3])
                fsm.setInputValue(words[3], words[4])
            else:
                """nothing"""
        # set first state(s1) information
        elif line[0] == '#':
            if isVarSetting == 1:
                beforeStat.setTransition(tempdic, "s" + str(idx - 1))
                fsm.setState(beforeStat)
                isVarSetting = 0
            tempdic = {}
            time = line[1:-1]
            beforeStat = stat
            stat = State("s" + str(idx), time)

            idx += 1
            if time != "0":
                isVarSetting = 1
        elif isVarSetting == 1:
            # go to the next line and set the transitions information
            value = line[0]
            var = fsm.getInputVal(line[1])
            tempdic[var] = value
    beforeStat.setTransition(tempdic, "s" + str(idx - 1))
    fsm.setState(beforeStat)

    fsm.setState(stat)
    return fsm


if __name__ == "__main__":
    rf = open("test2.vcd", "r")
    wf = open("output.v", "w")
    fsm = FSM()

    lines = rf.readlines()
    lines = lines[10:]
    fsm = setFSM(lines, fsm)
    print("FSM created\n")

    fsm.printHeader(wf)
    fsm.printInitialize(wf)
    fsm.printTransition(wf)

    rf.close()
wf.close()
