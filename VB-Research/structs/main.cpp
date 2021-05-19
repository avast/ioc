
#include <windows.h>
#include <stdio.h>
#include <conio.h>

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


int __stdcall mMsgBox(wchar_t *str)
{
	if(str == NULL || *str == NULL) return 0;
	return MessageBoxW(0, str, L"In C",0);
}

struct CFG{
	BSTR    str1;
	int     int1;
};

unsigned char test[] = {
	0x6C, 0x0C, 0x00, 0x5E, 0x00, 0x00, 0x04, 0x00, 0xFD, 0x69, 0x58, 0xFF, 0x04, 0x48, 0xFF, 0x0A, 
	0x01, 0x00, 0x08, 0x00, 0x04, 0x48, 0xFF, 0xFD, 0xFE, 0x44, 0xFF, 0x5E, 0x00, 0x00, 0x04, 0x00, 
	0x0A, 0x02, 0x00, 0x04, 0x00, 0x3C, 0x2F, 0x44, 0xFF, 0x36, 0x04, 0x00, 0x58, 0xFF, 0x48, 0xFF, 
	0x3A, 0x34, 0xFF, 0x03, 0x00, 0x07, 0x0C, 0x00, 0x04, 0x00, 0x4D, 0x68, 0xFF, 0x03, 0x40, 0x04, 
	0x58, 0xFF, 0x0A, 0x01, 0x00, 0x08, 0x00, 0x04, 0x58, 0xFF, 0xFB, 0xEF, 0x48, 0xFF, 0xFD, 0xFE, 
	0x44, 0xFF, 0x5E, 0x00, 0x00, 0x04, 0x00, 0x0A, 0x02, 0x00, 0x04, 0x00, 0x3C, 0x2F, 0x44, 0xFF, 
	0x36, 0x04, 0x00, 0x58, 0xFF, 0x48, 0xFF, 0x94, 0x0C, 0x00, 0x00, 0x00, 0x5E, 0x00, 0x00, 0x04, 
	0x00, 0x0A, 0x02, 0x00, 0x04, 0x00, 0x3C, 0x1B, 0x04, 0x00, 0x94, 0x0C, 0x00, 0x00, 0x00, 0x2A, 
	0x31, 0x30, 0xFF, 0x6C, 0x30, 0xFF, 0x5E, 0x00, 0x00, 0x04, 0x00, 0x0A, 0x02, 0x00, 0x04, 0x00, 
	0x3C, 0x14, 0x00, 0x00, 0x9C, 0x10, 0x40, 0x00, 0x08, 0x00, 0x4C, 0x00, 0x94, 0x00, 0x28, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x19, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0xFF, 0x01, 0x00, 0x18, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x44, 0xFF, 0x01, 0x00, 0x58, 0xFF, 0x02, 0x00, 
	0x48, 0xFF, 0x02, 0x00, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xE9, 0xE9, 0xE9, 0xE9, 
	0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0x9E, 0x9E, 0x9E, 0x9E, 
	0xAC, 0x16, 0x00, 0x00
};

void main(void){

	int rv = 0;
	int constPool[20] = {0};
	int lpProjObj[10] = {0};
	
	ObjectTable objtable = {0};
	CodeObject codeObj = {0};
	ObjectInfo objInfo = {0};
	
	typedef IUnknown* (__stdcall *CreateIExprSrvObj)(int,int,int);

	HMODULE hRuntime = (HMODULE)LoadLibrary("msvbvm60.dll");
	int lpProcCallEngine = (int)GetProcAddress(hRuntime,"ProcCallEngine");
	CreateIExprSrvObj IExprSrvObj = (CreateIExprSrvObj)GetProcAddress(hRuntime,"CreateIExprSrvObj"); 

	//printf("ProcCallEngine = %x, CreateIExprSrvObj=%x\n", lpProcCallEngine,IExprSrvObj);

	IUnknown *iunk = IExprSrvObj(0,4,0); //initilize runtime 
	
	// test  - 216 bytes
	int offset_test = (int)&test + 0x94;
	(*(int*)offset_test) = (int)&objInfo;

	objInfo.aObject = (int)&codeObj;
	objInfo.lpConstantPool = (int)&constPool;
	objInfo.aObjectTable = (int)&objtable;
	objtable.lpProjectObject = (int)&lpProjObj; //ENGINE:66104EAB   [ebp-2Ch] = ObjTable.lpProjectObject[0x0C]; (heap memory) unknown

	CFG cfg;

	//if we had used only a wchar string, we would get a crash 
	//if we tried to concat it with anything. StrPtr(cfg.str1) would be ok but not much else.
	cfg.str1 = SysAllocString(L"this is my string in cfg");  
	cfg.int1 = 0x11223344;

	constPool[0x0] = (int)GetProcAddress(hRuntime,"VarPtr");
	constPool[0x1] = (int)GetProcAddress(hRuntime,"rtcHexVarFromVar");
	constPool[0x2] = (int)&mMsgBox;
	constPool[0x3] = (int)SysAllocString(L"c.int1 = 0x");
	constPool[0x4] = (int)SysAllocString(L"will i get a crash? ");

	printf("Launching pcode cfg = %x\n", &cfg); 

	_asm{
		//int 3
		lea eax, cfg  
		push eax                   //Function test(ByRef c As cfg) As Long
		mov edx, offset_test
        mov ecx, lpProcCallEngine
		call ecx
		mov rv, eax  ;//return value from our vb function
	}

	if(iunk!=NULL) iunk->Release(); //doesnt really matter...

	printf("retval = %x\n", rv); //sub main can not return a value, but we can use any prototype for other funcs..no need to use only main.
	printf("Press any key to exit...");
	getch();

}