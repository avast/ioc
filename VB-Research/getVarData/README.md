We have two interlinked functions in this example.

The C host sets a global variable used as a for loop maxCount
and implements two callbacks:

* __mMsgbox__ prints a string message to the console
* __getData__ returns a variant back to the vb pcode 

Type based on numeric arg passed in.

```
output:
------------------------------------
getData(0)
string callback: 0 TypeName(v) = String
string callback: Value = this is my string
getData(1)
string callback: 1 TypeName(v) = Byte()
string callback: Ubound: 19
string callback: Value = AAAAAAAAAAAAAAAAAAAA
getData(2)
string callback: 2 TypeName(v) = Date
string callback: Value = 3/18/2014 9:24:57 PM
getData(3)
string callback: 3 TypeName(v) = Long
string callback: Value = 32

Press any key to exit...
```