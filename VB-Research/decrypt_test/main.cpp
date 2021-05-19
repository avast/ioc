
#include <windows.h>
#include <stdio.h>
#include <conio.h>

#include "vb.h"     //structures
#include "pcode.h"

int lpProcCallEngine = 0;

//examples progress callback (same vb declare as sleep)
void __stdcall callback(int arg){
	printf("%d\n",arg);
}

void __stdcall strCallBack(char* arg){
	printf("string callback: %s\n",arg);
}

//get a temp pointer to p + xBytes without casts or pointer arithmetic
int* pPlus(int * p, int increment){
	_asm{
		mov eax, p
		add eax, increment
	}
}

int initExtendedTLS(HMODULE hRuntime){
	
	//vb file access however requires Ebthread+18 to point to valid alloc that doesnt happen with IExprSrvObj initilization..
	//we dont really need this if we use C callbacks...only use this if really necessary since it adds complexity

	//we get its tls index offset from the start of the rtcGetErl export...
	//.text:660EA58E FF 35 00 00 11 66   push    _g_itlsEbthread
    int* lpRtcErl = (int*)GetProcAddress(hRuntime,"rtcGetErl");
	if(lpRtcErl==0) return -1;

	short p = (short)(*lpRtcErl);
	if (p != 0x35FF) return -2;                    //Check rtcGetErl for push opcode failed

	int* tlsEbthread = (int*)*(pPlus(lpRtcErl,2)); //address of tls slot variable
	int* tlsMem = (int*)TlsGetValue(*tlsEbthread); //slot value -> actual memory alloc
    if ( tlsMem == 0 ) return -3;                  //TlsGetValue(*g_itlsEbthread) failed 

	int buf = (int)malloc(80);
	if(buf==0) return -4;
	memset((void*)buf,0,80);  //MUST be zeroed out

	//printf("tlsMem = %x dummy=%x\n", tlsMem, buf);
    //printf("tlsMem + 0x18 = %x\n", (char*)tlsMem + 0x18);

    //_asm int 3
	*pPlus(tlsMem,0x18) = buf; //fill in this field of struct with our own alloced memory
	return 1;

}

int offset_rc4;

void __declspec(naked) stubCall_rc4(){
	_asm{
		//int 3
		mov     edx, offset_rc4
		mov     ecx, lpProcCallEngine
		jmp     ecx
	}
}



void main(void){

	int rv = 0;
	int abort = 0; 
	int constPool[20] = {0};
	int lpProjObj[10] = {0};
	
	objInfo.aObject = (int)&codeObj;
	objInfo.lpConstantPool = (int)&constPool;
	objInfo.aObjectTable = (int)&objtable;
	objtable.lpProjectObject = (int)&lpProjObj;

	/*some debugging values 
	printf("objtable = %x\n",  &objtable);
	printf("lpProjObj = %x\n", &lpProjObj);
	printf("constPool = %x\n", &constPool);
	printf("pcode = %x - %x\n", &pcode, &pcode + sizeof(pcode));
	printf("abort addr: %x\n", (int)&abort);*/

	HMODULE hRuntime = (HMODULE)LoadLibrary("msvbvm60.dll");
	lpProcCallEngine = (int)GetProcAddress(hRuntime,"ProcCallEngine");
	CreateIExprSrvObj IExprSrvObj = (CreateIExprSrvObj)GetProcAddress(hRuntime,"CreateIExprSrvObj"); 

	IExprSrvObj(0,4,0); //initilize runtime enough for most things to work (COM, native pcode handlers etc)

	//do you need access to native vb file access functions or vb msgbox? (C callbacks cleaner)
	/*if(initExtendedTLS(hRuntime) != 1){
		printf("initExtendedTLS failed...");
		return;
	}*/

	//build the const pool
	constPool[0x0] = (int)GetProcAddress(hRuntime,"rtcVarBstrFromAnsi");
	constPool[0x1] = (int)SysAllocString(L"AAAA");
    constPool[0x2] = (int)&stubCall_rc4; //Module1.Proc_4015EC
	constPool[0x3] = (int)&strCallBack;
	constPool[0x4] = (int)GetProcAddress(hRuntime,"rtcTypeName");
	constPool[0x5] = (int)SysAllocString(L"Byte()");
	constPool[0x6] = (int)&callback;
	constPool[0x7] = (int)SysAllocString(L"String");
	constPool[0x8] = (int)GetProcAddress(hRuntime,"rtcStrConvVar2");
	constPool[0x9] = (int)GetProcAddress(hRuntime,"rtcLeftCharBstr");

	offset_rc4 = (int)&rc4 + 0x3e4;
	(*(int*)offset_rc4) = (int)&objInfo;	

	int offset_sub_main = (int)&sub_main + 0x90;
	(*(int*)offset_sub_main) = (int)&objInfo;
	
	/* full run tested & working..
	_asm{
		//int 3
		mov edx, offset_sub_main 
        mov ecx, lpProcCallEngine
		call ecx
		mov rv, eax
	}
	*/

    //now lets call the rc4 function on our own
	/*
		Public Function rc4(ByteOrString As Variant, ByVal password As String, strret As Boolean) as variant

		0019FC58 ebp-E8  0x0019FC70 ; ebp-D0 = empty variant (retval)
		0019FC5C ebp-E4  0x0019FC88 ; ebp-B8 = variant bstr aaaa
		0019FC60 ebp-E0  0x00794DEC =         0x41
		0019FC64 ebp-DC  0x0019FC82 ; ebp-BE = -1
	*/
	
	VARIANT retVal = {VT_EMPTY};
	VARIANT v = {VT_EMPTY};
	v.vt = VT_BSTR;
	v.bstrVal = SysAllocStringByteLen("\x92\x01\x60\x01\xA7\x00\x7C\x00",8);
	BSTR passwd = SysAllocString(L"A");
    int boolStrRet = -1; //vb true

	_asm{
		//int 3
		lea eax, boolStrRet
		push eax
		push passwd
		lea eax, v
		push eax
		lea eax, retVal
		push eax
		mov edx, offset_rc4
        mov ecx, lpProcCallEngine
		call ecx
	}

	printf("retval.vt = %x\n", retVal.vt);
    wprintf(L"retval.bstr = %s\n", retVal.bstrVal);
	printf("Press any key to exit...");
	getch();

}


