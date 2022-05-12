# -*- coding: utf-8 -*-

"""
Koło Fortuny
Mateusz Wasyluk
"""
import random
from tkinter import *
from tkinter.ttk import *
from tkinter import simpledialog
from PIL import Image, ImageTk
import numpy as np
from queries import draw_question, get_score
import re
from xml.etree.ElementTree import Element, SubElement, ElementTree, parse
from insertPG import pointsToTable

root = Element("Wynik")


class Player:
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.total = 0


class Window(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.p1 = IntVar(value=1)
        self.p2 = IntVar()
        self.p3 = IntVar()
        self.p4 = IntVar()
        self.p5 = IntVar()

        self.wheelValues = [1, -2, 3, -4, 5, -6, 7, -8, 9, -10, 0, -1, 2, -3, 4, -5, 6, -7, 8, -9, 10]
        self.wheelIndex = 0
        self.turnPoints = 0

        self.category = ''
        self.questionText = ''
        self.answer = ''
        self.hiddenAnswer = ''

        self.playerList = []
        self.playerCount = 0
        self.playerOrder = []
        self.playerIndex = 0
        self.roundCounter = 0

        self.newGameButton = Button(self, text="Nowa Gra", command=self.newGame)
        self.bestScoreButton = Button(self, text="Najlepsze Wyniki", command=self.showScores)
        self.roundLabel = Label(self, text="Runda 0/3")
        self.questionLabel = Label(self, text='')
        self.endGameButton = Button(self, text="Zakończ", command=self.endGame)
        self.p1CheckBox = Checkbutton(self, text="Gram!", variable=self.p1, state='disabled')
        self.p2CheckBox = Checkbutton(self, text="Gram!", variable=self.p2)
        self.p3CheckBox = Checkbutton(self, text="Gram!", variable=self.p3)
        self.p4CheckBox = Checkbutton(self, text="Gram!", variable=self.p4)
        self.p5CheckBox = Checkbutton(self, text="Gram!", variable=self.p5)
        self.p1Name = Entry(self)
        self.p2Name = Entry(self)
        self.p3Name = Entry(self)
        self.p4Name = Entry(self)
        self.p5Name = Entry(self)
        self.base = Canvas(self, width=467, height=467)
        self.image = Image.open('tarcza1.png')
        self.im = ImageTk.PhotoImage(self.image)
        self.guessLetterButton = Button(self, text='Zgadnij literę', state='disabled', command=self.guessLetter)
        self.spinTheWheelButton = Button(self, text="Kręć kołem!", state='disabled', command=self.spin)
        self.guessAnswerButton = Button(self, text='Zgadnij hasło', state='disabled', command=self.guessAnswer)
        self.answerLabel = Label(self)
        self.p1Points = Label(self)
        self.p2Points = Label(self)
        self.p3Points = Label(self)
        self.p4Points = Label(self)
        self.p5Points = Label(self)
        self.queueLabel = Label(self)
        self.endTurnButton = Button(self, text="Zakończ turę", state='disabled', command=self.endTurn)
        self.endRoundButton = Button(self, text="Zakończ rundę", state='disabled', command=self.endRound)
        self.turnPointsLabel = Label(self)
        self.bestScoreLabel1 = Label(self)
        self.bestScoreLabel2 = Label(self)
        self.bestScoreLabel3 = Label(self)
        self.bestScoreLabel4 = Label(self)
        self.bestScoreLabel5 = Label(self)
        self.bestScoreLabel6 = Label(self)

        self.style = Style()
        self.parent = parent
        self.initialize()

    def getQuestion(self):
        question = draw_question()
        self.category = question[0]
        self.questionText = question[1]
        self.answer = question[2]
        self.questionLabel.configure(text=self.category + ': ' + self.questionText)

        for h in range(0, len(self.answer)):
            self.hiddenAnswer += '*'

        if self.answer.find(' ') != -1:
            spaceIndex = self.answer.find(' ')
            self.hiddenAnswer = self.hiddenAnswer[:spaceIndex] + ' ' + self.hiddenAnswer[spaceIndex + 1:]

    def newGame(self):

        if self.p1.get() == 1:
            name = self.p1Name.get()
            self.pl1 = Player(name)
            self.playerCount += 1
            self.p1Points.configure(font=('Helvetica', 20), text=self.pl1.name + ' ' + str(self.pl1.points))
            self.p1Points.grid(row=5, column=5, columnspan=3)
        if self.p2.get() == 1:
            name = self.p2Name.get()
            self.pl2 = Player(name)
            self.playerCount += 1
            self.p2Points.configure(font=('Helvetica', 20), text=self.pl2.name + ' ' + str(self.pl2.points))
            self.p2Points.grid(row=6, column=5, columnspan=3)
        if self.p3.get() == 1:
            name = self.p3Name.get()
            self.pl3 = Player(name)
            self.playerCount += 1
            self.p3Points.configure(font=('Helvetica', 20), text=self.pl3.name + ' ' + str(self.pl3.points))
            self.p3Points.grid(row=7, column=5, columnspan=3)
        if self.p4.get() == 1:
            name = self.p4Name.get()
            self.pl4 = Player(name)
            self.playerCount += 1
            self.p4Points.configure(font=('Helvetica', 20), text=self.pl4.name + ' ' + str(self.pl4.points))
            self.p4Points.grid(row=8, column=5, columnspan=3)
        if self.p5.get() == 1:
            name = self.p5Name.get()
            self.pl5 = Player(name)
            self.playerCount += 1
            self.p5Points.configure(font=('Helvetica', 20), text=self.pl5.name + ' ' + str(self.pl5.points))
            self.p5Points.grid(row=9, column=5, columnspan=3)

        if self.p1.get() == 1 or self.p2.get() == 1 or self.p3.get() == 1 or self.p4.get() == 1 or self.p5.get() == 1:
            self.endGameButton.configure(state='enabled')
        else:
            self.endGameButton.configure(state='disabled')

        self.newGameButton.configure(state='disabled')
        self.endGameButton.configure(state='enabled')

        self.roundCounter += 1
        self.roundLabel.configure(text='Runda' + str(self.roundCounter) + '/3')
        self.playerOrder = np.random.permutation(np.arange(1, self.playerCount + 1))[:self.playerCount]
        self.getQuestion()

        self.answerLabel.configure(font=('Helvetica', 30), text=self.hiddenAnswer)
        self.answerLabel.grid(row=4, column=5, columnspan=3)

        if self.playerOrder[0] == 1:
            self.currentPlayer = self.pl1.name
        elif self.playerOrder[0] == 2:
            self.currentPlayer = self.pl2.name
        elif self.playerOrder[0] == 3:
            self.currentPlayer = self.pl3.name
        elif self.playerOrder[0] == 4:
            self.currentPlayer = self.pl4.name
        elif self.playerOrder[0] == 5:
            self.currentPlayer = self.pl5.name
        self.queueLabel.configure(font=('Helvetica', 30), text="Kolej gracza " + self.currentPlayer)
        self.spinTheWheelButton.configure(state='enabled')

    def spin(self):
        rotateCount = random.randint(0, 20)
        image = Image.open("tarcza1.png")
        imRotate = image.rotate(17 * rotateCount)
        imRotate.save("tarczacopy.png")
        image = Image.open("tarczacopy.png")
        self.im = ImageTk.PhotoImage(image)
        self.base.create_image(0, 0, image=self.im, anchor=NW)
        self.turnPoints = self.wheelValues[rotateCount]
        if self.turnPoints != 0:
            self.turnPointsLabel.configure(text="Grasz o " + str(self.turnPoints) + " pkt")
            self.guessLetterButton.configure(state='enabled')
        else:
            self.turnPointsLabel.configure(text="Tracisz turę i wszystkie punkty")
            self.endTurnButton.configure(state='enabled')
            if self.currentPlayer == self.pl1.name:
                self.pl1.points = 0
                print(self.pl1.points)
                self.p1Points.configure(text=self.pl1.name + ' ' + str(self.pl1.points))
            elif self.currentPlayer == self.pl2.name:
                self.pl2.points = 0
                self.p2Points.configure(text=self.pl2.name + ' ' + str(self.pl2.points))
            elif self.currentPlayer == self.pl3.name:
                self.pl3.points = 0
                self.p3Points.configure(text=self.pl3.name + ' ' + str(self.pl3.points))
            elif self.currentPlayer == self.pl4.name:
                self.pl4.points = 0
                self.p4Points.configure(text=self.pl4.name + ' ' + str(self.pl4.points))
            elif self.currentPlayer == self.pl5.name:
                self.pl5.points = 0
                self.p5Points.configure(text=self.pl5.name + ' ' + str(self.pl5.points))
        self.spinTheWheelButton.configure(state='disabled')

    def guessLetter(self):

        self.letterAsker = simpledialog.askstring(prompt="Podaj literę", title='Podaj literę')
        self.letterAsker = self.letterAsker.upper()
        if len(self.letterAsker) > 1:
            self.letterAsker = self.letterAsker[:1]
        if self.answer.find(self.letterAsker) != -1 and self.hiddenAnswer.find(self.letterAsker) == -1:
            list = [m.start() for m in re.finditer(self.letterAsker, self.answer)]
            for i in list:
                self.hiddenAnswer = self.hiddenAnswer[:i] + self.letterAsker + self.hiddenAnswer[i + 1:]
            self.answerLabel.configure(font=('Helvetica', 30), text=self.hiddenAnswer)
            if self.turnPoints > 0:
                if self.currentPlayer == self.pl1.name:
                    self.pl1.points += self.turnPoints
                    self.p1Points.configure(text=self.pl1.name + ' ' + str(self.pl1.points))
                elif self.currentPlayer == self.pl2.name:
                    self.pl2.points += self.turnPoints
                    self.p2Points.configure(text=self.pl2.name + ' ' + str(self.pl2.points))
                elif self.currentPlayer == self.pl3.name:
                    self.pl3.points += self.turnPoints
                    self.p3Points.configure(text=self.pl3.name + ' ' + str(self.pl3.points))
                elif self.currentPlayer == self.pl4.name:
                    self.pl4.points += self.turnPoints
                    self.p4Points.configure(text=self.pl4.name + ' ' + str(self.pl4.points))
                elif self.currentPlayer == self.pl5.name:
                    self.pl5.points += self.turnPoints
                    self.p5Points.configure(text=self.pl5.name + ' ' + str(self.pl5.points))
            self.guessAnswerButton.configure(state='enabled')
        else:
            if self.turnPoints < 0:
                if self.currentPlayer == self.pl1.name:
                    self.pl1.points += self.turnPoints
                    self.p1Points.configure(text=self.pl1.name + ' ' + str(self.pl1.points))
                elif self.currentPlayer == self.pl2.name:
                    self.pl2.points += self.turnPoints
                    self.p2Points.configure(text=self.pl2.name + ' ' + str(self.pl2.points))
                elif self.currentPlayer == self.pl3.name:
                    self.pl3.points += self.turnPoints
                    self.p3Points.configure(text=self.pl3.name + ' ' + str(self.pl3.points))
                elif self.currentPlayer == self.pl4.name:
                    self.pl4.points += self.turnPoints
                    self.p4Points.configure(text=self.pl4.name + ' ' + str(self.pl4.points))
                elif self.currentPlayer == self.pl5.name:
                    self.pl5.points += self.turnPoints
                    self.p5Points.configure(text=self.pl5.name + ' ' + str(self.pl5.points))

        self.guessLetterButton.configure(state='disabled')
        self.endTurnButton.configure(state='enabled')

    def pointsToXML(self):
        for x in self.playerOrder:
            wynik = SubElement(root, 'wynik', kategoria='runda')

            if x == 1:
                SubElement(wynik, 'gracz').text = self.pl1.name
                points = SubElement(wynik, "punkty")
                points.text = str(self.pl1.points)
                self.pl1.total += self.pl1.points
                self.pl1.points = 0
                self.p1Points.configure(text=self.pl1.name + ' ' + str(self.pl1.points))
            elif x == 2:
                SubElement(wynik, 'gracz').text = self.pl2.name
                points = SubElement(wynik, "punkty")
                points.text = str(self.pl2.points)
                self.pl2.total += self.pl2.points
                self.pl2.points = 0
                self.p2Points.configure(text=self.pl2.name + ' ' + str(self.pl2.points))
            elif x == 3:
                SubElement(wynik, 'gracz').text = self.pl3.name
                points = SubElement(wynik, "punkty")
                points.text = str(self.pl3.points)
                self.pl3.total += self.pl3.points
                self.pl3.points = 0
                self.p3Points.configure(text=self.pl3.name + ' ' + str(self.pl3.points))
            elif x == 4:
                SubElement(wynik, 'gracz').text = self.pl4.name
                points = SubElement(wynik, "punkty")
                points.text = str(self.pl4.points)
                self.pl4.total += self.pl4.points
                self.pl4.points = 0
                self.p4Points.configure(text=self.pl4.name + ' ' + str(self.pl4.points))
            elif x == 5:
                SubElement(wynik, 'gracz').text = self.pl5.name
                points = SubElement(wynik, "punkty")
                points.text = str(self.pl5.points)
                self.pl5.total += self.pl5.points
                self.pl5.points = 0
                self.p5Points.configure(text=self.pl5.name + ' ' + str(self.pl5.points))
            SubElement(wynik, 'rodzaj').text = 'runda'

        ElementTree(root).write('round.xml', xml_declaration=True, encoding='utf-8', method='xml')

    def endRound(self):
        self.endRoundButton.configure(state='disabled')
        self.pointsToXML()
        self.roundCounter += 1
        if self.roundCounter <= 3:
            self.roundLabel.configure(text='Runda ' + str(self.roundCounter) + '/3')
            self.playerOrder = np.random.permutation(np.arange(1, self.playerCount + 1))[:self.playerCount]
            self.hiddenAnswer = ''
            self.getQuestion()
            self.answerLabel.configure(text=self.hiddenAnswer)

            self.spinTheWheelButton.configure(state='enabled')
            self.endTurnButton.configure(state='disabled')

            self.playerIndex = 0
            if self.playerOrder[self.playerIndex] == 1:
                self.currentPlayer = self.pl1.name
            elif self.playerOrder[self.playerIndex] == 2:
                self.currentPlayer = self.pl2.name
            elif self.playerOrder[self.playerIndex] == 3:
                self.currentPlayer = self.pl3.name
            elif self.playerOrder[self.playerIndex] == 4:
                self.currentPlayer = self.pl4.name
            elif self.playerOrder[self.playerIndex] == 5:
                self.currentPlayer = self.pl5.name
            self.queueLabel.configure(font=('Helvetica', 30), text="Kolej gracza " + self.currentPlayer)

        else:
            self.endGameButton.configure(state='enabled')

    def guessAnswer(self):
        self.guessAnswerButton.configure(state='disabled')
        self.answerAsker = simpledialog.askstring(prompt="Podaj hasło", title='Podaj hasło')
        self.answerAsker = self.answerAsker.upper()
        if self.answerAsker == self.answer:
            multiplier = self.hiddenAnswer.count('*')
            if self.currentPlayer == self.pl1.name:
                self.pl1.points *= multiplier
                self.p1Points.configure(text=self.pl1.name + ' ' + str(self.pl1.points))
            elif self.currentPlayer == self.pl2.name:
                self.pl2.points *= multiplier
                self.p2Points.configure(text=self.pl2.name + ' ' + str(self.pl2.points))
            elif self.currentPlayer == self.pl3.name:
                self.pl3.points *= multiplier
                self.p3Points.configure(text=self.pl3.name + ' ' + str(self.pl3.points))
            elif self.currentPlayer == self.pl4.name:
                self.pl4.points *= multiplier
                self.p4Points.configure(text=self.pl4.name + ' ' + str(self.pl4.points))
            elif self.currentPlayer == self.pl5.name:
                self.pl5.points *= multiplier
                self.p5Points.configure(text=self.pl5.name + ' ' + str(self.pl5.points))
            self.hiddenAnswer = self.answer
            self.answerLabel.configure(font=('Helvetica', 30), text=self.hiddenAnswer)
            self.endRoundButton.configure(state='enabled')
            self.endTurnButton.configure(state='disabled')

    def endTurn(self):
        self.playerIndex += 1
        if self.playerIndex == len(self.playerOrder):
            self.playerIndex = 0
        if self.playerOrder[self.playerIndex] == 1:
            self.currentPlayer = self.pl1.name
        elif self.playerOrder[self.playerIndex] == 2:
            self.currentPlayer = self.pl2.name
        elif self.playerOrder[self.playerIndex] == 3:
            self.currentPlayer = self.pl3.name
        elif self.playerOrder[self.playerIndex] == 4:
            self.currentPlayer = self.pl4.name
        elif self.playerOrder[self.playerIndex] == 5:
            self.currentPlayer = self.pl5.name
        self.queueLabel.configure(font=('Helvetica', 30), text="Kolej gracza " + self.currentPlayer)
        self.spinTheWheelButton.configure(state='enabled')
        self.endTurnButton.configure(state='disabled')

    def pointsFromXML(self):
        tree = parse('round.xml')
        elem = tree.getroot()
        for k in elem.findall('wynik'):
            name = k.find('gracz').text
            points = k.find('punkty').text
            type = k.find('rodzaj').text
            pointsToTable(str(name), int(str(points)), str(type))

    def endGame(self):
        for x in self.playerOrder:
            wynik = SubElement(root, 'wynik', kategoria='gra')
            if x == 1:
                SubElement(wynik, 'gracz').text = self.pl1.name
                points = SubElement(wynik, "punkty")
                points.text = str(self.pl1.total)
            elif x == 2:
                SubElement(wynik, 'gracz').text = self.pl2.name
                points = SubElement(wynik, "punkty")
                points.text = str(self.pl2.total)
            elif x == 3:
                SubElement(wynik, 'gracz').text = self.pl3.name
                points = SubElement(wynik, "punkty")
                points.text = str(self.pl3.total)
            elif x == 4:
                SubElement(wynik, 'gracz').text = self.pl4.name
                points = SubElement(wynik, "punkty")
                points.text = str(self.pl4.total)
            elif x == 5:
                SubElement(wynik, 'gracz').text = self.pl5.name
                points = SubElement(wynik, "punkty")
                points.text = str(self.pl5.total)
            SubElement(wynik, 'rodzaj').text = 'gra'
        ElementTree(root).write('round.xml', xml_declaration=True, encoding='utf-8', method='xml')
        self.endGameButton.configure(state='disabled')
        self.pointsFromXML()

    def showScores(self):
        scores = get_score('runda')
        self.bestScoreLabel1.configure(text='Najlepsza runda: ' + str(scores[0]))
        self.bestScoreLabel2.configure(text='Najlepsza runda: ' + str(scores[1]))
        self.bestScoreLabel3.configure(text='Najlepsza runda: ' + str(scores[2]))
        scores = get_score('gra')
        self.bestScoreLabel4.configure(text='Najlepsza gra: ' + str(scores[0]))
        self.bestScoreLabel5.configure(text='Najlepsza gra: ' + str(scores[1]))
        self.bestScoreLabel6.configure(text='Najlepsza gra: ' + str(scores[2]))

    def initialize(self):

        self.parent.title("Koło Fortuny")
        self.style.theme_use('clam')
        self.style.configure('.', font=('Helvetica', 12))
        self.pack(fill=BOTH, expand=1)
        self.columnconfigure(5, weight=1)

        self.newGameButton.grid(row=1, column=0, pady=10, padx=10, sticky=W + N)
        self.bestScoreButton.grid(row=1, column=1, pady=10, padx=10, sticky=W + N)

        self.roundLabel.configure(font=('Helvetica', 20))
        self.roundLabel.grid(row=1, column=2, pady=1, padx=10, sticky=W)

        self.questionLabel.configure(font=('Helvetica', 15), wraplength=700, justify='center')
        self.questionLabel.grid(row=1, column=3, columnspan=5, pady=5, padx=5, sticky=E + N)

        self.p1CheckBox.grid(row=2, column=0, pady=1, padx=10, sticky=E)
        self.p1Name.insert(END, "Gracz 1")
        self.p1Name.grid(row=3, column=0, pady=1, padx=10, sticky=E)

        self.p2CheckBox.grid(row=5, column=0, pady=1, padx=10, sticky=E)
        self.p2Name.insert(END, "Gracz 2")
        self.p2Name.grid(row=6, column=0, pady=1, padx=10, sticky=E)

        self.p3CheckBox.grid(row=8, column=0, pady=1, padx=10, sticky=E)
        self.p3Name.insert(END, "Gracz 3")
        self.p3Name.grid(row=9, column=0, pady=1, padx=10, sticky=E)

        self.p4CheckBox.grid(row=10, column=0, pady=1, padx=10, sticky=E)
        self.p4Name.insert(END, "Gracz 4")
        self.p4Name.grid(row=11, column=0, pady=1, padx=10, sticky=E)

        self.p5CheckBox.grid(row=13, column=0, pady=1, padx=10, sticky=E)
        self.p5Name.insert(END, "Gracz 5")
        self.p5Name.grid(row=14, column=0, pady=1, padx=10, sticky=E)

        self.endGameButton.grid(row=16, column=0, pady=1, padx=10, sticky=S)
        self.endGameButton.config(state='disabled')

        self.base.grid(row=3, column=1, pady=5, padx=50, sticky=E + W + S + N, columnspan=3, rowspan=20)
        self.base.create_image(0, 0, image=self.im, anchor=NW)

        self.guessLetterButton.grid(row=3, column=5, sticky=W)
        self.spinTheWheelButton.grid(row=3, column=6, padx=25, sticky=W)
        self.guessAnswerButton.grid(row=3, column=7, padx=50, sticky=W)
        self.queueLabel.grid(row=10, column=5, columnspan=3)
        self.turnPointsLabel.grid(row=11, column=5, columnspan=3)
        self.endTurnButton.grid(row=12, column=5, columnspan=2)
        self.endRoundButton.grid(row=12, column=7, columnspan=2)
        self.bestScoreLabel1.grid(row=13, column=5, columnspan=3)
        self.bestScoreLabel2.grid(row=14, column=5, columnspan=3)
        self.bestScoreLabel3.grid(row=15, column=5, columnspan=3)
        self.bestScoreLabel4.grid(row=16, column=5, columnspan=3)
        self.bestScoreLabel5.grid(row=17, column=5, columnspan=3)
        self.bestScoreLabel6.grid(row=18, column=5, columnspan=3)


def main():
    gui = Tk()
    gui.geometry('1280x720')
    app = Window(gui)
    gui.mainloop()


if __name__ == '__main__':
    main()
