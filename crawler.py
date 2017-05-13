__author__ = 'Eric'

import requests
from itertools import chain
from py2neo import Graph, Node, Relationship

con = Graph()
con.delete_all()

print('hello')

POAS_PATH = 'http://localhost:60200/api/'
POAS_RESOURCES =            ['notaries', 'people', 'subjects', 'poas']
POAS_RESOURCES_SINGULAR =   ['Notary',   'Person', 'Subject',  'POA']
POAS_FOREIGN_KEYS =         {
                             'idWitness': ('Notary', 'WITNESSED'),
                             'IdRegistrator': ('Notary','NOTARIZED'),
                             'Subject_idSubject': ('Subject', 'SUBJECTS'),
                             'Person_idPerson': ('Person', 'SIGNED'),
                             }

ORDERS_PATH = 'http://muchopesos-001-site1.smarterasp.net/api/'
ORDERS_RESOURCES_SINGULAR = ORDERS_RESOURCES = ['Expert', 'Order']
ORDERS_FOREIGN_KEYS = {'Experts_idExperts': ('Expert', 'ORDERED')}
EXPERTS_FOREIGN_KEYS = {'idDocument': ('POA', 'EXPERTIZED')}

for res, label in zip(POAS_RESOURCES, POAS_RESOURCES_SINGULAR):
    response = requests.get(POAS_PATH + res)
    if response.status_code == 200:
        for o in response.json():
            con.create(Node(label, **o))

for res, label in zip(ORDERS_RESOURCES, ORDERS_RESOURCES_SINGULAR):
    response = requests.get(ORDERS_PATH + res)
    if response.status_code == 200:
        for o in response.json():
            con.create(Node(label, **o))

poas = con.find("POA")
for poa in poas:
    for prop in POAS_FOREIGN_KEYS:
        node_label, rel_label = POAS_FOREIGN_KEYS[prop]
        fk_value = poa[prop]
        extern_node = con.find_one(node_label, 'id' + node_label, fk_value)
        con.create(Relationship(extern_node, rel_label, poa))

orders = con.find("Order")
for order in orders:
    for prop in ORDERS_FOREIGN_KEYS:
        node_label, rel_label = ORDERS_FOREIGN_KEYS[prop]
        fk_value = order[prop]
        extern_node = con.find_one(node_label, 'id' + node_label + 's', fk_value)
        con.create(Relationship(extern_node, rel_label, order))

experts = con.find("Expert", limit=1)
for expert in experts:
    for prop in EXPERTS_FOREIGN_KEYS:
        node_label, rel_label = EXPERTS_FOREIGN_KEYS[prop]
        fk_value = expert[prop]
        print(node_label, fk_value, 'id' + node_label)
        extern_node = con.find_one(node_label, 'id' + node_label, int(fk_value))
        if not extern_node is None:
            print(extern_node)
            con.create(Relationship(expert, rel_label, extern_node))