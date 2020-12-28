import json, bcrypt, os, dotenv, datetime
from cryptography.fernet import Fernet

basedir = os.path.abspath(os.path.dirname(__file__))
dotenv.load_dotenv(os.path.join(basedir, '.env'))
secretKey = os.environ.get('SECRET_KEY')

def makeHtml(template,content):
    html=template
    html=html.replace("<!-- #header# -->",str(content["instance"]))
    html=html.replace("#datenow#",str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')))
    for item in content["itens"]:
        html=html.replace("<!-- #navbarItem# -->",str(f"""<a class="nav-link"  href="#{item["id"]}">{item["header"]}</a>\n<!-- #navbarItem# -->"""))
        html=html.replace("<!-- #content# -->",str(convertTabletoHtml(item)))
    return html

def convertTabletoHtml(contentJson):
    html=f"""<h2 id="{contentJson["id"]}">{contentJson["header"]}</h2>"""
    html+="""<table class='table table-success'>\n"""
    html+="<tr>\n"
    for column in contentJson["column"]:
        html+=f"<th>{column}</th>\n"
    html+="</tr>\n"
    
    for row in contentJson["data"]:
        html+="<tr class='table-light'>\n"
        for value in row:
            html+=f"<td>{str(value)}</td>\n"
        # html+="<td>"+row+"</td>"
        html+="</tr>\n"
    html+="</table><br>\n"
    html+="<!-- #content# -->"
    return html

def getJson(file):
    jsonData = {}
    try:
        jsonFile = open(file,'r')
        jsonData = json.load(jsonFile)
        jsonFile.close()
    except:
        print("error")
    return jsonData

def generateKey():
    return Fernet.generate_key().decode()

def decrypt(text):
    try:
        return Fernet(secretKey).decrypt(text.encode()).decode()
    except:
        return text

def crypt(text):
    if text != decrypt(text):
        return text
    else:
        return Fernet(secretKey).encrypt(text.encode()).decode()