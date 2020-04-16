import yaml
import glob
import json


with open("/Users/nakamura/Downloads/cj.json") as f:
    data = json.load(f)

    manifests = data["manifests"]

    licenses = {}
    attributions = {}

    for manifest in manifests:

        #################

        '''

        attribution = ""
        
        if "attribution" in manifest:
            attribution = manifest["attribution"]
    
        if attribution not in attributions:
            attributions[attribution] = 0

        attributions[attribution] += 1

        '''

        #################

        license = manifest["license"]

        if license not in licenses:
            licenses[license] = 0
        licenses[license] += 1

    #################

    # print(licenses)
    for license in licenses:
        print(license+"\t"+str(licenses[license]))
        print("----------------------")
    # print(atributions)

    #################

    for license in attributions:
        print(license+"\t"+str(attributions[license]))
        print("----------------------")

    #################

    print(len(manifests))