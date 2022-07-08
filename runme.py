import json
import os


def read_json(input_file):
    config_file = open(input_file)
    try:
        config_data = json.load(config_file)
    except:
        quit()
    config_file.close()
    return config_data


def build_command_string(config_data):
    command_string = './aws_signing_helper credential-process'
    command_string += ' --certificate '+ config_data['certificate_file']
    command_string += ' --private-key '+ config_data['certificate_key']
    command_string += ' --trust-anchor-arn '+'arn:aws:rolesanywhere:'+config_data['Region']+':'+config_data['AccountID']+':trust-anchor/'+config_data['AnchorID']
    command_string += ' --profile-arn '+'arn:aws:rolesanywhere:'+config_data['Region']+':'+config_data['AccountID']+':profile/'+config_data['ProfileID']
    command_string += ' --role-arn '+'arn:aws:iam::'+config_data['AccountID']+':role/'+config_data['RoleName']
    command_string +=  '| jq . > ./anywhere.creds'
    return(command_string)


def define_exports(ex_type, ex_value):
    printme = ex_type + "=\""+ ex_value+"\""
    print(printme)
    return 0


def print_exports(creds):
    values = [
        ['AWS_ACCESS_KEY_ID','AccessKeyId'],
        ['AWS_SECRET_ACCESS_KEY','SecretAccessKey'],
        ['AWS_SESSION_TOKEN','SessionToken']
            ]
    for x in values:
        define_exports(x[0],creds[x[1]])
    return 0



os.system(build_command_string(read_json('./config.json')))
print_exports(read_json('./anywhere.creds'))
