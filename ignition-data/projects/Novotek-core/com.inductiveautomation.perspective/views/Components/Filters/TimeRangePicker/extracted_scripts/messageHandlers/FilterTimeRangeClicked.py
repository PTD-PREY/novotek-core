	import datetime
	
	if payload == "currentWeek":
	    rangeDay_start = datetime.timedelta(days=datetime.datetime.today().weekday())
	    rangeDay_end = datetime.timedelta(days=(6 - datetime.datetime.today().weekday()))
	
	    startWeek = datetime.date.today() - rangeDay_start
	    endWeek = datetime.date.today() + rangeDay_end
	
	    self.view.params.dateFrom = datetime.date(startWeek.year, startWeek.month, startWeek.day)
	    self.view.params.dateTo = endWeek
	
	elif payload == "previousWeek":
	    rangeDay_start = datetime.timedelta(days=datetime.datetime.today().weekday() + 7)
	    rangeDay_end = datetime.timedelta(days=(datetime.datetime.today().weekday() + 1))
	
	    startWeek = datetime.date.today() - rangeDay_start
	    endWeek = datetime.date.today() - rangeDay_end
	
	    self.view.params.dateFrom = datetime.date(startWeek.year, startWeek.month, startWeek.day)
	    self.view.params.dateTo = endWeek
	
	elif payload == "currentMonth":
	    today = datetime.date.today()
	    startMonth = today.replace(day=1)
	    if today.month == 12:
	        nextMonth = today.replace(year=today.year + 1, month=1, day=1)
	    else:
	        nextMonth = today.replace(month=today.month + 1, day=1)
	    endMonth = nextMonth - datetime.timedelta(days=1)
	
	    self.view.params.dateFrom = startMonth
	    self.view.params.dateTo = endMonth
	
	elif payload == "previousMonth":
	    today = datetime.date.today()
	    firstDay_currentMonth = today.replace(day=1)
	    lastDay_previousMonth = firstDay_currentMonth - datetime.timedelta(days=1)
	    start_previousMonth = lastDay_previousMonth.replace(day=1)
	
	    self.view.params.dateFrom = start_previousMonth
	    self.view.params.dateTo = lastDay_previousMonth