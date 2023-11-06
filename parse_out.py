import re

def extract(list: list, case=0) -> list:
    data = []
    LUT = None
    with open("Output/Turbojet.out", 'r') as file:
        file.readline();file.readline()
        for line in file:
            line = re.split(r'\s+', line)
            if len(line) == 0:
                continue
            if LUT == None:
                LUT = {}
                index = -2
                for x in line:
                    LUT[x] = index
                    index += 1
            else:
                temp = []
                for x in line:
                    x = x.removesuffix('+')
                    try:
                        temp.append(float(x))
                    except:
                        temp.append(x)
                data.append(temp)
    result = []
    for x in list:
        result.append(data[case][LUT[x]])
    return result

if __name__ == "__main__":
    print(extract(["Tt4[K]", "Eta_Thermal"]))