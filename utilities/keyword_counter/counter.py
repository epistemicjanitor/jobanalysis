import os

try:
    import sqlite3
except ImportError as err:
    print("This utility requires sqlite3")
except:
    raise

try:
    from collections import Counter
except:
    raise


class KeywordCounter(object):

    def __init__(self):
        pass

    def load(self, vocabulary, data, query=None):
        """
        vocabulary: list of string objects; or path to an \n delimited text file
        data: path to sqlite3 db file; requires SQL query parameter
        query: SQL query, type str; assumes that the query returns a
        list of str objects.
        """

        self.vocabulary = vocabulary
        self.data = data
        self.query = query

        if isinstance(self.vocabulary, list):
            if isinstance(self.vocabulary[0], str):
                self.vocabulary = vocabulary
            else:
                print('Vocabulary must be a list of str')
                return

        elif os.path.isfile(self.vocabulary):
            vocab_temp = []
            with open(self.vocabulary, 'r') as f:
                for line in f:
                    delim = line.find('\n')
                    line = line[:delim]
                    vocab_temp.append(line)
            self.vocabulary = vocab_temp
        if isinstance(self.data, list):
            self.data = data

        elif os.path.isfile(self.data):
            if isinstance(self.query, str):
                try:
                    conn = sqlite3.connect(self.data)
                    c = conn.cursor()
                    c.execute(self.query)
                    self.data = c.fetchall()
                except sqlite3.OperationalError:
                    print('Please enter a valid SQL query')
                    return
            else:
                print('Please enter a valid SQL query')
                return
        self.cities, self.documents = zip(*self.data)

        """--------------
        HELPER FUNCTIONS:
        --------------"""

    def sdcHelper(self, word_list, found, debug=False):

        """
        Check if there are false positives for 'r' and 'c'.
        If cCond >>> False, or
           rCond >>> False, that means they are false positives and should
        be removed.
        """
        cCond = self.cCounter(word_list)
        rCond = self.rCounter(word_list)


        """
        Helper functions for removing false positives of 'r' and 'c'
        """

        def rcRemoval(item):
            if len(item) == 0:
                return False
            if item[0] == 'c' or item[0] == 'r':
                return True
            else:
                return False

        def rRemoval(item):
            if len(item) == 0:
                return False
            if item[0] == 'r':
                return True
            else:
                return False

        def cRemoval(item):
            if len(item) == 0:
                return False
            if item[0] == 'c':
                return True
            else:
                return False



        if cCond and rCond:
            if debug:
                print([cCond, rCond])
            return found
        elif not cCond and not rCond:
            found[:] = [item for item in found if not rcRemoval(item)]
            if debug:
                print([cCond, rCond])
                print('\n')
                print(found)
            return found

        elif not cCond and rCond:
            found[:] = [item for item in found if not cRemoval(item)]
            if debug:
                print([cCond, rCond])
                print('\n')
                print(found)
            return found
        elif not rCond and cCond:
            found[:] = [item for item in found if not rRemoval(item)]
            if debug:
                print([cCond, rCond])
                print('\n')
                print(found)
            return found



    #"""cCounter FUNCTION CHECKS FOR CERTAIN KEYWORDS BEFORE/AFTER 'c' TO CHECK IF
    #THE CAUGHT 'c' IS NOT JUST NOISE FROM TEXT PARSING."""

    def cCounter(self, word_list, debug=False):
        test_list = []

        for ix, token in enumerate(word_list):
            if token == 'c':
                test_list = word_list[ix-10:ix+10]
                break

        if len(test_list) != 0:
            cond1, cond2 = self.cCounterHelper(test_list)
            if cond1 > 1 and cond2 > 0:
                if debug:
                    return True, test_list
                else:
                    return True
            elif cond1 > 1 and cond2 == 0:
                if debug:
                    return True, test_list
                else:
                    return True
            else:
                return False
        if debug:
            return False, None
        else:
            return False



    def cCounterHelper(self, test_list):
        key1 = 'programming coding software engineering scripting development developing engineer language languages java julia python scala fortran bash ruby sql perl r matlab data analytics praktijkervaring statistische analyse statistique programmation mining clustering classification sap hana manipulating visualizing building statistical programmier stata programmeren analyse mysql php gnuplot visualisatie technologien techniques vba postgresql druid presto hive cassandra keras tensorflow'
        key2 = 'experience exposure demonstrable essential knowledge skill skills proficiency skilled requirements requirement practical proven professional passion strong'
        kws1 = key1.split()
        kws2 = key2.split()
        kw1cnt = 0
        kw2cnt = 0

        for keyword in kws1:
            for _, token in enumerate(test_list):
                if token == keyword:
                    kw1cnt += 1
                    break
        for keyword in kws2:
            for _, token in enumerate(test_list):
                if token == keyword:
                    kw2cnt += 1
                    break
        return kw1cnt, kw2cnt



    def rCounter(self, word_list, debug=False):
        test_list = []

        for ix, token in enumerate(word_list):
            if token == 'r':
                if word_list[ix+2] == 'd':
                    continue
                test_list = word_list[ix-10:ix+10]
                break

        if len(test_list) != 0:
            cond1, cond2 = self.rCounterHelper(test_list)
            if cond1 > 1 and cond2 > 0:
                if debug:
                    return True, test_list
                else:
                    return True
            elif cond1 > 1 and cond2 == 0:
                if debug:
                    return True, test_list
                else:
                    return True
            else:
                return False
        if debug:
            return False, None
        else:
            return False


    def rCounterHelper(self, test_list):
        key1 = 'programming coding software engineering scripting development developing engineer language languages java julia python scala fortran bash ruby sql perl r matlab data analytics praktijkervaring statistische analyse statistique programmation mining clustering classification sap hana manipulating visualizing building statistical programmier stata programmeren analyse mysql php gnuplot visualisatie technologien techniques vba postgresql druid presto hive cassandra keras tensorflow'
        key2 = 'experience exposure demonstrable essential knowledge skill skills proficiency skilled requirements requirement practical proven professional passion strong'
        kws1 = key1.split()
        kws2 = key2.split()
        kw1cnt = 0
        kw2cnt = 0

        for keyword in kws1:
            for _, token in enumerate(test_list):
                if token == keyword:
                    kw1cnt+=1
                    break
        for keyword in kws2:
            for _, token in enumerate(test_list):
                if token == keyword:
                    kw2cnt+=1
                    break
        return kw1cnt, kw2cnt


    def single_doc_counter(self, document, debug=False):
        """
        Input: A document from self.documents; type str.
        Output: list of keywords found in the supplied text document.
        """

        """-------
        ATTRIBUTES
        -------"""

        found = []

        if debug:
            print("Initialize found list for keywords")
            print(type(found))

        word_list = document.split()
        ct = Counter(word_list)
        ctvals = ct.most_common()
        for tool in self.vocabulary:
            for token in ctvals:
                if token[0] == tool:
                    found.append(token)

        if debug:
            print("Printing found keywords: {}".format(found))
            print('\n')
            print(type(found))


        found_ = self.sdcHelper(word_list, found)

        if debug:
            print(type(found_))
            print(found_)
            return found, found_
        else:
            return found

    def document_counts(self):
        return [self.single_doc_counter(doc) for doc in self.documents]

    def numKeywordsPerText(self):
        return [len(item) for item in self.document_counts()]

    def indexDict(self):
        idx = {}
        for i in range(max(self.lengths)):
            key = 'idx'+str(i)
            value = [ix for ix, item in enumerate(self.lengths) if item == i]
            #if len(value) != -1:
            idx[key] = value
        return idx

    def keywordsDict(self):
        dct = {}
        for key, value in self.indexdict.items():
            dct[key] = [self.single_doc_counter(self.documents[ix]) for ix in value]
        return dct

    def keywordsDictFrozen(self):
        dct = {}

        for key, value in self.keywordsdict_.items():
            frozen = [frozenset(list(zip(*item))[0]) for item in value if len(value[0]) != 0]
            dct[key] = frozen
        return dct

    def preprocess(self):
        """
        This function MUST be called before computing keyword statistics.
        Function silently returns three attributes described below.
        """

        """
        ATTRIBUTES

        lengths: number of keywords found in every document in the corpus from
        the provided vocabulary; type list
        indexdict: dictionary of indexes for every document in the corpus with
        the same number of keywords; grouped by the number of keywords, i.e.
        length.
        """

        self.lengths = self.numKeywordsPerText()
        self.indexdict = self.indexDict()
        self.keywordsdict_ = self.keywordsDict()
        self.keywordsdict = self.keywordsDictFrozen()

    def sequenceStats(self, print_statistic=False):

        """
        This function returns keyword statistics.

        common_lengths
        common_sequences
        """

        self.common_lengths = []
        self.common_sequences = []

        def common_lengths():
            counts = Counter(self.lengths)
            return counts.most_common()

        def common_sequences():
            allsequences = []
            for key, value in self.keywordsdict.items():
                allsequences += value
            counts = Counter(allsequences)
            a = counts.most_common()
            results = []
            for item in a:
                seq, cnt = item
                results.append((list(seq), cnt))
            return results


        self.common_lengths = common_lengths()
        self.common_sequences = common_sequences()


        if print_statistic == 'common_lengths':
            print(self.common_lengths)
        if  print_statistic  == 'common_sequences':
            print(self.common_sequences)

    def keywordStats(self, statistic=False):
        """
        Output:
            keyword_counts: total counts for every keyword;
        """

        def keywordCounts():
            keyword_counts = []
            for keyword in self.vocabulary:
                keyword_counts.append((keyword, self.singleKeywordCounter(keyword)))
            return keyword_counts

        self.keyword_counts = keywordCounts()


    def singleKeywordCounter(self, keyword, distribution=False, all_keywords=False):
        """
        If indexdict is not provided, returns the total number of keyword
        found in the corpus, each document is a YES/NO mention 1/0.
        Because some documents might have the keyword mentioned more than once,
        if you wish to count ALL keyword mentions in the corpus
        If indexdict is provided, returns the keyword distribution among
        different keyword sequence lengths.
        """
        if distribution:
            results = []
            for key, value in self.indexdict.items():
                seq_length = [int(key[ix:]) for ix, token in enumerate(key) if token.isdigit()][0]
                total = 0
                for ix in value:
                    doc = self.documents[ix].split()
                    if keyword == 'r':
                        cond = self.rCounter(doc)
                        if cond:
                            total+=1
                            continue
                        else:
                            continue
                    elif keyword == 'c':
                        cond = self.cCounter(doc)
                        if cond:
                            total+=1
                            continue
                        else:
                            continue
                    else:
                        count = doc.count(keyword)
                        if count:
                            total+=1
                        continue
                results.append((seq_length, total))
            return results

        else:
            total = 0
            for doc in self.documents:
                doc = doc.split()
                if keyword == 'r':
                    cond = self.rCounter(doc)
                    if cond:
                        total+=1
                        continue
                    else:
                        continue
                elif keyword == 'c':
                    cond = self.cCounter(doc)
                    if cond:
                        total+=1
                        continue
                    else:
                        continue
                else:
                    count = doc.count(keyword)
                    if count:
                        total+=1
                    continue
            return total


