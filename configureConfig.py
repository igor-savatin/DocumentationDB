import json, os, sys

from tools import getJson,crypt,generateKey

def createCfg(file,templateFile):
    try:
        if os.path.isfile(file) == False:
            instance=getJson(templateFile)
            try:
                with open(file, "w") as fp:
                    json.dump(instance, fp, indent=4)
            except OSError:
                print("Error of create config files example."),
                sys.exit(1)
    except OSError:
        print(f"Error of creation: {file}")
        sys.exit(1)

def validadeInvalidCommands(configCfgQuery):
    try:
        file=getJson(configCfgQuery)
        for db in file:
            for query in file[db]:
                if 'insert' in query['query'].lower():
                    print("============================================================================================")
                    print(f"Verify {configCfgQuery}, because exist insert in string:")
                    print(f"ID: {query['id']} / query: {query['query']}")
                    sys.exit(1)
                elif 'update' in query['query'].lower():
                    print("============================================================================================")
                    print(f"Verify {configCfgQuery}, because exist update in string:")
                    print(f"ID: {query['id']} / query: {query['query']}")
                    sys.exit(1)
                elif 'delete' in query['query'].lower():
                    print("============================================================================================")
                    print(f"Verify {configCfgQuery}, because exist delete in string:")
                    print(f"ID: {query['id']} / query: {query['query']}")
                    sys.exit(1)
                elif 'merge' in query['query'].lower():
                    print("============================================================================================")
                    print(f"Verify {configCfgQuery}, because exist merge in string:")
                    print(f"ID: {query['id']} / query: {query['query']}")
                    sys.exit(1)
                elif 'drop' in query['query'].lower():
                    print("============================================================================================")
                    print(f"Verify {configCfgQuery}, because exist drop in string:")
                    print(f"ID: {query['id']} / query: {query['query']}")
                    sys.exit(1)
    except OSError:
        print("Verify config files")
        sys.exit(1)


def validateCfg(configCfgInstance,configCfgQuery):
    try:
        if os.path.isfile(configCfgInstance) and os.path.isfile(configCfgQuery):
            db=getJson(configCfgInstance)
            query=getJson(configCfgQuery)
            for instance in db["instance"]:
                if instance["name"]==None:
                    raise Exception("Name of instance null")
                if instance["ip"]==None:
                    raise Exception("ip of instance null")
                if instance["instanceType"].lower()!="oracle" \
                    and instance["instanceType"].lower()!="mssql" \
                    and instance["instanceType"].lower()!="sqlserver" \
                    and instance["instanceType"].lower()!="sql server":
                    raise Exception("Verify param instance (remember set oracle or mssql)")
                if instance["user"]==None:
                    raise Exception("User of instance null") 
                if instance["password"]==None:
                    raise Exception("Password of instance null")
                if instance["connectionString"]==None:
                    raise Exception("Connection String of instance null")
                try:
                    for queryId in instance["query"]:
                        queryString=list(filter(lambda q: q["id"].lower() == queryId, query[instance["instanceType"].lower()]))[0]
                except:
                    print(f"""Verify Query {queryId} of instance {instance["name"]}""")
                    sys.exit(1)
        if not os.path.isfile(configCfgInstance) or not os.path.isfile(configCfgQuery):
            if not os.path.isfile(configCfgInstance):
                print("Instance File does not exist!")
                createCfg(configCfgInstance , './template/instance.json')
                print(f"Was created one example file, please edit the file {configCfgInstance}.")
            if not os.path.isfile(configCfgQuery):
                print("Query File File does not exist!")
                createCfg(configCfgQuery , './template/query.json')
                print(f"Was created one example file, please edit the file {configCfgQuery}.")
    except OSError:
        print("Verify config files")
        sys.exit(1)

def cryptPassword(instanceFile):
    try:
        instance=getJson(instanceFile)
        for i, row in enumerate(instance["instance"]):
            instance["instance"][i]["password"] = crypt(row["password"])
        # print(instance)
        try:
            with open(instanceFile, "w") as fp:
                json.dump(instance, fp, indent=4)
        except OSError:
            print("Error update password.")
            sys.exit(1)
    except:
        print("Erro crypt password")
        sys.exit(1)

def validadeEnvFile(file):
    if not os.path.exists(file):
        key=generateKey()
        print('oi')
        envFile=f"""SECRET_KEY="{key}"
CONFIG_PATH="config"
QUERY_FILE="query.json"
INSTANCE_FILE="instance.json"
REPORT_PATH="report" 
TEMPLATE_PATH="template"
"""
        print(envFile)

        f = open(file, "w")
        f.write(envFile)
        f.close()
        print("File .env created")


def checkCfg(instanceFile,queryFile):
    validadeEnvFile(".env")
    validateCfg(instanceFile,queryFile)
    validadeInvalidCommands(queryFile)
    cryptPassword(instanceFile)
