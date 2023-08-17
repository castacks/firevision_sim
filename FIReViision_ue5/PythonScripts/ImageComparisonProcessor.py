import pandas as pd
import ParametersClass as pc
import os

#Directory of test results folder
TEST_RESULTS_PATH = ""
IMAGES_PATH = os.path.join(TEST_RESULTS_PATH, "images")

#Directory of reference image
REFERENCE_IMAGEPATH = ""

#Directory of results output
OUTPUT_PATH = 'output/'

TEST_MODE = 1
TEST_NAME = pc.test_name(TEST_MODE)

def path_from_index(df, index):
    return df.loc[df['image_index'] == index]

def image_from_file(file):
    #TODO
    pass

def check_accuracy(test_image, reference_image):
    #TODO
    pass

def process_data(test_results_path, reference_imagepath, output_path, test_mode):
    data_df = pd.read_csv(test_results_path + "\\" + pc.test_name(test_mode) + "raw_data.xlsx")
    results_df = pd.DataFrame(columns=['accuracy', 'image_index'])
    
    #TODO: Get reference image
    reference_image = image_from_file(reference_imagepath + 'reference.png')
    
    for i in data_df.image_index:
        filepath = path_from_index(data_df, i) #gets file path
        image = image_from_file(filepath) #gets image from file path
        accuracy = check_accuracy(image, reference_image) #gets accuracy
        row = pd.Series({"accuracy": accuracy, "image_index": i}) #creates row
        
        pd.concat([results_df, row], ignore_index=True, in_place=True) #concats row to results_df

    # Merges results (with accuracies) and data (with params)
    results_df = results_df.merge(data_df, on='image_index')
    results_df.to_excel(output_path + "\\" + pc.test_name(test_mode) + "_results.xlsx", index=False)

def main():
    process_data(TEST_RESULTS_PATH, REFERENCE_IMAGEPATH, OUTPUT_PATH, TEST_MODE)
