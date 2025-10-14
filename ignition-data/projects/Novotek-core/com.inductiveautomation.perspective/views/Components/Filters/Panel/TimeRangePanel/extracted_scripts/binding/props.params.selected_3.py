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
	rangeMonth = datetime.timedelta(days=lastDayOfMonth)
	
	previousDate = datetime.date.today() - rangeMonth
	lastDayOfPreviousMonth = calendar.monthrange(previousDate.year, previousDate.month)[1]
	
	startWeek = datetime.date(previousDate.year, previousDate.month, 1)
	endWeek = datetime.date(previousDate.year, previousDate.month, lastDayOfPreviousMonth)
	
	return (value['from'] == startWeek.strftime("%d/%m/%Y")) and (value['to'] == endWeek.strftime("%d/%m/%Y"))