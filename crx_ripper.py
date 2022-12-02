import requests
import argparse, sys
import zipfile



chromeversion="108.0.5359.71"
extensionid=""
outputfile="mycrx.crx"
url = ""
payload={}
headers = {}

#response = requests.request("GET", url, headers=headers, data=payload)
def parseArgv():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    
    group.add_argument("-q", "--quiet", action="store_true", help = "Run quietly")
    crxidentifier = parser.add_mutually_exclusive_group(required=True)
    crxidentifier.add_argument("-u", "--url", help = "The URL of the extension")
    crxidentifier.add_argument("-i", "--id", help = "The ID of the extension")
    parser.add_argument("-o", "--output", help = "Name of the output file")
    parser.add_argument("-cv","--chromeversion",help = "The chrome version to download, default is 108.0.5359.71")
    if len(sys.argv) == 1:
        parser.print_help()
    args, leftover = parser.parse_known_args()
    
    global extensionid
    if args.id is not None:
       extensionid = args.id
    else:
        extensionid = (args.url.split("/"))[-1] 
    global outputfile
    if args.output is not None:
        outputfile = args.output
    else:
        outputfile = extensionid + ".crx"
    global chromeversion
    if args.chromeversion is not None:
        chromeversion = args.chromeversion

    global url
    url = "https://clients2.google.com/service/update2/crx?response=redirect&prodversion="+chromeversion+"&acceptformat=crx2,crx3&x=id%3D"+extensionid+"%26uc"
    
    if args.quiet is False:
        print("\textensionid: "+extensionid+"\n")
        print("\toutput file: "+outputfile+"\n")
        print("\tchromeversion:"+chromeversion+"\n")
        print("\tdownloadurl: " + url)
    attempt_fetch()
    attempt_unzip()
    

def attempt_fetch():
    #fetch the file
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        open(outputfile, 'wb').write(response.content)
    except Exception as inst:
        print(url)
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)   

def attempt_unzip():
    #uzip the file
    try: 
        with zipfile.ZipFile(outputfile, 'r') as zip_ref:
            zip_ref.extractall(extensionid)
    except Exception as inst:
        print(url)
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)   

if __name__ == '__main__':
    parseArgv()

