from module.speech_recognition.rec_audio import speech_recognition

import os
import json

# chemin vers le dossier de test
TESTPATH = "./speech_recognition/test/test-set/"
test_folders_list = os.listdir(TESTPATH)

print(test_folders_list)

# Variables pour stocker le nombre de bonnes et de mauvaises prévisions 
good_prev_number = 0
bad_prev_number = 0

# # Liste pour stcoker les noms des recs qui ont mal été prédit 
# good_prev_list = []
# bad_prev_list = []

# On boucle sur tous les dossiers qui se trouve dans le dossier "test-set"
for folder in test_folders_list:
    # current_json_path = TESTPATH + folder + "/" + "answers.json"

    # On ouvre le fichier answers.json du dossier actuel => Un fichier answer.json par dossier 
    json_file = open(TESTPATH + folder + "/" + "answers.json")
    # On stocke les infos de ce fichier 
    current_json_data = json.load(json_file)[0]
    # print(current_json_data)
    print(f'---{folder}----')

    # On boucle sur les fichiers qui sont dans le dossier actuel 
    for item in os.listdir(TESTPATH + folder):

        # Si ce n'est pas le fichier json on va lire le record
        if item != "answers.json":

            # print(item)
            # print(current_json_data)
            # current_item = {}

            # On cherche le nom du fichier dans le fichier json
            current_item = [element for element in current_json_data["recList"] if element['name'] == os.path.splitext(item)[0]][0]
            # for element in current_json_data["recList"]:
            #     # print(element)
            #     if element["name"] == os.path.splitext(item)[0]:
            #         current_item = element
            #         break

            path_to_current_file = TESTPATH + folder + "/" + item
            # On passe le record et le mot qui doit être prononcé dans la méthode du speech to text
            result = speech_recognition(path_to_current_file, current_json_data["word"])

            # Si la réponse du speech to text correspond à celle attendue on augmente la variable "good_prev_number" 
            if result.getPrononciation() == current_item["goodPrononciation"]:
                good_prev_number += 1
            # Si la réponse du speech to text diffère de celle attendue on augmente la variable "bad_prev_number" 
            else:
                print("Bad guess => ", result.getPrononciation(), current_item["goodPrononciation"], "| Enregistrement concerné => " + current_item["name"])
                # print("Resume: " + result.getDetectedWord())
                bad_prev_number += 1

print(good_prev_number / (good_prev_number + bad_prev_number) * 100)