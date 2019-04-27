#!/usr/bin/python3

import re
import bs4

import argparse



do_debug=False

def debug(*args, sep=' ', end='\n'):
    if do_debug:
        print("DEBUG ",end='')
        print(*args, sep=sep, end=end)
    else:
        pass


def loadhtmlfile(filename):
    #
    # _iwona_sadowska__polish_a_comprehensive_grammar_z_lib.org_.html
    f=open(filename)
    lines=f.readlines()
    f.close()
    

    html='\b'.join(lines)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    # https://www.crummy.com/software/BeautifulSoup/bs3/documentation.html#contents

    body=soup.body
    return body

fonts=[]


def get_font_from_attrs(attrs):
    xx="get_font_from_attrs"
    debug(xx,"attrs",attrs)
    ff=""
    if "class" in attrs:
        for attr in attrs['class']:
            if attr.startswith('ff'): # font family
                ff=attr
                debug(xx,"foundff",ff)          
    return ff

def pushfont(content):
    xx="pushfont"
    debug(xx,"content.attrs",content.attrs)
    ff=get_font_from_attrs(content.attrs)
    if ff:
        fonts.append(ff)
        
def popfont(content):
    xx="popfont"
    debug(xx,"content",content.attrs)
    ff=get_font_from_attrs(content.attrs)
    if ff:
        fonts.pop()
    
def printcontent(content,verbose,transtables):
    xx="printcontent"
    if len(fonts)>0:
        thefont=fonts[-1]
    else:
        thefont=""
    debug(xx,"this is a string",fonts,thefont,content)

    if thefont in transtables.keys():
        thetable=thefont
    else:
        thetable="default"
        
    txt=content    
    txt=txt.translate(transtables[thetable])
    if verbose:
        print('[',thefont,']',txt,sep='',end='')
    else:
        print(txt,sep='',end='')


def go_deep(start,verbose,transtables,depth):
    xx="go_deep"
    i=0
    for content in start.contents:
        if isinstance(content,bs4.NavigableString):
            printcontent(content,verbose,transtables)
        else:
            debug(xx,"content",depth,i,content.name,content.attrs)
            pushfont(content)
            go_deep(content,verbose,transtables,depth+1)
            popfont(content)
            debug(xx,"tag",content.name)
            if content.name=="div":
                print() # print a newline
        i=i+1
        
def convert_html2txt(htmlfile,transdata,verbose):
    """
    Main function to call
    """
    # DO NOT DELETE DEFAULT
    # get the transtables fro the transdata
    transtables={}
    for key,value in transdata.items():
        transtables[key]=str.maketrans(value)

    body=loadhtmlfile(htmlfile)
    go_deep(body,verbose,transtables,0)



    
def parse_cli():
    xx="parse_cli"
    parser = argparse.ArgumentParser(description="""Translates characters in HTMP fonts
""",formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('filename',help="The name of the HTML file")
    parser.add_argument('-v','--verbose', help="set verbose mode (show font names)",action="store_true")

    opts = parser.parse_args()
    debug(xx,"opts:",opts)
    return opts


# ==============================================
"""
Define your transdata
"""
# DO NOT DELETE DEFAULT
transdata={}

transdata['default']={}
transdata['ff14']={
    'a':'Ą',
    'b':'ą',
    'c':'Ę',
    'd':'ę',
    'e':'Ć',
    'f':'ć',
    'g':'Ń',
    'h':'ń',
    'i':'Ś',
    'j':'ś',
    'k':'Ź',
    'l':'ź',
    'm':'Ż',
    'n':'ż',
}

transdata['ff19']=transdata['ff14']

transdata['ff17']={ # IPA
    
    'a':'Ą',
    'b':'ą',
    'c':'Ę',
    'd':'ę',
    'e':'Ć',
    'f':'ć',
    'g':'Ń',
    'h':'ń',
    'i':'Ś',
    'j':'ś',
    'k':'Ź',
    'l':'ź',
    'm':'Ż',
    'n':'ż',
    
    'I':'t͡s',
    'J':'t͡ɕ',
    # 'z':'ɛ̃',
    'y':'ɛ̃',
    'z':'ɛ',
    'q':'ɲ',
    'w':'ɔ',
    'ś':'ɕ',
    'L':'ks',
    'v':'ɨ',
    't':'ʑ',
    'p':'ʐ',
    'J':'t͡ɕ',
    'o':'t͡ʂ',
    'K':'d͡ʑ',
    't':'ʑ',
    'x':'ɔ̃',
    'u':'ɕ',
}
transdata['ff1a']=transdata['ff17']
transdata['ff1b']={
    ' ':'',
}

    
    
if __name__ == "__main__":
    opts=parse_cli()
    verbose=opts.verbose
    htmlfile=opts.filename
    convert_html2txt(htmlfile,transdata,verbose)
