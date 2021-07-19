import os
import argparse
import shutil
import xml.etree.ElementTree as ET



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_type", type=str, default='obj', help="The 3d model format(obj,stl,dae)")
    parser.add_argument("--model_name", type=str, help="The output of the gazebo model name")
    parser.add_argument("--author_name", type=str, default='Xinliang', help="The output of the gazebo model name")
    parser.add_argument("--author_email", type=str, default='xinliangzhong@foxmail.com', help="The output of the gazebo model name")
    args = parser.parse_args()
    print(args)

    if args.model_name == None:
        print('Please --model_name=Your_file_name')
        return
    
    cur_dir = os.getcwd()
    model_name = args.model_name

    print(cur_dir)
    print(model_name)

    sample_model_sdf = os.path.join(cur_dir,'sample/model.sdf')
    sample_model_config = os.path.join(cur_dir,'sample/model.config')
    
    # modofy model.sdf files
    sdf_tree = ET.parse(sample_model_sdf)
    sdf_tree_root = sdf_tree.getroot()

    for item in sdf_tree_root.iter():
        if(item.tag == 'model'):
            item.set('name', model_name)
        if(item.tag == 'uri'):
            print(item.text)
            text = 'model://' + model_name +'/meshes/' + model_name + '.' + args.model_type
            item.text = text
    
    ET.dump(sdf_tree_root)

    # modify model.config files
    config_tree = ET.parse(sample_model_config)
    config_tree_root = config_tree.getroot()

    cnt = 0
    for item in config_tree_root.iter():
        if(item.tag == 'description'):
            item.text = model_name
        if(item.tag == 'name' and cnt == 0):
            cnt = 1
            item.text = model_name
    
    ET.dump(config_tree_root)
    
    input_dir = os.path.join(cur_dir,'input')
    output_dir = os.path.join(cur_dir,'output/models')
    print(output_dir)

    obj_path = os.path.join(input_dir, model_name +'.obj')
    mtl_path = os.path.join(input_dir, model_name +'.mtl')
    texture_in_path = os.path.join(input_dir, model_name)
    if os.path.exists(obj_path) and os.path.exists(mtl_path):
        pass
    else:
        print('We can not find obj or mtl files')
        print(obj_path)
        print(mtl_path)
        return
    

    output_model_dir = os.path.join(output_dir, model_name)

    if os.path.exists(output_model_dir):
        shutil.rmtree(output_model_dir)
    

    meshs_dir = os.path.join(output_model_dir, 'meshes')
    if not os.path.exists(meshs_dir):
        print('xxxxx')
        os.makedirs(meshs_dir)

    texture_out_path = os.path.join(meshs_dir, model_name)
    if not os.path.exists(texture_out_path):
        os.makedirs(texture_out_path)
    
    sdf_tree.write(output_model_dir + '/model.sdf')
    config_tree.write(output_model_dir + '/model.config')

    shutil.copy(obj_path, meshs_dir)
    shutil.copy(mtl_path, meshs_dir)
    print(meshs_dir)
    if os.path.exists(texture_in_path):
        print(texture_in_path)
        print(meshs_dir)
        # shutil.copytree(texture_in_path, meshs_dir)
        for root, dirs, files in os.walk(texture_in_path, topdown=False):
            for name in files:
                print(os.path.join(root, name))
                filepath=os.path.join(root, name)
                print(filepath)
                shutil.copy(filepath,texture_out_path)
                print(texture_out_path)

if __name__ == '__main__':
    main()