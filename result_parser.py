import json
from pathlib import Path
import zipfile
import os

extrated_files_path = "./results"
    
#zip_file_path = output_relatorios
def parse_results(zip_file_path):
    """
    Creates a JSON file ease to transform later in table 
      given the path to the results file 
    
    PARAMS:
        zip_file_path - path to the zipfile containing the results
        json_file_path - path to put the final json file
    """

    # Stores the extrated data
    extracted_data = []
    # extracts the directories
    directories = []

    # Iterate over all files and directories recursively
    for path in Path(zip_file_path).rglob("*.zip"):  # rglob("*") recursively gets all files and directories
        directories.append(path)
    
    for path in directories:
        # Open and extract all files to the specified extrated_files_path
        json_files = extractFiles(path, extrated_files_path)
        # extract the course from the path 
        curso = str(os.path.normpath(path).split(os.path.sep)[-2])
        
        # Iterate extrated files 
        for file_name in json_files:
        
            # Ignores the files 'options', 'overview' and 'submissionFileIndex'
            insertsData(curso, file_name, extracted_data)
                
    # Clears the files on output directory
    removefiles('./results')

    # Creates a file named mydata.json
    json_file_path = "results/mydata.json"
    
    with open(json_file_path, "w") as final:
        # Serializes obj to JSON 
        json.dump(extracted_data, final)
        


def insertsData(curso, file_name, extracted_data):
    # Creates the full path to file
    file_path = os.path.join(extrated_files_path, file_name)  
    if file_name not in {"options.json", "overview.json", "submissionFileIndex.json"}: 
        try:
            #Inserts data
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                id1 = divideString(data["id1"],0)
                id2 = divideString(data["id2"],0)
                max_value = data.get('similarities').get('MAX', '')
                tipo_avaliacao = divideString(file_path,1)
                exercicio = divideString(data["id1"],2)[:-5]
            
                # Appends to the extracted_data the json of the current comparison (max value)
                extracted_data.append(
                {'curso':curso,
                'tipo':tipo_avaliacao,
                'exercicio': exercicio,
                'aln1':id1,
                'aln2':id2, 
                'indicePlagio':max_value})
                
        except Exception as e:
            print(f"Error processing {file_name}: {e}")

        
def removefiles(folder_path):
    # Loop through all files in the folder and remove them
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        os.remove(file_path)
        
        
        
def extractFiles(path,extrated_files_path):
    with zipfile.ZipFile(path, 'r') as zip_ref:

        # List all files path of the extrated_files_path that end with ".json"
        json_files = [f for f in zip_ref.namelist() if f.endswith('.json')]
       
        # Extract all json files on results
        for json_file in json_files:
            zip_ref.extract(json_file, extrated_files_path)

        print(f"Files extracted to {extrated_files_path}")
        
    return json_files



def divideString(textoADividir, i):
    output = textoADividir.rsplit('_')
    return output[i]
    
        
