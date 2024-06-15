import gdb
import hashlib

####################
# Utiliti Function
####################

def ReadMemory(addr, length):
    data = gdb.inferiors()[0].read_memory(addr, length).tobytes()
    return data

def GetIntVariable(var):
    return int(gdb.parse_and_eval(var))

def GetStrVariable(var):
    return str(gdb.parse_and_eval(var))

def HashStringArray(string_array, algorithm="sha256"):
    hasher = hashlib.new(algorithm)
    for string in string_array:
        hasher.update(string.encode('utf-8'))
    return hasher.hexdigest()

def GetCallStack():
    stack = []
    frame = gdb.newest_frame()
    while frame is not None:
        stack.append('??' if frame.name() is None else frame.name())
        frame = frame.older()
    return stack, HashStringArray(stack)

##########################
# Custom Breakpoint Class
##########################

addr2Size = {}
addr2Stkid = {}
stkidInfo = {}

class FuncFinishBP(gdb.FinishBreakpoint):
    def __init__ (self, function_entry_info):
        gdb.FinishBreakpoint.__init__(self, gdb.newest_frame(), internal=True)
        self.function_entry_info = function_entry_info

    def GetIntRet(self):
        return int(self.return_value)

    def GetStrRet(self):
        return str(self.return_value)

    def stop(self):
        global addr2Size
        global addr2Stkid
        global stkidInfo
        malloc_addr = self.GetIntRet()
        malloc_bytes, stack, stack_id = self.function_entry_info
        addr2Size[malloc_addr] = malloc_bytes
        addr2Stkid[malloc_addr] = stack_id
        if stack_id not in stkidInfo:
            stkidInfo[stack_id] = [stack, 0]
        stkidInfo[stack_id][1] += malloc_bytes
        return False

class MallocBP(gdb.Breakpoint):
    def __init__(self):
        super(MallocBP, self).__init__('malloc', gdb.BP_BREAKPOINT)

    def stop(self):
        malloc_bytes = GetIntVariable('bytes')
        stack, stack_id = GetCallStack()
        FuncFinishBP((malloc_bytes, stack, stack_id))
        return False

class FreeBP(gdb.Breakpoint):
    def __init__(self):
        super(FreeBP, self).__init__('free', gdb.BP_BREAKPOINT)

    def stop(self):
        global addr2Size
        global stkidInfo
        global addr2Stkid
        free_addr = GetIntVariable('mem')
        try:
            free_bytes = addr2Size[free_addr]
            stkid = addr2Stkid[free_addr]
            stkidInfo[stkid][1] -= free_bytes
        except:
            print(f"WARN: free_addr:{free_addr}")
        return False

############################
# Custom GDB Command
############################
class DumpData(gdb.Command):
    def __init__(self):
        super(DumpData, self).__init__("dump", gdb.COMMAND_DATA)

    def invoke(self, arguments, from_tty):
        for _, t in stkidInfo.items():
            print(f"===== live bytes:{t[1]} =====")
            for cur in t[0]:
                print(cur)

class ReaderM(gdb.Command):
    def __init__(self):
        super(ReaderM, self).__init__("rdm", gdb.COMMAND_DATA)

    def invoke(self, arguments, from_tty):
        args = gdb.string_to_argv(arguments)
        ReadMemory(int(args[0], 16), int(args[1]))


############################
# Pretty Printer Class
############################
class PointPrinter:
    def __init__(self, val):
        self.val = val
    def to_string(self):
        return "x:{} y:{}".format(self.val['x'], self.val['y'])

def LookupPrettyPrinter(val):
    if val.type.tag == "Point":
        return PointPrinter(val)
    return None


def main():
    # create breakpointes
    MallocBP()
    FreeBP()

    # register custom command
    DumpData()
    ReaderM()

    # register pretty printer
    gdb.printing.register_pretty_printer(
        gdb.current_objfile(),
        LookupPrettyPrinter, replace=True)
    
    gdb.execute("r")

main()
