import logging, os, json, dotenv, datetime

from configureConfig import checkCfg,validadeEnvFile
from tools import getJson,makeHtml
from database import connectOracle,connectMSSQL


def generateReport(instance,query,templatePath,reportPath):
    logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO,datefmt="%H:%M:%S")
    logging.info("Start")
    """Files de config"""
    db=getJson(instance)
    query=getJson(query)
    pageIndex = open(f"{templatePath}/index.html","r").read()
    dirFile = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    for instance in db["instance"]:
        response = {}
        itens = []
        template = open(f"{templatePath}/report.html","r").read()
        """Nome da instancia"""
        response["instance"] = instance["name"]
        logging.info(f"""Processando instância: {instance["instanceType"]} - {instance["name"]}""")
        logging.info("Executando query:")        
        """loop das querys para cada instancia"""
        for queryId in instance["query"]:
            queryString=""
            """encontrando a query string"""
            instanceType = instance["instanceType"].lower()
            queryString=list(filter(lambda x: x["id"].lower() == queryId, query[instanceType]))[0]
            logging.info(f""" - {queryString["header"]}""")
            """validando a tecnologia do banco"""
            if instanceType == "oracle":
                output=connectOracle(instance["user"], instance["password"], instance["connectionString"], queryString["query"])
            elif instanceType == "mssql":
                output=connectMSSQL(server = instance["connectionString"],database = instance["database"],username = instance["user"],password = instance["password"], query = queryString["query"])
            output["header"] = queryString["header"]
            output["id"] = queryString["id"]
            itens.append(output)
            response['itens'] = itens
        fileHtml=makeHtml(template,response)
        try:
	        if not os.path.exists(f"{reportPath}/{dirFile}"):
        		os.mkdir(f"{reportPath}/{dirFile}")
        except OSError:
            print(f"Creation of the directory {reportPath}/{dirFile} failed")
        nameFile=f"""{str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))}_{instance["name"]}_{instance["type"]}"""
        pageIndex = pageIndex.replace("<!-- #line# -->",f"""<tr class='table-light'>\n<td>{instance["name"]}</td>\n<td>{instance["ip"]}</td>\n<td>{instance["instanceType"]}</td>\n<td>{instance["type"]}</td>\n<td>{instance["user"]}</td>\n<td>{instance["connectionString"]}</td>\n<td><a href="{nameFile}.html">{nameFile}<a></td>\n</tr>\n<!-- #line# -->""")
        pageIndex = pageIndex.replace("#datenow#",str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')))
        open(f"{reportPath}/{dirFile}/01_index.html","w").write(pageIndex)
        open(f"{reportPath}/{dirFile}/{nameFile}.html","w").write(fileHtml)
    logging.info("end")
    print(f"\nReport gerated {reportPath}\{dirFile}\01_index.html")
    

def main():
    print("""*********************************************************************************""")
    print("""*                                                                               *""")
    print("""*                                Documentation                                  *""")
    print("""*                                                                               *""")
    print("""*********************************************************************************""")
    print("")
    validadeEnvFile(".env")
    """Load variables"""
    basedir = os.path.abspath(os.path.dirname(__file__))
    dotenv.load_dotenv(os.path.join(basedir, '.env'))
    configPath = os.path.abspath(os.environ.get('CONFIG_PATH'))
    queryFile = f"{configPath}\{os.environ.get('QUERY_FILE')}"
    instanceFile = f"{configPath}\{os.environ.get('INSTANCE_FILE')}"
    reportPath = os.path.abspath(os.environ.get('REPORT_PATH'))
    templatePath = os.path.abspath(os.environ.get('TEMPLATE_PATH'))
    # secretKey = os.environ.get('SECRET_KEY')
    print(f"Paths Default:\n Instance File: {instanceFile} \n Query File: {queryFile} \n Report Path: {reportPath} \n Template Path: {templatePath}")
    checkCfg(instanceFile,queryFile)
    # generateReport(instance = instanceFile
    # ,query=queryFile
    # ,templatePath=templatePath
    # ,reportPath = reportPath)

if __name__ == "__main__":
    main()