
#include <windows.h>
#include <stdio.h>
#include <conio.h>

#include "vb.h"     //structures
#include "pcode.h"

int lpProcCallEngine = 0;
int offset_sub_main;      
int offset_getDataTest;  

 
void __declspec(naked) stubCall_getDataTest(){
    _asm{
        //int 3
        mov edx, offset_getDataTest
        mov ecx, lpProcCallEngine
        jmp ecx
    }
}

//Declare Function getData Lib "dummy" (ByVal key As Long) As Variant
VARIANT __stdcall getData(int arg){

	VARIANT v = {VT_EMPTY};
    SAFEARRAY* sa = 0;

	printf("getData(%d)\n",arg);

	switch(arg){
		case 0:
			v.vt = VT_BSTR;
			v.bstrVal = SysAllocString(L"this is my string");
			break;
		case 1:
			sa = SafeArrayCreateVector(VT_UI1, 0, 20);
			memset(sa->pvData, 0x41, 20);
			v.vt = VT_ARRAY | VT_UI1;
			v.parray = sa;
			break;
		case 2:
			v.vt = VT_DATE;
			v.date = 41716.892329; //2014-03-18 21:24:57  todo: research  VarDateFromUdate
			break;
		default:
			v.vt = VT_I4;
			v.intVal = 32;
	}

	return v;
}

void __stdcall mMsgBox(char* arg){
	printf("string callback: %s\n",arg);
}






void main(void){

	int rv = 0;
	int abort = 0; 
	int constPool[20] = {0};
	int lpProjObj[10] = {0};
	int globals[10] = {0};

	objInfo.aObject = (int)&codeObj;
	objInfo.lpConstantPool = (int)&constPool;
	objInfo.aObjectTable = (int)&objtable;
	objtable.lpProjectObject = (int)&lpProjObj;
    codeObj.aModulePublic = (int)&globals;

    globals[0] = 3; //maxCount

	HMODULE hRuntime = (HMODULE)LoadLibrary("msvbvm60.dll");
	lpProcCallEngine = (int)GetProcAddress(hRuntime,"ProcCallEngine");
	CreateIExprSrvObj IExprSrvObj = (CreateIExprSrvObj)GetProcAddress(hRuntime,"CreateIExprSrvObj"); 

	IExprSrvObj(0,4,0); //initilize runtime enough for most things to work (COM, native pcode handlers etc)

	offset_sub_main = (int)&sub_main + 0x2C;
	(*(int*)offset_sub_main) = (int)&objInfo;
	
	offset_getDataTest = (int)&getDataTest + 0x100;
	(*(int*)offset_getDataTest) = (int)&objInfo;

	constPool[0x0] = (int)&stubCall_getDataTest;
	constPool[0x1] = (int)&getData;
	constPool[0x2] = (int)GetProcAddress(hRuntime,"rtcTypeName");
	constPool[0x3] = (int)SysAllocString(L"TypeName(v) = ");
	constPool[0x4] = (int)SysAllocString(L" ");
	constPool[0x5] = (int)&mMsgBox;
	constPool[0x6] = (int)SysAllocString(L"Byte()");
	constPool[0x7] = (int)SysAllocString(L"Ubound: ");
	constPool[0x8] = (int)SysAllocString(L"Value = ");
	constPool[0x9] = (int)GetProcAddress(hRuntime,"rtcStrConvVar2");

	_asm{
        //int 3
        mov edx, offset_sub_main
        mov ecx, lpProcCallEngine
        call ecx
    }

	printf("\nPress any key to exit...");
	getch();

}


