__author__ = 'markbannan'
from stop_words import stops
from collections import Counter
from bs4 import BeautifulSoup
import operator
import re
import nltk
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, select


def lookahead(iterable):
    it = iter(iterable)
    last = it.next() # next(it) in Python 3
    for val in it:
        yield last, False
        last = val
    yield last, True

class wordHandling:

    def countWordsNormalized(self):
        # QUERY DB, BUILD WORD COUNT LIST, BUILD STRING VIEW OF DATA & RETURN

        new_str=''
        engine = create_engine('mysql+mysqlconnector://root:root@localhost/dw_bintel')
        metadata = MetaData(bind=engine)

        sms = Table('sms_words', metadata, autoload=True)
        conn = engine.connect()

        srp = "SELECT investigation_notes FROM sms_words_June8 WHERE risk='High Risk'"
        results = engine.execute(srp)
        entries = [dict(investigation_notes=row[0]) for row in results]

        for value in entries:
            new_str += str(value).lower()
        tokens = nltk.word_tokenize(new_str)
        text = nltk.Text(tokens)
        #    new_str += text

        # remove punctuation, count raw words
        nonPunct = re.compile('.*[A-Za-z].*')
        raw_words = [w for w in text if nonPunct.match(w)]
        raw_word_count = Counter(raw_words)

        # stop words
        no_stop_words = [w for w in raw_words if w.lower() not in stops]
        no_stop_words_count = Counter(no_stop_words)

        first_time = 0
        word_tag_str = ""
        text_part = ',{"text":"'
        size_part = '","size":'
        list_str_start = '[{"text":"'
        list_str_end = "]"
        end_record = "}"
        words_to_display = 25

        [v_max[1] for v_max in no_stop_words_count.most_common(1)]
        new_v_max = float(v_max[1])

        for k,v in no_stop_words_count.most_common(words_to_display):
            new_v = round(float(v)/new_v_max*100.0, 0)
            if first_time == 0:
                word_tag_str += list_str_start + k + size_part + str(new_v) + end_record
            else:
                if first_time == words_to_display - 1:
                    word_tag_str += text_part + k + size_part + str(new_v) + end_record + list_str_end
                else:
                    word_tag_str += text_part + k + size_part + str(new_v) + end_record
            first_time += 1
        return word_tag_str

    def countWords(self, countValue = 'normalize', nbrWordsToReturn=25):
        # QUERY DB, BUILD WORD COUNT LIST, BUILD STRING VIEW OF DATA & RETURN

        new_str=''
        engine = create_engine('mysql+mysqlconnector://root:root@localhost/dw_bintel')
        metadata = MetaData(bind=engine)

        sms = Table('sms_words', metadata, autoload=True)
        conn = engine.connect()

        srp = "SELECT investigation_notes FROM sms_words_June8 WHERE risk='High Risk'"
        results = engine.execute(srp)
        for row in results:
#            new_str = row.decode('utf-8')
            print row
            tokens = nltk.word_tokenize(row)
        text = nltk.Text(tokens)

        # remove punctuation, count raw words
        nonPunct = re.compile('.*[A-Za-z].*')
        raw_words = [w for w in text if nonPunct.match(w)]
        raw_word_count = Counter(raw_words)

        # stop words
        no_stop_words = [w for w in raw_words if w.lower() not in stops]
        no_stop_words_count = Counter(no_stop_words)

        first_time = 0
        word_tag_str = ""
        text_part = ',{"text":"'
        size_part = '","size":'
        list_str_start = '[{"text":"'
        list_str_end = "]"
        end_record = "}"
#        words_to_display = 25

        if countValue == 'normalize':
            [v_max[1] for v_max in no_stop_words_count.most_common(1)]
            new_v_max = float(v_max[1])

            for k,v in no_stop_words_count.most_common(nbrWordsToReturn):
                new_v = round(float(v)/new_v_max*100.0, 0)
                if first_time == 0:
                    word_tag_str += list_str_start + k + size_part + str(new_v) + end_record
                else:
                    if first_time == nbrWordsToReturn - 1:
                        word_tag_str += text_part + k + size_part + str(new_v) + end_record + list_str_end
                    else:
                        word_tag_str += text_part + k + size_part + str(new_v) + end_record
                first_time += 1
            return word_tag_str
        else:
            for k,v in no_stop_words_count.most_common(nbrWordsToReturn):
                if first_time == 0:
                    word_tag_str += list_str_start + k + size_part + str(v) + end_record
                else:
                    if first_time == nbrWordsToReturn - 1:
                        word_tag_str += text_part + k + size_part + str(v) + end_record + list_str_end
                    else:
                        word_tag_str += text_part + k + size_part + str(v) + end_record
                first_time += 1
            return word_tag_str


print wordHandling().countWords('normalize', 5)