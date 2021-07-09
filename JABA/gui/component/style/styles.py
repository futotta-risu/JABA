
main_style = """

#SectionLabel{
    font-weight: bold;
    font-size: 16px;
    color: #333;
    margin-bottom: 4px;
}

#PlotLabel{
    font-weight: bold;
    font-size: 16px;
    color: #333;
    margin-bottom: 4px;
}

#DashboardLabel{
    font-weight: bold;
    font-size: 30px;
    color: #fff;
    margin-bottom: 2px;
}


#Background{
    background-color: #F1F8F8;
}

#MapButton{
  background-color: #8af;
}

#MapButton {
    background:linear-gradient(to bottom, #599bb3 5%, #408c99 100%);
    background-color:#599bb3;
    border-radius:8px;
    color:#ffffff;
    font-family:Arial;
    font-size:14px;
    padding:6px 12px 5px;
    text-decoration:none;
}
#MapButton:hover {
    background:linear-gradient(to bottom, #408c99 5%, #599bb3 100%);
    background-color:#408c99;
}
#MapButton:active {
    position:relative;
    top:1px;
}

#NameEdit {
    border: 0px;
    border-bottom: 1px solid #aaa;
}

#NameEdit:focus {
    border: 0px;
    border-bottom: 1px solid #8af;
}

#FormLabel {
    font-size:12px;
    font-weight: bold;
}

#InnerModelDescription1m83b9s{
    border-right: 1px solid #ddd;
}

QTableView {
 border: none;
}

QTableWidget::item{
    padding-top: 6px;
    padding-bottom: 6px;
}

QCalendarWidget QWidget#qt_calendar_prevmonth
{
   qproperty-icon:url("media/icons/left.png");
}

QCalendarWidget QWidget#qt_calendar_nextmonth
{
   qproperty-icon:url("media/icons/right.png");
}

#DeleteButton{
    qproperty-icon:url("media/icons/cross.png");
    background-color: rgba(255, 255, 255, 0);
    border: 0px solid black;
}

#DeleteButton:hover{
    qproperty-icon:url("media/icons/cross-hover.png");
    background-color: rgba(255, 255, 255, 0);
    border: 0px solid black;
}


#ViewModeButton{
    qproperty-iconSize: 24px 24px;
}

#ViewModeButton{
    background-color: rgba(255, 255, 255, 0);
    border: 0px solid black;
}

QWidget#qt_calendar_navigationbar
{
    background-color: #ffffff;
    border: 0px solid #4f4f4f;
    color: #18BEBE;
}

QCalendarWidget QMenu{
    color: #18BEBE;

}

QCalendarWidget{
    color: #18BEBE;

}

QDateEdit {
	color: #18BEBE;
}

QCalendarWidget QToolButton{
    color: #18BEBE;
}

QSplitter::handle:vertical#PlotHeaderSplit {
    height: 0px;
}

#TitleWidget{
    background-color: #18BEBE;
    border-radius: 8px;
    margin: 0px 8px 0px 8px;
}

#TitleWidgetHeader{
    background-color: #18BEBE;
    margin-right: 8px;
}

"""