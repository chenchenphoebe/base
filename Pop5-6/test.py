import xlwt
file = xlwt.Workbook()
table = file.add_sheet('sheet name',cell_overwrite_ok=True)
table.write(1, 1, 'text')
file.save("test1.xls")
