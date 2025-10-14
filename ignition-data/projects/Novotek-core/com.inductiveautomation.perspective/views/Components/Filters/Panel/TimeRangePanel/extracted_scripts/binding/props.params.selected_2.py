# {
#     "struct": {
#         "from": "{view.params.dateFrom}",
#         "to": "{view.params.dateTo}"
#     },
#     "waitOnAll": true
# }

	import datetime
	import calendar
	
	currentYear = datetime.date.today().year
	currentMonth = datetime.date.today().month
	
	lastDayOfMonth = calendar.monthrange(currentYear, currentMonth)[1]
	
	startWeek = datetime.date(currentYear, currentMonth, 1)
	endWeek = datetime.date(currentYear, currentMonth, lastDayOfMonth)
	
	return (value['from'] == startWeek.strftime("%d/%m/%Y")) and (value['to'] == endWeek.strftime("%d/%m/%Y"))