#!/usr/bin/env python
# -*- coding: utf-8  -*-
#
# Darlehensrechner
#	Laufzeit
#	Gesamtzinsen nach x Jahren
#	Annuität bestehend aus Tilgung und Zinsen

import locale


kredit = 112					# Darlehen in  Tausend €
kredit *= 1000					# Kurzform von kredit = kredit * 1000
sollzins = 0.75					# Sollzins in % pro Jahr
zahlung = 4800					# Zahlungsrate/Annuität (Tilgung und Zins) pro Jahr
zperiode = 12					# Zahlungsperiode, x mal im Jahr
skip = 5					# alle skip Jahre Werte ausgeben
graphZeigen = False				# Graph ausgeben
if graphZeigen:
	import matplotlib.pyplot as plot
schulden = kredit				# restliche Schulden, Anfangswert ist der Kredit
ezins = (1 + sollzins/zperiode) ** zperiode -1	# effektiver Jahreszins bei monatlicher Zahlung
tilgung = 0					# berechneter Tilgungsanteil je Monat
jahre = 0					# berechnete Gesamtlaufzeit
zsum = 0					# Zinszahlungen gesamt
zlist = []					# Liste mit Zinsen
tlist = []					# Liste mit Tilgungen
jlist = []					# Liste mit Jahren

locale.setlocale(locale.LC_ALL, '')		# regionale Eigenschaften des Systems auslesen
def euro(value):				# Hilfsfunktion Beträge in Euro formatieren
	return locale.currency(value, grouping=True)

print("┌────────────────── Darlehensrechner ──────────────────┐")
print("\tKredit:\t\t\t" + euro(kredit))
print("\tAnnuität:\t\t" + euro(zahlung) + "/a")
print("\t\t\t\t" + euro(zahlung/12) + "/Monat")
print("\tNominalzins:\t\t" + str(sollzins) + " %/a")
print("\tEff. Jahreszins:\t" + str(round(ezins, 2)) + " %/a")
print("├──────────────────────────────────────────────────────┤")

while schulden > 0:				# while-Schleife bis es keine Schulden mehr gibt
	jahre += 1				# Jahre hochzählen (jahre = jahre +1)
	zins = schulden * sollzins/100		# Zins für Jahr berechnen
	zsum += zins				# Zins aufsummieren
	tilgung = zahlung - zins		# Tilgung für Jahr berechnen
	if tilgung < 0:				# Sonderfall zu geringe Zahlungsrate
		print("[!] Zahlungsrate zu gering: Zins übersteigt Zahlungsrate.")
		exit(1)
	if schulden < zahlung:			# Sonderfall letztes Jahr, komplette Tilgung
		zahlung = schulden		# Zahlung maximal so viel wie Restkredit
		tilgung = zahlung - zins	# Tilgungsanteil entsprechend anpassen
	schulden -= zahlung			# Restkredit für nächstes Jahr berechnen
	
	# Werte ausgeben alle $skip Jahre und immer das erste und letzte Jahr
	if skip == 1 or jahre % skip == 1 or schulden == 0:
		zlist.append(zins)
		tlist.append(tilgung)
		jlist.append("Jahr " + str(jahre))
		print("Jahr " + str(jahre))
		print("\tZins:\t\t" + euro(zins) + ("\t\t" if zins<100 else "\t") + euro(zins/12) + "/Monat")
		print("\tTilgung:\t" + euro(tilgung) + ("\t\t" if tilgung<100 else "\t") + euro(tilgung/12) + "/Monat")
		print("\tRestkredit\t" + euro(schulden))

print("├──────────────────────────────────────────────────────┤")
print("\tLaufzeit:\t\t" + str(jahre) + " Jahre")
print("\tZinszahlungen:\t\t" + euro(zsum) + " (" + str(round(100/kredit*zsum, 2)) + " %)")
print("└──────────────────────────────────────────────────────┘")

if graphZeigen:
	fig, ax = plot.subplots()
	ax.bar(jlist, tlist, 0.6, label='Tilgung')
	ax.bar(jlist, zlist, 0.6, bottom=tlist, label='Zins')
	ax.set_ylabel("Zahlungsrate in €/a")
	ax.set_title("Annuität über Laufzeit")
	ax.legend()
	plot.show()
