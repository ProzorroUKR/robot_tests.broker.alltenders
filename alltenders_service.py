#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from iso8601 import parse_date
from json import JSONEncoder
#from robot.output import LOGGER
#from robot.output.loggerhelper import Message
import op_robot_tests.tests_files.service_keywords as service_keywords
import munch
import re
import os
import urllib

def build_xpath(path, *idx):
    idx = tuple(int(i) + 1 for i in idx)
    return 'xpath=' + path.replace('xpath=', '').format(*idx)

def build_xpath_from_template(path, *args):
    return 'xpath=' + path.replace('xpath=', '').format(*args)

def build_xpath_old(*items):
    xpath = ''
    for item in items:
        xpath = '({0}{1})[{2}]'.format(xpath, item['path'].replace('xpath=', ''), int(item['idx']))
    return 'xpath=' + xpath

def build_xpath_for_parent(parent_path, parent_idx, *items):
    return build_xpath_old({ 'path': parent_path, 'idx': parent_idx }, *items)

def build_xpath_for_child(parent_path, parent_idx, child_path, child_idx):
    return build_xpath_for_parent(parent_path, parent_idx, { 'path': child_path, 'idx': child_idx })

def convert_iso_datetime(isodate, pattern="%d.%m.%Y %H:%M"):
    iso_dt = parse_date(isodate)
    date_string = iso_dt.strftime(pattern)
    return date_string

def datetime_to_iso(strDate,  pattern="%d.%m.%Y %H:%M"):
    date = datetime.strptime(strDate, pattern)
    return date.isoformat()

def download_document_from_url(url, path_to_save_file):
    f = open(path_to_save_file, 'wb')
    f.write(urllib.urlopen(url).read())
    f.close()
    return os.path.basename(f.name)

def find_complaint_index_by_complaintID(data, complaintID):
    if not data:
        return 0
    if 'data' in data:
        data = data['data']
    if not isinstance(data, (list, tuple)):
        data = [data]
    for index, element in enumerate(data):
        if 'complaintID' in element and element['complaintID'] == complaintID:
            break
    else:
        index = -1
    return index

def find_document_by_id(data, doc_id):
    for document in data.get('documents', []):
        if doc_id in document.get('title', ''):
            return document
    for complaint in data.get('complaints', []):
        for document in complaint.get('documents', []):
            if doc_id in document.get('title', ''):
                return document
    for award in data.get('awards', []):
        for document in award.get('documents', []):
            if doc_id in document.get('title', ''):
                return document
        for complaint in award.get('complaints', []):
            for document in complaint.get('documents', []):
                if doc_id in document.get('title', ''):
                    return document
    for cancellation in data.get('cancellations', []):
        for document in cancellation.get('documents', []):
            if doc_id in document.get('title', ''):
                return document
    for bid in data.get('bids', []):
        for document in bid.get('documents', []):
            if doc_id in document.get('title', ''):
                return document
    raise Exception('Document with id {} not found'.format(doc_id))

def find_document_index_by_id(data, doc_id):
    if not data:
        return 0
    if 'data' in data:
        data = data['data']
    if not isinstance(data, (list, tuple)):
        data = [data]
    for index, document in enumerate(data):
        if doc_id in document.get('title', ''):
            break
    else:
        index = -1
    return index

def find_index_by_id(data, object_id):
    if not data:
        return 0
    if 'data' in data:
        data = data['data']
    if not isinstance(data, (list, tuple)):
        data = [data]
    for index, element in enumerate(data):
        if 'id' in element and element['id'] == object_id:
            break
        if 'complaintID' in element and element['complaintID'] == object_id:
            break
        element_id = service_keywords.get_id_from_object(element)
        if element_id == object_id:
            break
    else:
        index = -1
    return index

def iso_date_to_ua(isodate):
    return convert_iso_datetime(isodate, "%d.%m.%Y")

def munchify_dictionary(arg=None, data=False):
    if arg is None:
        arg = {}
    if data:
        arg = { 'data': arg }
    return munch.munchify(arg)

def object_to_json(data):
    return JSONEncoder().encode(data)

def prepare_data(initial_data):
    data = initial_data['data']
    # --- procuringEntity ---
    procuringEntity = data['procuringEntity']
    procuringEntity['name'] = u'ТОВАРИСТВО З ОБМЕЖЕНОЮ ВІДПОВІДАЛЬНІСТЮ "ПАУЕР ГРУП"'
    procuringEntity['name_ru'] = u'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "ПАУЕР ГРУП"'
    procuringEntity['name_en'] = u'POWER GROUP LLC.'
    procuringEntity['kind'] = u'general'
    # --- identifier ---
    identifier = procuringEntity['identifier']
    identifier['id'] = u'35592115'
    identifier['legalName'] = u'ТОВАРИСТВО З ОБМЕЖЕНОЮ ВІДПОВІДАЛЬНІСТЮ "ПАУЕР ГРУП"'
    identifier['legalName_ru'] = u'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "ПАУЕР ГРУП"'
    identifier['legalName_en'] = u'POWER GROUP LLC.'
    identifier['uri'] = u'http://test.com'
    identifier['scheme'] = u'UA-EDR'
    # --- address ---
    address = procuringEntity['address']
    address['countryName'] = u'Україна'
    address['locality'] = u'киев'
    address['region'] = u'киевская'
    address['postalCode'] = u'01034'
    address['streetAddress'] = u'01034, м.Київ, Шевченківський район, ВУЛИЦЯ ЯРОСЛАВІВ ВАЛ, будинок 38'
    # --- additionalClassifications for all items
    for item in data['items']:
        for classification in item['additionalClassifications']:
            classification['id'] = u'-----'
            classification['description'] = u'Не визначено'
            classification['scheme'] = u'NONE'
    return initial_data

def ua_date_to_iso(uadate):
    return datetime_to_iso(uadate, "%d.%m.%Y")
