class bibentry:
    """Carries data of a bibtex entry"""
    
    def __init__(self, input_line): # input_line: string starting with @
        self.input_data = input_line # save defining line just in case
        self.id = input_line.split('{')[1].split(',')[0]    # inspire ID
        self.type = input_line.split('@')[1].split('{')[0]  # e.g. article
        self.rawdata = [] # list of input lines
        self.processed = False # has the data been parsed?
        self.data = {} # dictionary of processed data
        
    def add_line(self, input_line): # add line of potential data
        # input, string containing a line that does not begin with @
        # must throw out anything that doesn't have an assignment ('=')
        self.rawdata.append(input_line)
        # will still have to do post-processing later

    def process(self): # take the raw data and convert into processed data
        datalist = []
        newentry = True # start a new entry
        #
        for i in self.rawdata:
            if i.strip() == '}':
                continue # end
            if newentry == True:
                datalist.append(i.strip())
            else:
                datalist[len(datalist)-1] = datalist[len(datalist)-1] + ' ' + i.strip()
            if i.endswith('",\n'):
                newentry = True
            else:
                newentry = False
        #
        for j in datalist:
            self.data.update(
                {j.split('=',1)[0].strip() : j.split('=',1)[1].strip().lstrip('"').rstrip('",') })
        #
        ## Process author list
        authorlist = []
        if 'author' in self.data:
            for i in self.data['author'].split(' and '):
                # authorlist.append( i.split(',')[1].strip() + ' ' + i.split(',')[0].strip() )
                authorlist.append(i)
            self.data['author'] = authorlist
        #
        ## Process title
        if 'title' in self.data:
            self.data['title'] = self.data['title'].lstrip('{').rstrip('}')
        self.processed = True

    def htmlout(self):
        myhtml = '<li> '
        if 'title' in self.data:
            myhtml = myhtml + '<i>"' + self.data['title'] + ',"</i><br />'
        if 'author' in self.data:
            for i in range(0,len(self.data['author'])):
                # myhtml = myhtml + self.data['author'][i]
                ## The problem are some entries that don't have "and Last, First"
                ## but rather have "and others"
                try:
                    myhtml = myhtml + self.data['author'][i].split(',')[1][1] + '. '
                except IndexError: # if ...split(',')[1] doesn't exist
                    # print self.data['author'][i]
                    print 'Non-standard author in ' + self.id +  ', probably "and others"'
                myhtml = myhtml + self.data['author'][i].split(',')[0]
                #
                # myhtml = myhtml + self.data['author'][i].split()[0][0] + '. '
                # myhtml = myhtml + self.data['author'][i].split()[1]
                if i == len(self.data['author'])-1:
                    myhtml = myhtml + '; '
                else:
                    myhtml = myhtml + ', '
        ## 
        ## You might prefer to include this, I think it's easier to just
        ## include the DOI which encodes everything
        ##
        # if 'journal' in self.data:
        #     myhtml = myhtml + self.data['journal'] + ' '
        # if 'volume' in self.data:
        #     myhtml = myhtml + '<b>' + self.data['volume'] + '</b> '
        # if 'pages' in self.data:
        #     myhtml = myhtml + self.data['pages'] + ' '
        # if 'year' in self.data:
        #     myhtml = myhtml + '(' + self.data['year'] + ') '
        if 'doi' in self.data:
            myhtml = myhtml + '<a href="http://dx.doi.org/'
            myhtml = myhtml + self.data['doi']
            myhtml = myhtml + '">'
            myhtml = myhtml + self.data['doi']
            myhtml = myhtml + '</a> '
        if 'eprint' in self.data:
            myhtml = myhtml + '[<a href="http://arxiv.org/abs/arXiv:'
            myhtml = myhtml + self.data['eprint']
            myhtml = myhtml + '">' + self.data['eprint'] + '</a>]'
        myhtml = myhtml + '</li>'
        return myhtml
        
            
    def htmlout2(self): # different formatting
        myhtml = '<li> '
        if 'title' in self.data:
            if 'doi' in self.data:
                myhtml = myhtml + '<a href="http://dx.doi.org/'
                myhtml = myhtml + self.data['doi']
                myhtml = myhtml + '">'
            myhtml = myhtml + '<i>"' + self.data['title'] + ',"</i><br />'
            if 'doi' in self.data:
                myhtml = myhtml + '</a> '
        #
        if 'author' in self.data:
            for i in range(0,len(self.data['author'])):
                # myhtml = myhtml + self.data['author'][i]
                ## The problem are some entries that don't have "and Last, First"
                ## but rather have "and others"
                try:
                    myhtml = myhtml + self.data['author'][i].split(',')[1][1] + '. '
                except IndexError: # if ...split(',')[1] doesn't exist
                    # print self.data['author'][i]
                    print 'Non-standard author in ' + self.id +  ', probably "and others"'
                myhtml = myhtml + self.data['author'][i].split(',')[0]
                #
                # myhtml = myhtml + self.data['author'][i].split()[0][0] + '. '
                # myhtml = myhtml + self.data['author'][i].split()[1]
                if i == len(self.data['author'])-1:
                    myhtml = myhtml + '; '
                else:
                    myhtml = myhtml + ', '
        ##
        if 'journal' in self.data:
            myhtml = myhtml + self.data['journal'] + ' '
        if 'volume' in self.data:
            myhtml = myhtml + '<b>' + self.data['volume'] + '</b> '
        if 'pages' in self.data:
            myhtml = myhtml + self.data['pages'] + ' '
        if 'year' in self.data:
            myhtml = myhtml + '(' + self.data['year'] + ') '
        # if 'doi' in self.data:
        #     myhtml = myhtml + '<a href="http://dx.doi.org/'
        #     myhtml = myhtml + self.data['doi']
        #     myhtml = myhtml + '">'
        #     myhtml = myhtml + self.data['doi']
        #     myhtml = myhtml + '</a> '
        if 'eprint' in self.data:
            myhtml = myhtml + '[<a href="http://arxiv.org/abs/arXiv:'
            myhtml = myhtml + self.data['eprint']
            myhtml = myhtml + '">' + self.data['eprint'] + '</a>]'
        myhtml = myhtml + '</li>'
        return myhtml
                