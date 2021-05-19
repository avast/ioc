This sample shows how to:
* embed binary strings in the constant pool
* decode them in pcode with an xor key given as an arg to the function
* do C call backs
* modify data in a c callback for use in the pcode
* return values both from callbacks, and from the pcode function itself

This one has been simplified from v1 to eliminate the copymemory call 
and the CStr2Vec pcode function to convert a binary string from the const pool
into a byte array.

