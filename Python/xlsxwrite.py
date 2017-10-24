# _*_ coding: utf-8 _*_

import xlsxwriter
import os

if os.path.exists('demo.xlsx'):
    os.remove('demo.xlsx')
workbook = xlsxwriter.Workbook('demo.xlsx')
worksheet = workbook.add_worksheet('main')

bold = workbook.add_format({'bold': True})
money = workbook.add_format({'num_format': '$#,##0'})


data = (
    ['zhongyongkang', 1000],
    ['xuyong', 2000],
    ['lalala', 238]
)

row = 1
col = 0

worksheet.write(0, 0, u'姓名', bold)
worksheet.write(0, 1, u'数量', bold)

for item, cost in (data):
    worksheet.write(row, col, item, bold)
    worksheet.write(row, col + 1, cost, money)
    row += 1

worksheet.write(row, col, 'Total', bold)
worksheet.write(row, col + 1, '=sum(B2:B4)', money)

workbook.close()