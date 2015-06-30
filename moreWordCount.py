from stop_words import stops
import re
import nltk
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, select
import operator
from collections import Counter

def build_stopWordFile():

    new_str =''

    file = open('stop_words.CSV', 'rU')
    stop_words = file.read()

    new_stop_words = stop_words.replace("'", "")
    new_str = stop_words.replace(",", "\n\r")

    print new_str

    with open('test.csv', 'w') as a_file:
        for result in new_str:
            result = ' '.join(result)
            a_file.write(result)

def print_wordCount():

    new_str=''
    engine = create_engine('mysql+mysqlconnector://root:root@localhost/dw_bintel')
    metadata = MetaData(bind=engine)
    sms = Table('sms_words', metadata, autoload=True)
    conn = engine.connect()

    srp = "SELECT text_word, counts FROM sms_word_totals_copy LIMIT 25"

    results = engine.execute(srp)

    #        entries = [dict(category=row[0], total=row[1], high=row[4], medium=row[3]) for row in results]
    #entries = [dict(category=row[0], SRP=(row[4]*64+row[3]*32+row[2]*4), high=row[4], medium=row[3], low=row[2]) for row in results]
    #sorted_entries = sorted(entries, key = lambda srp: srp['SRP'], reverse=True)

#    entries = [dict(investigation_notes=row[0]) for row in results]
#    for sms_word, sms_count in results:
#        for sms_word, sms_count in row:
#        new_str += encode(sms_word)

    first_time = 0
    freq_list = []
    word_tag_str = ""
    text_part = ',{"text":"'
    size_part = '","size":'
    list_str_start = '[{"text":"'
    list_str_end = "]"
    end_record = "}"
    for word_result, count_result in results:
        if first_time == 0:
            word_tag_str += list_str_start + word_result + size_part + str(count_result) + end_record
            first_time = 1
        else:
            if first_time == 25:
                word_tag_str += text_part + word_result + size_part + str(count_result) + end_record + "]"
            else:
                word_tag_str += text_part + word_result + size_part + str(count_result) + end_record
        first_time += 1

    print word_tag_str



print_wordCount()
