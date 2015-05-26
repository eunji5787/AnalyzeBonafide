#import QueryAvg
import sys
import Gnuplot
import glob

def getCvsfilename():
	csv_list = glob.glob("*.csv")
	for i in csv_list:
		print "If you want to see " + i + " 's chart. Choose " + str(csv_list.index(i))
	inputcsv = raw_input(" Input number according to the info ")
	while( inputcsv.isdigit() == False ):
		inputcsv = raw_input(" You can input only number. Please input number ")
	return csv_list[int(inputcsv)]

chartname = getCvsfilename()
chartpng = chartname.strip(".csv")+".png"

g = Gnuplot.Gnuplot()
g.title(chartname)
g.xlabel('Protocolname')
g.ylabel(chartname)
#g('set palette defined ( 1  "#0025ad", 2  "#0042ad", 3  "#0060ad", 4  "#007cad", 5  "#0099ad",')
#g('set palette defined ( 6  "#00ada4", 7  "#00ad88", 8  "#00ad6b", 9  "#007cad", 10  "#00ad4e",')
g('fi = "#99ffff"')
g('se = "#4671d5"')
g('th = "#ff0000"')
#g('fo = "#f36e00"')
g('set term png')
g('set output "%s"'%chartpng)
g('set style data histogram')
g('set style histogram cluster gap 1')
g('set style fill solid 1.0 border -1')
g('set datafile separator ","')
g('set key autotitle columnhead')
g('set auto x')
g('set yrange[0:*]')
plotcmd = "'"+str(chartname)+"'" + " using 2:xtic(1) ti col fc rgb fi"
plotcmd += ", '' u 3 ti col fc rgb se"
plotcmd += ", '' u 4 ti col fc rgb th"
#plotcmd += ", '' u 5 ti col fc rgb fo"

#plotcmd = "for [col=2:5] 'ProtocolAvg.csv' using col:xtic(1) ti col fc rgb fi"
g.plot(plotcmd)
