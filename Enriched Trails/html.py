


def define_html(urlimg,Info):

        categories = list( Info.keys() )
        
        print(categories)
        
        
        header = """ <html>
                <head>
                    
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
                    <link rel="stylesheet" href="./css/style.css">
                </head>
                    <body>
                        <div class="container">
                                <div class="row">
                                    <div class="col">
                                        <div class = "logo"></div>
                                    </div>
                                    <div class="col">
                                        <div class = "text" >
                                            UNIGE_MAP
                                         </div>
                                    </div>
                                </div>
                                <hr>
                                

                                <div class="map" style=" background-image: url(""" + urlimg + """ ">
                                    
                                </div>

                                """
        
        for category in categories :
        
                print(category)
                print(type(category))
                
                header += """<hr>
                            <div class="title">""" + category
                
                for element in Info[category]:
                
                    header += """ <div class= "spot" > """ + element + """ </div> """
                            
                   
                header +=  """ </div> """

        end = """</div>
                            </body>
            </html> """
        
        return header+end

