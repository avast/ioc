
#include <windows.h>
#include <stdlib.h>
#include "./distorm3.3/distorm.h"
#include <stdio.h>
#include <intrin.h>

#pragma warning(disable:4996)

//This is a modified version of the open source x86/x64 
//NTCore Hooking Engine written by:
//Daniel Pistelli <ntcore@gmail.com>
//http://www.ntcore.com/files/nthookengine.htm
//
//It uses the x86/x64 GPL disassembler engine
//diStorm was written by Gil Dabah. 
//Copyright (C) 2003-2012 Gil Dabah. diStorm at gmail dot com.
//
//Mods by David Zimmer <dzzie@yahoo.com>


//note: in several places we work on g_HookInfo[g_NumberOfHooks] as a global object in sub fx..


// 10000 hooks should be enough
#define MAX_HOOKS 10000
#define JUMP_WORST		0x10		// Worst case scenario + line all up on 0x10 boundary...
#define MAX_INSTRUCTIONS 100

#ifndef __cplusplus
#define extern "C" stdc
#else
#define  stdc
#endif

#ifdef _M_IX86
	#define isX64 false
#else 
	#define isX64 true
#endif

//on x86 htjmp requires less than 2gb between addresses
//on x64 pushret requires a 32 bit safe address use #pragma comment( linker, "/BASE:0x8000000")
//                                         x86 only                     
enum hookType{ ht_jmp = 0, ht_pushret=1, ht_jmp5safe=2, ht_jmpderef=3, ht_micro, ht_auto };
enum hookErrors{ he_None=0, he_cantDisasm, he_cantHook, he_maxHooks, he_UnknownHookType, he_cantInit  };
enum specificErrors{ hs_None, hs_NeedsAbs, hs_NoMicro, hs_ToBig, hs_x64NoPushRet };

char* hook_name[] = {"ht_jmp", "ht_pushret", "ht_jmp5safe", "ht_jmpderef", "ht_micro", "ht_auto"};

int  logLevel = 0;  
bool initilized = false;
char lastError[500] = {0};
hookErrors lastErrorCode = he_None;
specificErrors specificError = hs_None;
void  (__cdecl *debugMsgHandler)(char* msg);

typedef struct _HOOK_INFO
{
	ULONG_PTR Function;	// Address of the original function
	ULONG_PTR Hook;		// Address of the function to call 
	ULONG_PTR Bridge;   // Address of the instruction bridge
	hookType hooktype;
	char* ApiName;
	bool Enabled;
	int preAlignBytes;
	int index;
	int hookableBytes;
	int OverwrittenBytes;
	int OverwrittenInstructions;

} HOOK_INFO, *PHOOK_INFO;

HOOK_INFO g_HookInfo[MAX_HOOKS];
UINT g_NumberOfHooks = 0;
BYTE *g_pBridgeBuffer = NULL; // Here are going to be stored all the bridges
UINT g_CurrentBridgeBufferSize = 0; // This number is incremented as the bridge buffer is growing

char* GetHookName(hookType ht){
	return hook_name[ht];
}

stdc
char* __cdecl GetHookError(void){
	return (char*)lastError;
}

stdc
bool is32BitSafe(ULONG_PTR value){
	ULONG_PTR b = value & 0x00000000FFFFFFFF;
	return value == b ? true : false;
}

void dbgmsg(int level, const char *format, ...)
{
	char buf[1024];

	if(level > logLevel) return;

	if(debugMsgHandler!=NULL && format!=NULL){
		va_list args; 
		va_start(args,format); 
		try{
			_vsnprintf(buf,1024,format,args);
			(*debugMsgHandler)(buf);
		}
		catch(...){}
	}

}
stdc
bool __cdecl InitHookEngine(void){
	
	if(initilized) return true;
	
	char* mem_marker = "APIHOOKS";
	int len_marker = strlen(mem_marker);
	UINT sz = MAX_HOOKS * (JUMP_WORST * 3);
	sz +=len_marker;

	//try to get a 32bit safe allocation address...
	//g_pBridgeBuffer = (BYTE *)VirtualAlloc((void*)0x11000000 , sz, MEM_RESERVE | MEM_COMMIT , 0x40);

	if(g_pBridgeBuffer == NULL){
		g_pBridgeBuffer = (BYTE *) VirtualAlloc(NULL, sz, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
	}else{
		dbgmsg(1,"32 bit safe trampoline buffer obtained\n");
	}

	if(g_pBridgeBuffer == NULL) return false;
	
	memset(g_pBridgeBuffer, 0 , sz);
	memset(&g_HookInfo[0], 0, sizeof(struct _HOOK_INFO) * MAX_HOOKS);

	memcpy(g_pBridgeBuffer, mem_marker, len_marker);
	g_CurrentBridgeBufferSize += len_marker;

	initilized = true;
	return true;
}

//can now resolve from any pointer - dz 11.28.22
HOOK_INFO *GetHookInfoFromFunction(ULONG_PTR lpFunc)
{
	if (g_NumberOfHooks == 0)
		return NULL;

	for (UINT x = 0; x < g_NumberOfHooks; x++)
	{
		if (g_HookInfo[x].Function == lpFunc) return &g_HookInfo[x];
		if (g_HookInfo[x].Bridge == lpFunc) return &g_HookInfo[x];
		if (g_HookInfo[x].Hook == lpFunc) return &g_HookInfo[x];
	}

	return NULL;
}

#ifdef _M_IX86
	//these two are only used for x86 ht_jmp5safe hooks..

	void __stdcall output(ULONG_PTR ra){
		HOOK_INFO *hi = GetHookInfoFromFunction(ra);
		if(hi){
			dbgmsg(0,"jmp %s+5 api detected trying to recover...\n", hi->ApiName );
		}else{
			dbgmsg(0,"jmp+5 api caught %x\n", ra );
		}
	}

	void __declspec(naked) UnwindProlog(void){
		_asm{
			mov eax, [ebp-4] //return address
			sub eax, 10      //function entry point
			push eax         //arg to output
			call output

			pop eax      //we got here through a call from our api hook stub so this is ret
			sub eax, 10  //back to api start address
			mov esp, ebp //now unwind the prolog the shellcode did on its own..
			pop ebp      //saved ebp 
			jmp eax      //and jmp back to the api public entry point to hit main hook jmp
		}
	}

#endif

// This function  retrieves the necessary size for the jump
// overwrite as little of the api function as possible per hook type...
UINT GetJumpSize(hookType ht)
{

	#ifdef _M_IX86

		switch(ht){
			case  ht_jmp: return 5;
			case  ht_pushret: return 6;
			case  ht_micro: return 2; //overwrite size is actually only 2 + 5 in preamble.
			default: return 10;
		}

	#else

		switch(ht){
			case  ht_jmpderef: return 14;
			case  ht_pushret: return 6;
			case  ht_micro: return 6; //overwrite size is actually only 6 + 8 in preamble.
			default: return 12;
		}

	#endif

}

stdc
char* __cdecl GetDisasm(ULONG_PTR pAddress, int* retLen = NULL){ //just a helper doesnt set error code..

	_DecodeResult res;
	_DecodedInst decodedInstructions[MAX_INSTRUCTIONS];
	unsigned int decodedInstructionsCount = 0;
	_DecodeType dt =  isX64 ? Decode64Bits : Decode32Bits;
	_OffsetType offset = 0;

	res = distorm_decode(offset,	// offset for buffer
		(const BYTE *) pAddress,	// buffer to disassemble
		50,							// function size (code size to disasm) 
		dt,							// x86 or x64?
		decodedInstructions,		// decoded instr
		MAX_INSTRUCTIONS,			// array size
		&decodedInstructionsCount	// how many instr were disassembled?
		);

	if (res == DECRES_INPUTERR)	return NULL;
	
	int bufsz = 120;
	char* tmp = (char*)malloc(bufsz);
	memset(tmp, 0, bufsz);
	_snprintf(tmp, bufsz-1 , "%10x  %-10s %-6s %s\n", 
			 pAddress, 
		     decodedInstructions[0].instructionHex.p, 
			 decodedInstructions[0].mnemonic.p, 
			 decodedInstructions[0].operands.p
	);

	if(retLen !=NULL) *retLen = decodedInstructions[0].size;

	return tmp;
}
	



bool UnSupportedOpcode(BYTE *b, int hookIndex){ //primary instruction opcodes are the same for x64 and x86 

	BYTE bb = *b;
	
	switch(bb){ 
		case 0x74:
		case 0x75: 
		case 0xEB:
		case 0xE8:
		case 0xE9:
		case 0x0F: //can lead to false positive...
		//case 0xFF:
		case 0xc3: 
		case 0xc4: 
			        goto failed;
	}

	return false;


failed:
		UINT offset = (UINT)b - g_HookInfo[hookIndex].Function;
		char* d = GetDisasm((ULONG_PTR)b);

		if(d == NULL){
			sprintf(lastError,"Unsupported opcode at %s+%d: Opcode: %x", g_HookInfo[hookIndex].ApiName, offset, *b);
			lastErrorCode = he_cantHook;
		}else{
			sprintf(lastError,"Unsupported opcode at %s+%d\n%s", g_HookInfo[hookIndex].ApiName, offset, d);
			lastErrorCode = he_cantHook;
			free(d);
		}

		dbgmsg(1,lastError);
		return true;

}


void WriteInt( BYTE *pAddress, UINT value){    //4 bytes always
	*(UINT*)pAddress = value;
}

void WriteShort( BYTE *pAddress, short value){ //2 bytes always
	*(short*)pAddress = value;
}

void WriteULONG( BYTE *pAddress, ULONG_PTR value){//8 BYTES ON X64
	*(ULONG_PTR*)pAddress = value;
}

// A relative jump (opcode 0xE9) treats its operand as a 32 bit signed offset. If the unsigned
// distance between from and to is of sufficient magnitude that it cannot be represented as a 
// signed 32 bit integer, then we'll have to use an absolute jump instead (0xFF 0x25).
//https://bitbucket.org/edd/nanohook/src/da62bc7232e6/src/hook.cpp
bool abs_jump_required(UINT from, UINT to)
{
    const UINT upper = max(from, to);
    const UINT lower = min(from, to);

	return ((upper - lower) > 0x7FFFFFFF) ? true : false;
} 

bool isRelativeJump(hookType ht){

	#ifdef _M_IX86
		if( ht == ht_pushret ) return false;
		if( ht == ht_jmpderef ) return false;
		return true;
	#else
		return false;
	#endif
}

void OverWriteScratchPad(VOID *pAddress, HOOK_INFO *hinfo)
{	 
	DWORD dwOldProtect = 0;
	DWORD dwBuf = 0;
	int minPreAlign = 0;
    int sz = hinfo->OverwrittenBytes;

	BYTE *pCur = (BYTE *)pAddress;

	if(hinfo->hooktype == ht_micro){
		minPreAlign = isX64 ? 8 : 5 ;
		pCur -= minPreAlign;
		sz   += minPreAlign;
	}
	
	VirtualProtect(pCur, JUMP_WORST, PAGE_EXECUTE_READWRITE, &dwOldProtect);

	for(int i=0; i<sz; i++)	*pCur++ = 0xCC;

	VirtualProtect(pCur, JUMP_WORST, dwOldProtect, &dwBuf);

}

bool WriteJump(VOID *pAddress, ULONG_PTR JumpTo, hookType ht, int hookIndex)
{	 
	DWORD dwOldProtect = 0;
	int minPreAlign = 0;

	if(ht == ht_micro) minPreAlign = isX64 ? 8 : 5 ;

	BYTE *pCur = (BYTE *)pAddress;
	VirtualProtect(pCur - minPreAlign , JUMP_WORST, PAGE_EXECUTE_READWRITE, &dwOldProtect);
	

#ifdef _M_IX86
       
	   if( isRelativeJump(ht) ){
		   if( abs_jump_required( (UINT)pAddress, (UINT)JumpTo) ){
			   DebugBreak(); //this shouldnt happen with the pre-Validation
			   //sprintf(lastError, "Can not use a relative jump for this hook %s\n", g_HookInfo[hookIndex].ApiName); 
			   //lastErrorCode = he_cantHook;
			   //dbgmsg(0, "Can not use a relative jump for this hook %s\n", g_HookInfo[hookIndex].ApiName);
			   return false;
		   }
	   }


	   if(ht == ht_pushret){
		   //68 DDCCBBAA      PUSH AABBCCDD (6 bytes) - hook detectors wont see it, 
		   //C3               RETN                      jmp+5 = crash (good no exec, bad crash..)
		   *pCur = 0x68;
		   *((ULONG_PTR *)++pCur) = JumpTo;
		   pCur+=4;
		   *pCur = 0xc3;
	   }
	   else if(ht == ht_micro){
			// E9 xxxxxxxx   jmp 0x11111111 <--in fx preamble  (5 bytes)
			// EB F9         jmp short here <--api entry point (2 bytes)
		    pAddress = (BYTE *)pAddress - 5;
		    UINT dst = JumpTo - (UINT)(pAddress) - 5;  //2gb address limitation
			*pCur = 0xE9;
			WriteInt(pCur+1, dst);
			WriteShort(pCur+5, 0xF9EB);
	   }
	   else if(ht == ht_jmpderef){	  
			//eip>  FF25 AABBCCDD    JMP DWORD PTR DS:[eip+6] 10 bytes
			//eip+6 xxxxxxxx         data after instruction, other hookers will bad disasm, and large footprint
			*pCur = 0xff;            //if we can use the preALignBytes footprint down to 6...
			*(pCur+1) = 0x25;
			WriteInt(pCur+2, (int)pCur + 6);
			WriteInt(pCur+6, JumpTo);
	   }
	   else if(ht== ht_jmp){
			//E9 jmp (DESTINATION_RVA - CURRENT_RVA - 5 [sizeof(E9 xx xx xx xx)]) (5 bytes)
		    UINT dst = JumpTo - (UINT)(pAddress) - 5;  //2gb address limitation
			*pCur = 0xE9;
			WriteInt(pCur+1, dst);
	   }
	   else if(ht = ht_jmp5safe){ //this needs a second trampoline if api+5 jmp is hit, it needs to reverse the push ebp to send to hook..
			//E9 jmp normal prolog + eB call to UnwindProlog  (10 bytes)
		    *(pCur) = 0xE9;                        //fancy and cool but big footprint and complex..
			UINT dst = JumpTo - (UINT)(pCur) - 5; 
			WriteInt(pCur+1, dst);			
			*(pCur+5) = 0xE8;
			dst = (UINT)&UnwindProlog - (UINT)(pCur+5) - 5; //api+5 jmps are sent to our generic unwinder 
			WriteInt(pCur+6, dst);
	   }
	   else{
		   dbgmsg(0, "Unimplemented hook type asked for");
		   DebugBreak();
		   return false;
	   }

#else ifdef _M_AMD64

		
	if(ht == ht_jmpderef){
		//ff 25 00 00 00 00        jmp [rip+addr] (14 bytes)
	    //80 70 8e 77 00 00 00 00  data: 00000000778E7080

		WriteShort(pCur, 0x25FF);
		WriteInt(pCur+2, 0x00000000);
		WriteULONG(pCur+6, JumpTo);

	}else if(ht == ht_pushret){
		   //68 DDCCBBAA      PUSH AABBCCDD (6 bytes) -  x64 push still takes a 32 bit const, 8 bytes written to stack, high 8 = 0
		   //C3               RETN   
		   if(!is32BitSafe(JumpTo) ){
			    dbgmsg(0, "Hooking %s failed: Can not use x64 push ret hook - jumpTo address is not 32bit safe %016llx\n", g_HookInfo[hookIndex].ApiName, JumpTo); 
			    DebugBreak(); //this shouldnt happen with the pre-Validation
				return false;
		   }
		   *pCur = 0x68;
		   WriteInt(pCur+1, JumpTo);
		   pCur+=5;
		   *pCur = 0xc3;
	}else if(ht == ht_micro){
			//0000000011000000 8 data bytes in function prealignment paddding...
            //0000000011000008 FF 25 F2 FF FF FF jmp qword ptr [11000000h]  <-- 6 byte hook in API prolog
			WriteInt(pCur, 0xFFF225FF);
			WriteShort(pCur+4, 0xFFFF);
			WriteULONG(pCur-8, JumpTo);
	 }else{
        //default x64 hooktype..
		//48 b8 80 70 8e 77 00 00 00 00   mov rax, 0x00000000778E7080 (12 bytes)
		//ff e0                           jmp rax  

		WriteShort(pCur, 0xb848); 
		WriteULONG(pCur+2, JumpTo);
		WriteShort(pCur+10, 0xE0FF);
	}

		/*
		how about ff25 [4byte address of alloced table entry].. 
		should be down to 6 bytes inline?
		if you can stay in the 2gb range i think..

		(16 bytes preserves rax)
		50                             push rax
		48 B8 EF CD AB 90 78 56 34 12  mov     rax, 1234567890ABCDEFh
        48 87 04 24                    xchg    rax, [rsp]
        C3                             retn
		*/

#endif

	DWORD dwBuf = 0;	// nessary othewrise the function fails
	VirtualProtect(pCur - minPreAlign, JUMP_WORST, dwOldProtect, &dwBuf);
	return true;
}

//is there any padding before the function start to emded data? many x86 have 5 bytes..
int CountPreAlignBytes(BYTE* pAddress){ 
	
	int x;
	for(x=0; x<=9; x++ ){
		BYTE b = *(BYTE*)(pAddress-x-1);
		if(b==0x90 || b==0xCC) ; else break;
	}
	return x;
}


VOID *CreateBridge(HOOK_INFO *hinfo)
{
	if (g_pBridgeBuffer == NULL) return NULL;

	UINT x = 0;
	_DecodeResult res;
	_DecodedInst decodedInstructions[MAX_INSTRUCTIONS];
	unsigned int decodedInstructionsCount = 0;
	_DecodeType dt =  isX64 ? Decode64Bits : Decode32Bits;
	_OffsetType offset = 0;

	ULONG_PTR Function = hinfo->Function;
	int JumpSize = GetJumpSize(hinfo->hooktype);

	res = distorm_decode(offset,	// offset for buffer
		(const BYTE *) Function,	// buffer to disassemble
		50,							// function size (code size to disasm) 
									// 50 instr should be _quite_ enough
		dt,							// x86 or x64?
		decodedInstructions,		// decoded instr
		MAX_INSTRUCTIONS,			// array size
		&decodedInstructionsCount	// how many instr were disassembled?
		);

	if (res == DECRES_INPUTERR){
		sprintf(lastError, "Could not disassemble address %x", (UINT)Function);
		//dbgmsg(lastError);
		lastErrorCode = he_cantDisasm;
		return NULL;
	}

	DWORD InstrSize = 0;
	VOID *pBridge = (VOID *) &g_pBridgeBuffer[g_CurrentBridgeBufferSize];

	//copy full instructions from API to our trampoline.
	for (x ; x < decodedInstructionsCount; x++)
	{
		if (InstrSize >= JumpSize) break;

		BYTE *pCurInstr = (BYTE *) (InstrSize + (ULONG_PTR) Function);
		
		if(logLevel >=3){
			dbgmsg(3, "%s+%d \t %-10s %-6s %s", 
				 hinfo->ApiName,
				 InstrSize,
				 decodedInstructions[x].instructionHex.p, 
				 decodedInstructions[x].mnemonic.p, 
				 decodedInstructions[x].operands.p
			);
		}

		if( UnSupportedOpcode(pCurInstr, hinfo->index) ){
			dbgmsg(0, "CreatreBridge::UnSupportedOpcode found missed in pre-Validation?! needed=%d, hookable=%d, cur=%d, type=%s",
						JumpSize, hinfo->hookableBytes,InstrSize, GetHookName(hinfo->hooktype)
				   );
			DebugBreak(); 
			//if we leave here, g_CurrentBridgeBufferSize has been incremented and bytes copied to
			//the alloced g_pBridgeBuffer, but the API itself is untouched.
			return NULL; 
		}

		memcpy(&g_pBridgeBuffer[g_CurrentBridgeBufferSize], (VOID *) pCurInstr, decodedInstructions[x].size);

		g_CurrentBridgeBufferSize += decodedInstructions[x].size;
		InstrSize += decodedInstructions[x].size;
	}

	hinfo->OverwrittenInstructions = x;
	hinfo->OverwrittenBytes = InstrSize; //we will 0xCC this many in API latter for debugging sake...

	//to leave trampoline...
	hookType ht = isX64 ? ht_jmp : ht_pushret; //both absolute address jumps for safety...
	bool rv = WriteJump(&g_pBridgeBuffer[g_CurrentBridgeBufferSize], Function + InstrSize, ht, hinfo->index);
	g_CurrentBridgeBufferSize +=  GetJumpSize(ht);  

	if(!rv) return NULL;

	return pBridge;
}

void ZeroHookInfo(int hookIndex){
	if( g_HookInfo[hookIndex].ApiName != NULL) free(g_HookInfo[hookIndex].ApiName);
	memset(&g_HookInfo[hookIndex], 0, sizeof(struct _HOOK_INFO));
}

int HookableBytes(ULONG_PTR Function){

	_DecodeResult res;
	_DecodedInst decodedInstructions[MAX_INSTRUCTIONS];
	unsigned int decodedInstructionsCount = 0;
	_DecodeType dt =  isX64 ? Decode64Bits : Decode32Bits;
	_OffsetType offset = 0;

	res = distorm_decode(offset,	// offset for buffer
		(const BYTE *) Function,	// buffer to disassemble
		50,							// function size (code size to disasm) 
									// 50 instr should be _quite_ enough
		dt,							// x86 or x64?
		decodedInstructions,		// decoded instr
		MAX_INSTRUCTIONS,			// array size
		&decodedInstructionsCount	// how many instr were disassembled?
		);

	if (res == DECRES_INPUTERR) return 0;

	DWORD InstrSize = 0;

	for (UINT x = 0; x < decodedInstructionsCount; x++)
	{
		BYTE *pCurInstr = (BYTE *) (InstrSize + (ULONG_PTR)Function);
		if (InstrSize >= 15) break;
		if(UnSupportedOpcode(pCurInstr, g_NumberOfHooks)) break; 
		InstrSize += decodedInstructions[x].size;
	}

	return InstrSize;

}


bool ValidateHookType(HOOK_INFO *hinfo){
	
	int neededSize = GetJumpSize(hinfo->hooktype);
	char* name = hook_name[(int)hinfo->hooktype];
	specificError = hs_None; 

	if(hinfo->hookableBytes < neededSize){
		specificError = hs_ToBig; 
		sprintf(lastError, "%s hook failed %s only has %d hookable bytes available\n", name , hinfo->ApiName, hinfo->hookableBytes );
		return false;
	}

	if( isRelativeJump( hinfo->hooktype ) ){//only use relative jumps for api->hook *never* bridge->real api
		if( abs_jump_required( (UINT)hinfo->Function, (UINT)hinfo->Hook ) ){
			   specificError = hs_NeedsAbs;
			   sprintf(lastError, "Can not use a relative jump for this hook %s\n", hinfo->ApiName); 
			   return false;
		}
	}

	if(hinfo->hooktype == ht_micro){
		int minPreAlign = isX64 ? 8 : 5 ;
		if(hinfo->preAlignBytes < minPreAlign){
			specificError = hs_NoMicro;
			sprintf(lastError, "ht_micro hook failed %s only has %d preAmble bytes available\n", hinfo->ApiName, hinfo->preAlignBytes );
			return false;
		}
	}	

	if(isX64 && !is32BitSafe(hinfo->Hook) ){
		specificError = hs_x64NoPushRet;
		sprintf(lastError, "Hooking %s failed: Can not use x64 push ret hook - jumpTo address is not 32bit safe %016llx\n", hinfo->ApiName, hinfo->Hook); 
	    return false;
    }

	return true;

}

bool AutoChooseHookType(HOOK_INFO *hinfo){

	// ht_jmp = 0, ht_pushret=1, ht_jmp5safe=2, ht_jmpderef=3, ht_micro, ht_auto
	if(isX64){
		 //ht_jmpderef:14,  ht_pushret 6; ht_micro 6; default: 12;
		 hinfo->hooktype = ht_jmp;  //safest but requires 12 bytes...
         if(ValidateHookType(hinfo)) return true;
		 hinfo->hooktype = ht_micro; //if size was an issue, lets try this one
		 if(ValidateHookType(hinfo)) return true;
		 hinfo->hooktype = ht_pushret; //maybe no preamble space, this one is more limited though in address range..
		 if(ValidateHookType(hinfo)) return true;
		 return false; //bummer no go...
	}else{
		//ht_jmp: 5; ht_pushret 6; ht_micro 2;  default: 10
		 hinfo->hooktype = ht_jmp;  //best general choice
         if(ValidateHookType(hinfo)) return true;
		 hinfo->hooktype = ht_micro; //if size was an issue, lets try this one
		 if(ValidateHookType(hinfo)) return true;
		 return false; //bummer no go...
	}

}

stdc
BOOL __cdecl HookFunction(ULONG_PTR OriginalFunction, ULONG_PTR NewFunction, char *name, hookType ht)
{

	lastErrorCode = he_None;
	specificError = hs_None;
    lastError[0] = 0;

	if(!initilized){
		if( !InitHookEngine() ){
			lastErrorCode = he_cantInit;
			strcpy(lastError,"Can not Initilize HookEngine.");
			dbgmsg(1,lastError);
			return FALSE;
		}
	}

	HOOK_INFO *hinfo = GetHookInfoFromFunction(OriginalFunction);

	if (hinfo) return TRUE; //already hooked...

	if (g_NumberOfHooks == (MAX_HOOKS - 1)){
		lastErrorCode = he_maxHooks;
		strcpy(lastError,"Maximum number of hooks reached.");
		dbgmsg(1,lastError);
		return FALSE;
	}

	if(ht > ht_auto){
	   sprintf(lastError, "Unimplemented hook type asked for");
	   lastErrorCode = he_UnknownHookType;
	   return false;
	}

	hinfo = &g_HookInfo[g_NumberOfHooks];

	hinfo->Function = OriginalFunction;
	hinfo->Hook = NewFunction;
    hinfo->hooktype = ht;
	hinfo->index = g_NumberOfHooks;
	hinfo->ApiName = strdup(name);
	hinfo->preAlignBytes = CountPreAlignBytes( (BYTE*)OriginalFunction );
    hinfo->hookableBytes = HookableBytes( OriginalFunction );

	dbgmsg(1, "Hooking %s (0x%llx) -> 0x%llx, pre=%d avail=%d\n", hinfo->ApiName, hinfo->Function , hinfo->Hook , hinfo->preAlignBytes, hinfo->hookableBytes);

	if( ht == ht_auto ){
		if(!AutoChooseHookType(hinfo)){
			lastErrorCode = he_cantHook;
			dbgmsg(1, lastError);
			ZeroHookInfo(hinfo->index);
			return FALSE;
		}
		dbgmsg(1, "AutoChooseHookType selected %s for %s\n", hook_name[(int)hinfo->hooktype], hinfo->ApiName );
	}

	if( !ValidateHookType(hinfo) ){
		lastErrorCode = he_cantHook;
		dbgmsg(1, lastError);
		ZeroHookInfo(hinfo->index);
		return FALSE;
	}

	VOID *pBridge = CreateBridge(hinfo);

	if (pBridge == NULL){
		ZeroHookInfo(g_NumberOfHooks);
		return FALSE;
	}

	hinfo->Bridge = (ULONG_PTR) pBridge;
	hinfo->Enabled = true;

	OverWriteScratchPad((VOID *)OriginalFunction, hinfo); //make pad were going to overwrite all 0xCC for debugging sake..

	if(!WriteJump((VOID *) OriginalFunction, NewFunction, hinfo->hooktype, g_NumberOfHooks)){ //activates hook in api prolog..
		ZeroHookInfo(g_NumberOfHooks);
		return FALSE;
	}

	g_NumberOfHooks++; //now its complete..
	return TRUE;
}

stdc  
int __cdecl DisableHook(ULONG_PTR Function)
{
	HOOK_INFO *hinfo = GetHookInfoFromFunction(Function);
	if (hinfo)
	{
		if(hinfo->Enabled){
			hinfo->Enabled = false;
			WriteJump((VOID *)hinfo->Function, hinfo->Bridge, ht_jmp, hinfo->index);
			return 1;
		}
		return -1;
	}
	return -2;

}

stdc 
VOID __cdecl EnableHook(ULONG_PTR Function)
{
	HOOK_INFO *hinfo = GetHookInfoFromFunction(Function);
	if (hinfo)
	{
		if(!hinfo->Enabled){
			hinfo->Enabled = true;
			WriteJump((VOID *)hinfo->Function, hinfo->Hook, hinfo->hooktype, hinfo->index );
		}
	}
}

stdc
ULONG_PTR __cdecl GetOriginalFunction(ULONG_PTR Hook)
{
	if (g_NumberOfHooks == 0)
		return NULL;

	for (UINT x = 0; x < g_NumberOfHooks; x++)
	{
		if (g_HookInfo[x].Hook == Hook)
			return g_HookInfo[x].Bridge;
	}

	return NULL;
}
