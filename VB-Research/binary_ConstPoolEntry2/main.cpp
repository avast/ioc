
#include <windows.h>
#include <stdio.h>
#include <conio.h>

/*
output:
	Launching pcode
	in progress value = 55                <-- xor key passed into vb pcode as func arg
	in progress value = 12                <-- ubound binary byte array from string
	in callback cstr = this is my string  <-- cstr from decoded binary str in c callback
	in progress value = 41				  <-- first byte of string passed to callback modifed
	retval = 43                           <-- return value from progress callback (val+2)

 */ 

unsigned char pcode[] = {
	0x6C, 0x0C, 0x00, 0xFC, 0x0E, 0x0A, 0x00, 0x00, 0x04, 0x00, 0x3C, 0x1B, 0x01, 0x00, 0xFC, 0x5F, 
	0x6C, 0xFF, 0x04, 0x6C, 0xFF, 0x04, 0x74, 0xFF, 0xFF, 0x01, 0x6C, 0x74, 0xFF, 0xF4, 0x01, 0xFC, 
	0xCB, 0xFC, 0x0E, 0x0A, 0x00, 0x00, 0x04, 0x00, 0x3C, 0xF5, 0x00, 0x00, 0x00, 0x00, 0x04, 0x70, 
	0xFF, 0x6C, 0x74, 0xFF, 0xF4, 0x01, 0xFC, 0xCB, 0xFE, 0x64, 0x64, 0xFF, 0x5E, 0x00, 0x6C, 0x70, 
	0xFF, 0x6C, 0x74, 0xFF, 0xFC, 0x90, 0xE7, 0x6C, 0x0C, 0x00, 0xFB, 0x13, 0xFC, 0x0E, 0x6C, 0x70, 
	0xFF, 0x6C, 0x74, 0xFF, 0xFC, 0xA0, 0x04, 0x70, 0xFF, 0x66, 0x64, 0xFF, 0x3E, 0x00, 0xF5, 0x00, 
	0x00, 0x00, 0x00, 0x6C, 0x74, 0xFF, 0x2E, 0x60, 0xFF, 0x40, 0x0A, 0x02, 0x00, 0x04, 0x00, 0x3C, 
	0x2D, 0x60, 0xFF, 0xF5, 0x00, 0x00, 0x00, 0x00, 0x6C, 0x74, 0xFF, 0xFC, 0x90, 0x5E, 0x00, 0x00, 
	0x04, 0x00, 0x71, 0x5C, 0xFF, 0x3C, 0x6C, 0x5C, 0xFF, 0x71, 0x78, 0xFF, 0x14, 0x00, 0x00, 0x00, 
	0x98, 0x10, 0x40, 0x00, 0x08, 0x00, 0x20, 0x00, 0x90, 0x00, 0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x19, 0x00, 0x00, 0x00, 0x00, 0x00, 0x16, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x74, 0xFF, 0x05, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x1A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x60, 0xFF, 0x06, 0x00, 
	0x6C, 0xFF, 0x05, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xE9, 0xE9, 0xE9, 0xE9, 
	0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0x9E, 0x9E, 0x9E, 0x9E
};


struct ObjectTable{
    int lNull1;	            // As Long      ' 0x00 (00d)
    int aExecProj;			// As Long      ' 0x04 (04d) Pointer to a memory structure
    int aProjectInfo2;		// As Long      ' 0x08 (08d) Pointer to Project Info 2
    int Const1;				// As Long      ' 0x0C
    int  Null2;				// As Long      ' 0x10
    int lpProjectObject;	// As Long      ' 0x14
    char uuidObj[15];		// As Byte      'converted from 4 flags dzzie (from vb.idc)
    short fCompileType;		// As Integer   ' 0x28 (40d) Internal flag used during compilation
    short ObjectCount1;		// As Integer   ' 0x2A
    short iCompiledObjects; // As Integer   ' 0x2C (44d) Number of objects compiled.
    short iObjectsInUse;	// As Integer   ' 0x2E (46d) Updated in the IDE to correspond the total number ' but will go up or down when initializing/unloading modules.
    int lpObjectArray;		// As Long      ' 0x30
    int fIdeFlag;			// As Long      ' 0x34
    int lpIdeData;			// As Long      ' 0x38
    int lpIdeData2;			// As Long      ' 0x3C
    int aProjectName;		// As Long      ' 0x40      NTS
    int LangID1;			//  As Long     ' 0x44
    int LangID2;			//  As Long     ' 0x48
    int lpIdeData3;			//  As Long     ' 0x4C
    int dwIdentifier;	    //  As Long     ' 0x50
};

struct CodeObject{
    int aObjectInfo;	//	As Long         ' 0x00  Pointer to the Object Info for this Object.
    int Const1;		    //	As Long         ' 0x04  Always set to -1 after compiling.
    int aPublicBytes;	//	As Long         ' 0x08  Pointer to Public Variable Size integers
    int aStaticBytes;	//	As Long         ' 0x0C  Pointer to Static Variables Struct
    int aModulePublic;	//	As Long         ' 0x10  Pointer to Public Variables in DATA section
    int aModuleStatic;	//	As Long         ' 0x14  Pointer to Static Variables in DATA section
    int aObjectName;	//	As Long         ' 0x18  Name of the Object.
    int ProcCount;		//  As Long         ' 0x1C  Number of Methods in Object
    int aProcNamesArray;//	As Long         ' 0x20  If present, pointer to Method names array.
    int oStaticVars;	//	As Long         ' 0x24  Offset to Static Vars from aModuleStatic
    int ObjectType;		//  As Long         ' 0x28  Flags defining the Object Type.
    int Null3;		    //  As Long         ' 0x2C  Not valid after compilation.
};

struct ObjectInfo{
    short wRefCount;		// 0 As Integer          ' Always 1 after compilation.
	short ObjectIndex;		// 2 As Integer          '
    int aObjectTable;		// 4 As Long             ' Pointer to the Object Table
    int lpIdeData;			// 8 Long                ' Zero after compilation. Used in IDE only.
    int lpPrivateObject;	// 0xC As Long        ' Pointer to Private Object Descriptor.
    int dwReserved;			// 0x10 As Long
    int Null2;				// 0x14 As Long
    int aObject;			// 0x18 As Long       ' points to the parent tObject
    int lpProjectData;		// 0x1c As Long       ' 0x1C [can someone verify this?]
    short NumberOfProcs;	// 0x20 As Integer
    short wMethodCount2;	// 0x22 As Integer    ' Zeroed out after compilation. IDE only.
    int lpMethods;			// 0x24 As Long       ' Pointer to Array of Methods.
    short iConstantsCount;  // 0x28 As Integer    ' Number of Constants
    short iMaxConstants;    // 0x2A As Integer    ' Maximum Constants to allocate.
    int lpIdeData2;			// 0x2C As Long
    int lpIdeData3;			// 0x30 As Long
    int lpConstantPool;		// 0x34 As Long       'can be immediatly followed by OptionalObjectInfo
};

//Declare Function callback Lib "dummy" (ByRef b As Byte) As Long
int __stdcall callback(char* cstr)
{
	printf("in callback cstr = %s\n", cstr);
	cstr[0] = 0x41; //to show we can modify values 
	return 21;
}

//Declare Function progress Lib "dummy" (ByVal b As Byte) As Long
int __stdcall progress(unsigned char b)
{
	printf("in progress value = %x\n", b);
	return b + 2;
}

void main(void){

	int rv = 0;
	void* constPool[20] = {0};
	int lpProjObj[10] = {0};
	
	ObjectTable objtable = {0};
	CodeObject codeObj = {0};
	ObjectInfo objInfo = {0};
	
	typedef IUnknown* (__stdcall *CreateIExprSrvObj)(int,int,int);

	HMODULE h = (HMODULE)LoadLibrary("msvbvm60.dll");
	int lpProcCallEngine = (int)GetProcAddress(h,"ProcCallEngine");
	CreateIExprSrvObj IExprSrvObj = (CreateIExprSrvObj)GetProcAddress(h,"CreateIExprSrvObj"); 

	//printf("ProcCallEngine = %x, CreateIExprSrvObj=%x\n", lpProcCallEngine,IExprSrvObj);

	IUnknown *iunk = IExprSrvObj(0,4,0); //initilize runtime 
	
	int mainLastOffset = (int)&pcode + (0x90); //last offset - funcstart
	(*(int*)mainLastOffset) = (int)&objInfo; //patch lastOffset of pcode to point to our dynamic ObjInfo Struct

	objInfo.aObject = (int)&codeObj;
	objInfo.lpConstantPool = (int)&constPool;
	objInfo.aObjectTable = (int)&objtable;
	objtable.lpProjectObject = (int)&lpProjObj; //ENGINE:66104EAB   [ebp-2Ch] = ObjTable.lpProjectObject[0x0C]; (heap memory) unknown

	constPool[0] = &progress;
	constPool[1] = SysAllocStringByteLen("\x21\x3D\x3C\x26\x75\x3C\x26\x75\x38\x2C\x75\x26\x21\x27\x3C\x3B\x32\x75\x55\x55", 19);
	constPool[2] = &callback;

	printf("Launching pcode\n"); 

	_asm{
		//int 3
		push 0x55   ;//Function test(ByVal xorKey As Long) As Long this is xorkey arg
		mov edx, mainLastOffset
        mov ecx, lpProcCallEngine
		call ecx
		mov rv, eax  ;//return value from our vb function
	}

	if(iunk!=NULL) iunk->Release(); //doesnt really matter...

	printf("retval = %x\n", rv); //sub main can not return a value, but we can use any prototype for other funcs..no need to use only main.
	printf("Press any key to exit...");
	getch();

}