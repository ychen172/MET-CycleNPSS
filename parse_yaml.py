# This python file takes a yaml input and outputs into run.dat and arch.dat 
# the values in the order that the npss model expects.

import yaml

# These arrays match what keys go into each file, and *also define the order*
arch_keys = [
    "ambient.alt_in",
    "ambient.dTs_in",
    "ambient.MN_in",
    "inlet.W_in",
    "inlet.PqP_in",
    # "compressor.map",
    "compressor.PRdes",
    "compressor.effDes",
    "compressor.FL_I.MNdes",
    "fuel_start.LHV_in",
    "fuel_start.Wfuel",
    "burner.dPqP_dmd",
    "burner.effBase",
    "burner.FL_I.MNdes",
    # "turbine.map",
    "turbine.PRbase",
    "turbine.effDes",
    "turbine.FL_I.MNdes",
    "nozzle.FL_I.MNdes",
    "nozzle.dPqP",
    "shaft.Nmech",
    "shaft.HPX",
]
run_keys = [
    "thrust_des",
    "temp_ratio_des",
    "thrust_low_lim",
    "thrust_high_lim",
]

def main():
    with open('default.yaml', 'r') as file:
        data_object = yaml.safe_load(file)
    
    dictionary = {}
    for data_object_elem in data_object:
        parse_data_object(data_object_elem, dictionary)
    
    create_file("arch.dat", arch_keys, dictionary)
    create_file("run.dat", run_keys, dictionary)

def create_file(name, keys, dictionary):
    with open(name, 'w+') as file:
        for key in keys:
            if key in dictionary:
                file.write(str(dictionary[key]))
                file.write('\n')
            else:
                print("ERROR: Could not find key " + key + " in yaml file!")

def parse_data_object(object, result, base_key=""):
    for (key, element) in object.items():
        dict_key = base_key + key
        if isinstance(element, dict):
            parse_data_object(element, result, dict_key + ".")
        else:
            result[dict_key] = element

if __name__ == "__main__":
    main()