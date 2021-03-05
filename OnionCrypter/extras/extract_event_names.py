import idautils
import idc

def find_event_names():
	event_names = []
	#get address value of named address
	offset_name = 'CreateEventA'
	named_addr = ida_name.get_name_ea(BADADDR, offset_name)

	#get all unique xrefs to found named address
	xref_lst = []
	for xref in idautils.XrefsTo(named_addr):
		if xref.frm not in xref_lst:
			xref_lst.append(xref.frm)

	#get addresses where arguments of called function are pushed
	for xref in xref_lst:
		args = idaapi.get_arg_addrs(xref)

		if idc.get_operand_type(args[3], 0) == idaapi.o_imm:
	#		select last argument and read string to which it points
			op_val = idc.get_operand_value(args[3], 0)
			event_name = get_strlit_contents(op_val)
			if event_name != None :
				event_name = event_name.decode('ascii')
				event_names.append(event_name)

	return event_names

def store_results(event_names, result_file):
	with open(result_file, 'a') as f:
		sample_name = get_input_file_path().split("\\")
		sample_name = sample_name[-1].split('.')[0]

		event_names = [ f'"{x}"' for x in event_names]
		out_ndjson = f'{{"{sample_name}" : [{", ".join(event_names)}]}}\n'
		f.write(out_ndjson)

def main():
	if len(idc.ARGV) < 1:
		return

	ida_auto.auto_wait()
	event_names = find_event_names()
	store_results(event_names, idc.ARGV[1])
	ida_pro.qexit(0)

main()
