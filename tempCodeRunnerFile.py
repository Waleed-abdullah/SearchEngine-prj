file_path = './Dataset/nela-gt-2020/newsdata'
    # jsonFiles = [files for files in os.listdir(file_path) if files.endswith('.json')]
    # snow_stemmer = SnowballStemmer(language='english')
    # data = []
    # wordSet = set(stopwords.words('english'))
    # for i in range(50):
    #     fileName = jsonFiles[i]
    #     file = open(('./Dataset/nela-gt-2020/newsdata/{}'.format(fileName)))
    #     data_load = json.load(file)
    #     for raw_data in data_load:
    #         text_words = list(dict.fromkeys((re.sub('[^a-zA-Z]', ' ', raw_data['content'])).lower().split()))
    #         data += ([snow_stemmer.stem(word) for word in text_words if not word in wordSet])
            
   
    # f_lex = open("sample.txt", "w")
    # for x in sorted(list(dict.fromkeys((data)))):
    #     f_lex.write(x + "\n")
    # f_lex.close()