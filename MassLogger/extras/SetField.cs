ParameterInfo[] parameters = methodInfo.GetParameters();
int num24 = parameters.Length + 1;
Type[] array3 = new Type[num24];
if (methodInfo.DeclaringType.IsValueType)
{
    array3[0] = methodInfo.DeclaringType.MakeByRefType();
}
else
{
    array3[0] = Type.GetTypeFromHandle(YMn.GetRuntimeTypeHandleFromMetadataToken(16777235));//T:System.Drawing.Imaging.ImageCodecInfo
}
for (int n = 0; n < parameters.Length; n++)
{
    array3[n + 1] = parameters[n].ParameterType;
}
DynamicMethod dynamicMethod = new DynamicMethod(string.Empty, methodInfo.ReturnType, array3, typeFromHandle, true);
ILGenerator ilgenerator = dynamicMethod.GetILGenerator();
for (int num25 = 0; num25 < num24; num25++)
{
    switch (num25)
    {
    case 0:
        ilgenerator.Emit(OpCodes.Ldarg_0);
        break;
    case 1:
        ilgenerator.Emit(OpCodes.Ldarg_1);
        break;
    case 2:
        ilgenerator.Emit(OpCodes.Ldarg_2);
        break;
    case 3:
        ilgenerator.Emit(OpCodes.Ldarg_3);
        break;
    default:
        ilgenerator.Emit(OpCodes.Ldarg_S, num25);
        break;
    }
}
ilgenerator.Emit(OpCodes.Tailcall);
ilgenerator.Emit(flag2 ? OpCodes.Callvirt : OpCodes.Call, methodInfo);
ilgenerator.Emit(OpCodes.Ret);
fieldInfo.SetValue(null, dynamicMethod.CreateDelegate(typeFromHandle));
