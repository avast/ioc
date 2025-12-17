import idc
import idaapi

start = <address_start>
end = <address_end>

for ea in range(start, end, 4):
    idc.SetType(ea, "const __int32")
    idaapi.set_op_type(ea, idaapi.num_flag(), idaapi.OPND_ALL)