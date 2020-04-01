import networkx as nx
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import sys
import re

layout = [[sg.Text('Choose two files.')],
          [sg.Text('File 1', size=(8, 1)), sg.Input(), sg.FileBrowse()],
          [sg.Text('File 2', size=(8, 1)), sg.Input(), sg.FileBrowse()],
          [sg.Submit(), sg.Cancel()]]

window = sg.Window('Browse Files', layout)

event, values = window.read()
window.close()
fname1 = values[0]
fname2 = values[1]

plt.figure(figsize =(10, 7))

G = nx.read_weighted_edgelist(fname1, delimiter =" ")
H = nx.read_weighted_edgelist(fname2, delimiter =" ")

nx.draw_networkx(G, with_label = True)
plt.show()

nx.draw_networkx(H, with_label = True)
plt.show()

if nx.is_isomorphic(G, H):
    print("The graphs are isomorphic.")
else:
    print("The graphs are not isomorphic.")
