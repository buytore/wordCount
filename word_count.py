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

new_str=''
engine = create_engine('mysql+mysqlconnector://root:root@localhost/dw_bintel')
metadata = MetaData(bind=engine)

sms = Table('sms_words', metadata, autoload=True)
conn = engine.connect()

srp = "SELECT investigation_notes FROM sms_words_June8 WHERE risk='High Risk'"

results = engine.execute(srp)
#entries = [dict(category=row[0], SRP=(row[4]*64+row[3]*32+row[2]*4), high=row[4], medium=row[3], low=row[2]) for row in results]
#sorted_entries = sorted(entries, key = lambda srp: srp['SRP'], reverse=True)

entries = [dict(investigation_notes=row[0]) for row in results]
#content = sms_words.decode('utf-8')
#mark = content.strip('\r')

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

# save the results
results = sorted(
    no_stop_words_count.items(),
    key=operator.itemgetter(1),
    reverse=True)
first_time = 0
freq_list = []
word_tag_str = ""
text_part = ',{"text":"'
size_part = '","size":'
list_str_start = '[{"text":"'
list_str_end = "]"
end_record = "}"
for result in results[:25]:
#    freq_list.append(text_part + result[0] + size_part + str(result[1]))
    if first_time == 0:
        word_tag_str += list_str_start + result[0] + size_part + str(result[1]) + end_record
        first_time = 1
    else:
        if first_time == 25:
            word_tag_str += text_part + result[0] + size_part + str(result[1]) + end_record + "]"
        else:
            word_tag_str += text_part + result[0] + size_part + str(result[1]) + end_record
    first_time += 1

print word_tag_str

#            freq_list.append('{"text":"' + result[0] + '","size":' + str(result[1]) + "}")
#new_freq_list = [i.replace("'", '{') for i in freq_list]
#return new_freq_list[:100]
