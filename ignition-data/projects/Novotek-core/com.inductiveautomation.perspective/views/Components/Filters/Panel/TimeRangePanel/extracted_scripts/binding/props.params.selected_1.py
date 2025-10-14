# {
#     "struct": {
#         "from": "{view.params.dateFrom}",
#         "to": "{view.params.dateTo}"
#     },
#     "waitOnAll": true
# }

	import datetime
	
	rangeDay_start = datetime.timedelta(days=(datetime.datetime.today().weekday() + 7))
	rangeDay_end = datetime.timedelta(days=(datetime.datetime.today().weekday() +1))
	
	startWeek = datetime.date.today() - rangeDay_start
	endWeek = datetime.date.today() - rangeDay_end
	
	return (value['from'] == startWeek.strftime("%d/%m/%Y")) and (value['to'] == endWeek.strftime("%d/%m/%Y"))
	