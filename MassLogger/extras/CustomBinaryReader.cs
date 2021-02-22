internal static int CustomBinaryReader(BinaryReader \u0020)
{
    bool flag = false;
    uint num = 0U;
    uint num2 = (uint)pXk.ReadByte(\u0020);
    int num3 = 0;
    
    num |= (num2 & 63U);
    if ((num2 & 64U) != 0U)
    {
        flag = true;
    }
    if (num2 < 128U)
    {
        if (flag)
        {
            return (int)(~(int)num);
        }
        return (int)num;
    }
    else
    {
        int num4 = 0;
        for (;;)
        {
            uint num5 = (uint)\u0020.ReadByte();
            num |= (num5 & 127U) << 7 * num4 + 6;
            if (num5 < 128U)
            {
                break;
            }
            num4++;
        }
        if (flag)
        {
            return (int)(~(int)num);
        }
        return (int)num;
    }
}
