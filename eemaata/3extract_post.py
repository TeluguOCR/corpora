#! /usr/bin/env python3
import re, os
from bs4 import BeautifulSoup

def unhtml(html):
    """    Remove HTML from the text.    """
    html = re.sub(r'(?i)&nbsp;',                    ' ',  html)
    html = re.sub(r'(?i)&amp;',                     '&',  html)
    html = re.sub(r'(?i)&gt;',                      '>',  html)
    html = re.sub(r'(?i)&lt;',                      '<',  html)    
    html = re.sub(r'(?i)&quot;',                    '"',  html)    
    html = re.sub(r'&#8220;',                       '“',  html)
    html = re.sub(r'&#8221;',                       '”',  html)
    html = re.sub(r'&#8217;',                       '’',  html) 
    html = re.sub(r'(?i)<br[ \/]*>',                '\n', html)
    html = re.sub(r'(?s)<!--.*?--\s*>',             ' ',   html)
    html = re.sub(r'(?i)<ref[^>]*>[^>]*<\/ ?ref>',  ' ',   html)
    html = re.sub(r'(?s)<.[^<]*?>',                 ' ',   html)
    return html

def unspace(text):
    """     Remove Arbitrary Spaces    """
    text = re.sub(r'(?s)\r\n|\r',  '\n', text)
    text = re.sub(r'\t',            ' ', text)
    text = re.sub(r'  +',           ' ', text)
    text = re.sub(r'(?m)^ +',        '', text)
    text = re.sub(r'(?m) +$',        '', text)
    text = re.sub(r'(?s)\n+',      '\n', text)
    return text

fout = open("e_dump.txt", "w")
file_list = os.listdir("articles")
for file_name in sorted(file_list):
    with open("articles/"+file_name, 'r') as f:
        print(file_name, end=" ")
        try:
            soup = BeautifulSoup(f.read())
            title = soup.find("h3", "posttitle")
            if title is None : print("Title NOT FOUND")
            post = soup.find("div", "postentry")
            if post is None : print("Postentry NOT FOUND")
        except :
            print("Error Parsing", file_name, " : ", sys.exc_info()[0])
        else:
            title = unspace(unhtml(str(title)))
            post = unspace(unhtml(str(post)))
            fout.write(title)
            fout.write('\n')
            fout.write(post)
            fout.write('\n')
        print()
fout.close()