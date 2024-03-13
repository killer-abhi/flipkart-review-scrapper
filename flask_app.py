from flask import Flask,render_template,request,jsonify
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app=Flask(__name__)


@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        searchString=request.form['content'].replace(" ","")
        
        flipkartUrl="https://www.flipkart.com/search?q="+searchString
        uClient=uReq(flipkartUrl)
        flipkartPage=uClient.read()
        uClient.close()
        flipkart_html=bs(flipkartPage,"html.parser")
        containers=flipkart_html.find_all("div",{"class":"_1AtVbE col-12-12"})
        del containers[0:3]
        mainContainer=containers[0]
        productLink="https://www.flipkart.com"+mainContainer.div.div.div.a['href']
        print(productLink)
        prodRes=requests.get(productLink)
        prod_html=bs(prodRes.text,"html.parser")
        commentContainer=prod_html.find_all("div",{"class":"_16PBlm"})
        del commentContainer[-1]
        reviews=[]
        for comment in commentContainer:
            commentTitle=comment.div.div.div.p.text
            print(commentTitle)
            mydict={
                "Product":"product",
                "Name":'X',
                "Rating":"4",
                "CommentHead":commentTitle,
                "Comment":"Hello"
            }
            reviews.append(mydict)
        
        print(reviews)
        return render_template('results.html',reviews=reviews)
        
    else:
        return render_template('index.html')
        
if __name__=="__main__":
    app.run(port=3000,debug=True)