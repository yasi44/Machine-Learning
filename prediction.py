class stockPredictionModel:
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
            stockNames.append(re.match(REstock,stock))
            stockProbability.append(re.match(REprobability, stock))
            
        #boolList=[0]*len(self.labels)
        jsonString="["
        for i in self.labels:
            if REprobability[stockNames.index(i)] >self.THRESHOLD:
                string="{name:"+i+", predition:1"+"}"               
            else:
                string="{name:"+i+", predition:0"+"}"
            jsonString = jsonString + string
        jsonDumpped=json.dump(jsonString)
        return jsonDumpped
            
            
    def run(self,news, threshold):
        self.THRESHOLD=threshold
        magpie=Magpie(keras_model='savedMagpieModels/model.h5', 
                  word2vec_model='savedMagpieModels/embedding',
                  scaler='savedMagpieModels/scaler',
                  labels=self.labels)
        output=magpie.predict_from_text(news)
        return createStocksBoolJson(output)
