import os
import random
import shutil


# could provide top level dir and just append "text" or "image" to have less func parameters
def copy_train_data(source_text_dir, source_image_dir, out_train_text_dir, out_train_image_dir, file_names, split_point):
    # Iterate through the file names and move them to train
    for file_name in file_names[:split_point]:
        try:
            shutil.copy2(os.path.join(source_text_dir, file_name), os.path.join(out_train_text_dir, file_name))
            shutil.copy2(os.path.join(source_image_dir, file_name[:-4]+".jpg"), os.path.join(out_train_image_dir, file_name[:-4]+".jpg"))
        except:
            print("Could not copy files: " + file_name)
            continue

def copy_test_data(source_text_dir, source_image_dir, out_test_text_dir, out_test_image_dir, file_names, split_point):
    for file_name in file_names[split_point:]:
        try:
            shutil.copy2(os.path.join(source_text_dir, file_name), os.path.join(out_test_text_dir, file_name))
            shutil.copy2(os.path.join(source_image_dir, file_name[:-4]+".jpg"), os.path.join(out_test_image_dir, file_name[:-4]+".jpg"))
        except:
            print("Could not copy files: " + file_name)
            continue



def split_data_pipe(source_dir, output_dir, split, seed):
    # SPLIT = 0.8
    # TOP_PATH = "C:\\Users\\multimaster\\Desktop\\Final_dataset_11_13_23\\11_13_23\\original_data"
    # OUTPUT_DIR = "C:\\Users\\multimaster\\Desktop\\Final_dataset_11_13_23\\11_13_23\\original_data"
    # Set a seed for reproducibility
    random.seed(seed)

    # Set the source directories
    source_text_dir = source_dir + "\\labels"
    source_image_dir = source_dir + "\\images"


    # Set the destination directories
    out_train_text_dir = output_dir + "\\train\\labels"
    out_train_image_dir = output_dir + "\\train\\images"
    out_test_text_dir =  output_dir + "\\test\\labels"
    out_test_image_dir = output_dir + "\\test\\images"

    os.makedirs(out_train_text_dir,exist_ok=True)
    os.makedirs(out_train_image_dir,exist_ok=True)
    os.makedirs(out_test_text_dir,exist_ok=True)
    os.makedirs(out_test_image_dir,exist_ok=True)


    # Get a list of file names in the text folder (assuming the names match the image files)
    file_names = os.listdir(source_text_dir)

    # Randomly shuffle the file names using the seeded random function
    random.shuffle(file_names)

    # Calculate the split point based on an split/1-split ratio ex: 80/20
    split_point = int(split * len(file_names))

    copy_train_data(source_text_dir, source_image_dir, out_train_text_dir, out_train_image_dir, file_names, split_point)
    copy_test_data(source_text_dir, source_image_dir, out_test_text_dir, out_test_image_dir, file_names, split_point)

    return 1



def kfold_data(source_dir, output_dir, k, split, seed):
    random.seed(seed)

    # Set the source directories
    source_text_dir = source_dir + "\\labels"
    source_image_dir = source_dir + "\\images"

    # Get a list of file names in the text folder (assuming the names match the image files)
    file_names = os.listdir(source_text_dir)


    # Randomly shuffle the file names using the seeded random function
    random.shuffle(file_names)

    # Calculate the split point based on an split/1-split ratio ex: 80/20
    fold_size = len(file_names)// k

    # Calculate the split point based on an split/1-split ratio ex: 80/20
    split_point = int(split * len(file_names))

    subset_files = [file_names[i*fold_size:(i+1)*fold_size] for i in range(k)]

    for i in range(1, k+1):


        # Set the destination directories
        out_train_text_dir = output_dir + f"\\{i}\\train\\labels"
        out_train_image_dir = output_dir + f"\\{i}\\train\\images"
        out_test_text_dir =  output_dir + f"\\{i}\\test\\labels"
        out_test_image_dir = output_dir + f"\\{i}\\test\\images"

        os.makedirs(out_train_text_dir, exist_ok=True)
        os.makedirs(out_train_image_dir, exist_ok=True)
        os.makedirs(out_test_text_dir, exist_ok=True)
        os.makedirs(out_test_image_dir, exist_ok=True)

        copy_train_data(source_text_dir, source_image_dir, out_train_text_dir, out_train_image_dir, subset_files[i], split_point)
        copy_test_data(source_text_dir, source_image_dir, out_test_text_dir, out_test_image_dir, subset_files[i], split_point)
