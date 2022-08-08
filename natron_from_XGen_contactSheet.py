"""Natron XGen Contact sheet script"""
import os


# USER / FUNCTION INPUT
source_path = "G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/"
template_path = "0000_base_delta/template/"
template_name = "natron_template.ntp"
groom_path = template_path
seq_path = "G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/SimonYuen/maya/base_delta/images/dh_coil_8.2c1.0r_dh_coil_8.2c8.2r_dh_exp_gScale_2.1_dh_exp_gScale_4.5/"


# Calculated INPUT
path_to_template = source_path+template_path+template_name


def get_seq_name(seq_path, file_ext:str = ".png"):
    """reads path and outputs formatted sequence file name"""
    seq_name = ["{}.#{}".format(x.split(".")[0], file_ext) for x in os.listdir(seq_path) if x.endswith(file_ext)]
    if len(set(seq_name)) == 1:
        return seq_name[0]
    else:
        print("error in naming: Clean directory before proceeding.")


def file_read(path):
    """ READ NATRON TEMPLATE.NTP """
    with open(path, 'r') as f:
        return f.read()


def file_create(path, data):
    """ WRITE NEW TEMPLATE"""
    with open(path, 'w') as f:
        f.write(data)


def get_seq_len(seq_path, file_ext:str = ".png"):
    return len([x for x in os.listdir(seq_path) if x.endswith(file_ext)])


def natron_write(seq_path, rows:int=1, columns:int=1, resolution:int=500):
    """ READ, MODIFY, WRITE; NEW TEMPLATE"""
    tokens =  {
        "@@@seq_path@@@" : seq_path, 
        "@@@seq_name@@@" : get_seq_name(seq_path), 
        "@@@seq_length@@@" : str(get_seq_len(seq_path)), 
        "@@@array_write_path@@@" : seq_path, 
        "@@@rows@@@" : str(rows), 
        "@@@columns@@@" : str(columns),
        "@@@resHeight@@@" : str(rows*resolution), 
        "@@@resWidth@@@" : str(columns*resolution),
    }
    print(path_to_template)
    data = file_read(path_to_template)
    for k,v in tokens.items():
        print(k,v)
        data = data.replace(k, v)
    out_template = seq_path+"natron_out.ntp"
    file_create(out_template, data)
    print("created ", out_template)
    from subprocess import check_output
    check_output('"C:/Program Files/Natron/bin/NatronRenderer.exe" "{}" -w Write1'.format(out_template), shell=True)






# natron_write(seq_path, 2, 2)