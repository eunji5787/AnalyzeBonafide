import Gnuplot

g = Gnuplot.Gnuplot()
g.title('My Systems Plot')
g.xlabel('Date')
g.ylabel('Value')
g('set term png')
g('set out "output.png"')
#proc = open("response","r")
#databuff = Gnuplot.Data(proc.read(), title="test")

databuff = Gnuplot.Data("response", using='1:2',with_='line', title="test")
g.plot(databuff)