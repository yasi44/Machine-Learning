class stockPrediction:
    def __init__(self):
        File=open("stockLabels2.labels","r")
        List=[""]
        for Line in File:
            List.append(string.replace(Line,'\n',''))
        self.labels=List
        
    
    def createStocksBoolJson(self, magpieResult):
        
        REstock=re.compile(r'[A-Z]+')
        REprobability=re.compile(r'[0][.][0-9]+')
        stockNames=[]
        stockProbability=[]
        for stock in magpieResult:
            magpieResult_str=str(stock)
            listToks=magpieResult_str.split(',')
            stockNames.append(listToks[0][2:-1])
            stockProbability.append(float(listToks[1][1:-1]))
                     
        #boolList=[0]*len(self.labels)
        jsonString="["
        for i in stockNames:
            labelIndex=str(self.labels.index(i))
            if i== 'JCY':
                r=9
            if stockProbability[stockNames.index(i)] >self.THRESHOLD:
                string="{name:"+i+",index:"+labelIndex+", predition:1"+"},"               
            #else:# i think this part is not required and reporting only the positive treb is ok
            #    string="{name:"+i+",index="+labelIndex+", predition:0"+"},"
                jsonString = jsonString + string
        jsonString=jsonString[:-1]
        jsonDumpped=json.dumps(jsonString)
        return jsonDumpped
            
            
    def run(self,news, threshold):
        self.THRESHOLD=threshold
        magpie=Magpie(keras_model='savedMagpieModels/model.h5', 
                  word2vec_model='savedMagpieModels/embedding',
                  scaler='savedMagpieModels/scaler',
                  labels=self.labels)
        output=magpie.predict_from_text(news)
        return self.createStocksBoolJson(output)
