# by Torben Menke
# https://entorb.net
# date 2020-03-22


load "header.gp"

set terminal pngcairo size 640,800


set title ""
set ylabel "Infektionen"
# set xlabel "Datum"

# now lets compare several stats
set timefmt '%Y-%m-%d' # %d.%m.%Y %H:%M
set format x '%d.%m'
set xdata time

# TODO:
#set term windows


set key top left at graph 0, graph 1

set colorsequence default
unset style


date_last = system("tail -1 '../data/de-state-BW.tsv' | cut -f2")
set label 1 label1_text_right." based on RKI data of ".date_last

title = "Zeitverlauf der Infektionen in den Bundesländer"
set title title
set yrange [0:]
set output '../plots-gnuplot/cases-de-absolute.png'
plot \
  '../data/de-state-NW.tsv' using 2:3 title "Nordrhein-Westfalen" with lines lw 2, \
  '../data/de-state-BY.tsv' using 2:3 title "Bayern" with lines lw 2, \
  '../data/de-state-BW.tsv' using 2:3 title "Baden-Württemberg" with lines lw 2, \
  '../data/de-state-NI.tsv' using 2:3 title "Niedersachsen" with lines lw 2, \
  '../data/de-state-HE.tsv' using 2:3 title "Hessen" with lines lw 2, \
  '../data/de-state-RP.tsv' using 2:3 title "Rheinland-Pfalz" with lines lw 2, \
  '../data/de-state-BE.tsv' using 2:3 title "Berlin" with lines lw 2, \
  '../data/de-state-HH.tsv' using 2:3 title "Hamburg" with lines lw 2, \
  '../data/de-state-SN.tsv' using 2:3 title "Sachsen" with lines lw 2, \
  '../data/de-state-SH.tsv' using 2:3 title "Schleswig-Holstein" with lines lw 2, \
  '../data/de-state-BB.tsv' using 2:3 title "Brandenburg" with lines lw 2, \
  '../data/de-state-TH.tsv' using 2:3 title "Thüringen" with lines lw 2, \
  '../data/de-state-ST.tsv' using 2:3 title "Sachsen-Anhalt" with lines lw 2, \
  '../data/de-state-SL.tsv' using 2:3 title "Saarland" with lines lw 2, \
  '../data/de-state-MV.tsv' using 2:3 title "Mecklenburg-Vorpommern" with lines lw 2, \
  '../data/de-state-HB.tsv' using 2:3 title "Bremen" with lines lw 2, \

unset output
#  '../data/de-state-DE-total.tsv' using 2:3 title "Deutschland" with lines , \

set yrange [1:]
set logscale y

set title title ." - Logarithmische Skalierung"
set output '../plots-gnuplot/cases-de-absolute-log.png'
replot
unset output



# title = "Zeitverlauf der Infektionen in den Bundesländer pro 1 Mill Einwohner"
# set title title
# set yrange [0:]
# set output '../plots-gnuplot/cases-de-per-million.png'
# plot \
#   '../data/de-state-NW.tsv' using 2:3 title "Nordrhein-Westfalen" with lines lw 2, \
#   '../data/de-state-BY.tsv' using 2:3 title "Bayern" with lines lw 2, \
#   '../data/de-state-BW.tsv' using 2:3 title "Baden-Württemberg" with lines lw 2, \
#   '../data/de-state-NI.tsv' using 2:3 title "Niedersachsen" with lines lw 2, \
#   '../data/de-state-HE.tsv' using 2:3 title "Hessen" with lines lw 2, \
#   '../data/de-state-RP.tsv' using 2:3 title "Rheinland-Pfalz" with lines lw 2, \
#   '../data/de-state-BE.tsv' using 2:3 title "Berlin" with lines lw 2, \
#   '../data/de-state-HH.tsv' using 2:3 title "Hamburg" with lines lw 2, \
#   '../data/de-state-SN.tsv' using 2:3 title "Sachsen" with lines lw 2, \
#   '../data/de-state-SH.tsv' using 2:3 title "Schleswig-Holstein" with lines lw 2, \
#   '../data/de-state-BB.tsv' using 2:3 title "Brandenburg" with lines lw 2, \
#   '../data/de-state-TH.tsv' using 2:3 title "Thüringen" with lines lw 2, \
#   '../data/de-state-ST.tsv' using 2:3 title "Sachsen-Anhalt" with lines lw 2, \
#   '../data/de-state-SL.tsv' using 2:3 title "Saarland" with lines lw 2, \
#   '../data/de-state-MV.tsv' using 2:3 title "Mecklenburg-Vorpommern" with lines lw 2, \
#   '../data/de-state-HB.tsv' using 2:3 title "Bremen" with lines lw 2, \

# unset output
# #  '../data/de-state-DE-total.tsv' using 2:3 title "Deutschland" with lines , \

# set yrange [1:]
# set logscale y

# set title title ." - Logarithmische Skalierung"
# set output '../plots-gnuplot/cases-de-per-million-log.png'
# replot
# unset output








# set logscale y
# # set format y "10^{%L}"
# set title title ." - Logarithmische Skalierung"
# set output '../plots-gnuplot/cases-de-log.png'
# replot
# unset output
# unset logscale y
# unset xdata

# unset timefmt
# unset format
# unset xdata 