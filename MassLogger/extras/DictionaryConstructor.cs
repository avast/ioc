Dictionary<int, int> dictionary = new Dictionary<int, int>();
BinaryReader binaryReader = new BinaryReader(Type.GetTypeFromHandle(YMn.GetRuntimeTypeHandleFromMetadataToken(33554549)).Assembly.GetManifestResourceStream("XT7N54yDEN8FnpdpZs.npkuPXFrtOPP8sUvPf"));
binaryReader.BaseStream.Position = 0L;
byte[] array = binaryReader.ReadBytes((int)binaryReader.BaseStream.Length);
binaryReader.Close();
if (array.Length > 0)
{
    int num = array.Length % 4;
    int num2 = array.Length / 4;
    byte[] array2 = new byte[array.Length];
    uint num3 = 0U;
    if (num > 0)
    {
        num2++;
    }
    for (int i = 0; i < num2; i++)
    {
        int num4 = i * 4;
        uint num5 = 255U;
        int num6 = 0;
        uint num7;
        if (i == num2 - 1 && num > 0)
        {
            num7 = 0U;
            for (int j = 0; j < num; j++)
            {
                if (j > 0)
                {
                    num7 <<= 8;
                }
                num7 |= (uint)array[array.Length - (1 + j)];
            }
        }
        else
        {
            uint num8 = (uint)num4;
            num7 = (uint)((int)array[(int)((UIntPtr)(num8 + 3U))] << 24 | (int)array[(int)((UIntPtr)(num8 + 2U))] << 16 | (int)array[(int)((UIntPtr)(num8 + 1U))] << 8 | (int)array[(int)((UIntPtr)num8)]);
        }
        num3 = num3;
        uint num9 = num3;
        uint num10 = num3;
        uint num11 = 1795577737U;
        uint num12 = 1182509082U;
        uint num13 = num10;
        uint num14 = 1406428146U;
        uint num15 = 526153867U;
        uint num16 = (num11 >> 11 | num11 << 21) ^ num14;
        uint num17 = num16 & 16711935U;
        num16 &= 4278255360U;
        num11 = (num16 >> 8 | num17 << 8);
        uint num18 = 3007391072U;
        num18 = 56678U * (num18 & 65535U) + (num18 >> 16);
        num11 = 37629U * (num11 & 65535U) - (num11 >> 16);
        num11 = 25451U * num11 - num18;
        ulong num19 = (ulong)(num11 * num11);
        if (num19 == 0UL)
        {
            num19 -= 1UL;
        }
        num14 = (uint)((ulong)(num14 * num14) % num19);
        num18 = 29546U * (num18 & 65535U) + (num18 >> 16);
        num11 = 21832U * (num11 & 65535U) + (num11 >> 16);
        num11 = 7417U * num11 + num18;
        num13 ^= num13 >> 11;
        num13 += num12;
        num13 ^= num13 << 17;
        num13 += num14;
        num13 ^= num13 >> 13;
        num13 += num15;
        num13 = ((num18 << 16) - num14 ^ num12) + num13;
        num3 = num9 + (uint)num13;
        if (i == num2 - 1 && num > 0)
        {
            uint num20 = num3 ^ num7;
            for (int k = 0; k < num; k++)
            {
                if (k > 0)
                {
                    num5 <<= 8;
                    num6 += 8;
                }
                array2[num4 + k] = (byte)((num20 & num5) >> num6);
            }
        }
        else
        {
            uint num21 = num3 ^ num7;
            array2[num4] = (byte)(num21 & 255U);
            array2[num4 + 1] = (byte)((num21 & 65280U) >> 8);
            array2[num4 + 2] = (byte)((num21 & 16711680U) >> 16);
            array2[num4 + 3] = (byte)((num21 & 4278190080U) >> 24);
        }
    }
    array = array2;
    int num22 = array.Length / 8;
    massCrypto.VMt vmt = new massCrypto.VMt(new MemoryStream(array));
    for (int l = 0; l < num22; l++)
    {
        int key = vmt.ReadInt32();
        int value = vmt.ReadInt32();
        dictionary.Add(key, value);
    }
    vmt.Close();
}
massCrypto.FieldMethodDictionary = dictionary;
