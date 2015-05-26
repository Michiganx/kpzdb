__author__ = 'Eric'
import os
from subprocess import Popen, PIPE
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table
from reportlab.lib.styles import getSampleStyleSheet
from py2neo import Graph

REPORT_FILENAME = 'REPORT.PDF'
P12_FILE_PATH = 'pe.p12'
CERT_PASSWORD = '1'

con = Graph()


def sign_pdf(name):
    Popen(['java', '-jar', r'C:\Program Files (x86)\JSignPdf\jSignpdf.jar',
                   '--bg-path', 'logo.gif',
                   '-kst', 'PKCS12',
                   '-ksf', P12_FILE_PATH,
                   '-ksp', CERT_PASSWORD,
                   name,
                   '-V',
                   ])


def notaries_data():
    records =[]
    for n in con.find('Notary'):
        rec = [n['LastName'], n['Name'], n['Region']]
        records.append(rec)
    return records

def orders_data():
    records =[]
    for n in con.find('Order'):
        rec = [n['idCommissionOrders'], n['commissionName'], n['CommissionOrderDate']]
        records.append(rec)
    return records


def experts_data():
    records =[]
    for n in con.find('Expert'):
        rec = [n['name'], n['workplace'], n['address']]
        records.append(rec)
    return records

doc = SimpleDocTemplate(REPORT_FILENAME, pagesize=letter)
# container for the 'Flowable' objects

styleSheet = getSampleStyleSheet()


head = Paragraph(u'''<para align=center spaceb=3><h1><super>REPORT</super></h1></para>''',
               styleSheet["Heading1"])

P1 = Paragraph('''
    <para align=center spaceb=3> Notaries </para>''',
    styleSheet["BodyText"])

data1= [['LastName', 'Name', 'Region']] + notaries_data()



P2 = Paragraph('''
    <para align=center spaceb=3> Orders </para>''',
    styleSheet["BodyText"])

data2= [['#', 'comission', 'Date']] + orders_data()



P3 = Paragraph('''
    <para align=center spaceb=3> Experts </para>''',
    styleSheet["BodyText"])

data3= [['Name', 'Workplace', 'Region']] + experts_data()

t1 = Table(data1, style = [('BOX', (0,0), (-1,-1), 2, colors.black), ('GRID',(0,0),(-1,-1),1,colors.black)])
t2 = Table(data2, style = [('BOX', (0,0), (-1,-1), 2, colors.black), ('GRID',(0,0),(-1,-1),1,colors.black)])
t3 = Table(data3, style = [('BOX', (0,0), (-1,-1), 2, colors.black), ('GRID',(0,0),(-1,-1),1,colors.black)])



elements = [head, P1, t1, P2, t2, P3, t3]
# write the document to disk
doc.build(elements)

sign_pdf(REPORT_FILENAME)