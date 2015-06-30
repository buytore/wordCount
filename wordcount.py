__author__ = 'markbannan'
from stop_words import stops
from collections import Counter
from bs4 import BeautifulSoup
import operator
import re
import nltk
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, select


new_str=''
engine = create_engine('mysql+mysqlconnector://root:root@localhost/dw_bintel')

conn = engine.connect()

srp = "SELECT text_word, counts FROM sms_word_totals_copy WHERE 1"
results = engine.execute(srp)
#entries = [dict(investigation_notes=row[0]) for row in results]

#for value in entries:
for value in results:
    new_str += value[0] + ' '.encode('utf_8')
tokens = nltk.word_tokenize(new_str)
text = nltk.Text(tokens)

# remove punctuation, count raw words
nonPunct = re.compile('.*[A-Za-z].*')
raw_words = [w for w in text if nonPunct.match(w)]
#raw_word_count = Counter(raw_words)

first_time = 0
freq_list = []
word_tag_str = ""
text_part = ',{"text":"'
size_part = ', '
list_str_start = '[{"text":"'
list_str_end = "]"
end_record = "}"

for result in new_results[:25]:
    word_tag_str += result[0] + size_part + str(result[1])
    first_time+=1

print first_time, word_tag_str