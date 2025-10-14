# {
#     "struct": {
#         "from": "{view.params.dateFrom}",
#         "to": "{view.params.dateTo}"
#     },
#     "waitOnAll": true
# }

	import datetime
	
	rangeDay_start = datetime.timedelta(days=datetime.datetime.today().weekday())
	rangeDay_end = datetime.timedelta(days=(6-datetime.datetime.today().weekday()))
	
	startWeek = datetime.date.today() - rangeDay_start
	endWeek = datetime.date.today() + rangeDay_end
	
	return (value['from'] == startWeek.strftime("%d/%m/%Y")) and (value['to'] == endWeek.strftime("%d/%m/%Y"))
	