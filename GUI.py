import os
import pprint
import random
import wx
import CreateData
import Poisson
import Bayesian
import MLR
import SeasonAnalysis
import M_TeamAnalysis
import Mixed_TeamAnalysis
import P_TeamAnalysis
import B_TeamAnalysis
import ParameterAnalysis
import DataAnalysis
import datetime as dt
import sys
import time
import ModelEvaluation
import Mixed

import matplotlib
matplotlib.use('WXAgg')
import matplotlib.pyplot as plt


from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)

class BarsFrame(wx.Frame):
	title = 'Data Visualization and Predictive Analysis of Football teams'
    
	def __init__(self):
		wx.Frame.__init__(self, None, -1, self.title)
         
		self.create_main_panel()
		#self.textbox.SetValue("Set season here")
		#self.textbox1.SetValue("Set team here")
		

	def create_main_panel(self):
		self.panel = wx.Panel(self)
		#self.panel.SetBackgroundColour("#1100")
		#self.panel.SetBackgroundColour("maroon")

		#self.dpi = 50		
		self.figure = Figure(figsize=(13,5))

		self.axes = self.figure.add_subplot(111)
		self.canvas = FigureCanvas(self.panel, -1,  self.figure)
        
		self.textbox = wx.TextCtrl(self.panel, size=(200,-1),style=wx.TE_PROCESS_ENTER)
		self.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter, self.textbox)
	
		self.textbox1 = wx.TextCtrl(self.panel, size=(200,-1),style=wx.TE_PROCESS_ENTER)
		self.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter, self.textbox1)
        
		self.drawbutton = wx.Button(self.panel, -1, "Set Season Stats")
		self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton)
	
		#self.drawbutton1 = wx.Button(self.panel, -1, "Run Model")
		#self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton1)

		self.drawbutton2 = wx.Button(self.panel, -1, "Home Goal Distribution")
		self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton2)

		self.drawbutton3 = wx.Button(self.panel, -1, "Away Goal Distribution")
		self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton3)

		#self.drawbutton4 = wx.Button(self.panel, -1, "Show Team Performance")
		#self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton4)

		self.drawbutton5 = wx.Button(self.panel, -1, "Plot Away Probabilities")
		self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton5)

		self.drawbutton6 = wx.Button(self.panel, -1, "Plot Home Probabilities")
		self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton6)

		self.drawbutton7 = wx.Button(self.panel, -1, "Plot Effects")
		self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton7)

		self.drawbutton8 = wx.Button(self.panel, -1, "Home Scoring Intensity")
		self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton8)		

		self.drawbutton9 = wx.Button(self.panel, -1, "Away Scoring Intensity")
		self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton9)

		self.drawbutton10 = wx.Button(self.panel, -1, "Show Bayesian Performance")
		self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton10)

		self.drawbutton11 = wx.Button(self.panel, -1, "Run Bayesian Model")
		self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton11)

		self.drawbutton12 = wx.Button(self.panel, -1, "Run Poisson Model")
		self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton12)

		self.drawbutton13 = wx.Button(self.panel, -1, "Show Poisson Performance")
		self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton13)

		self.drawbutton131 = wx.Button(self.panel, -1, "R2 for Poisson")
		self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton131)

		self.drawbutton141 = wx.Button(self.panel, -1, "R2 for Bayesian")
		self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton141)

		self.drawbutton151 = wx.Button(self.panel, -1, "R2 for MLR")
		self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton151)

		self.drawbutton14 = wx.Button(self.panel, -1, "Run MLR Model")
		self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton14)

		self.drawbutton15 = wx.Button(self.panel, -1, "Season Home Analysis")
		self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton15)

		self.drawbutton16 = wx.Button(self.panel, -1, "Season Away Analysis")
		self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton16)

		self.drawbutton17 = wx.Button(self.panel, -1, "Show MLR Performance")
		self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton17)

		self.drawbutton18 = wx.Button(self.panel, -1, "Run Mixed Model")
		self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton18)

		self.drawbutton19 = wx.Button(self.panel, -1, "Show Mixed Performance")
		self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton19)

		self.drawbutton20 = wx.Button(self.panel, -1, "R2 for Mixed")
		self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton20)

		self.drawbutton21 = wx.Button(self.panel, -1, "Save Plot")
		self.Bind(wx.EVT_BUTTON, self.on_save_plot, self.drawbutton21)
	
		self.cb1=wx.RadioButton(self.panel, -1, "Shots")
		self.cb1.SetValue(0)
		self.cb1.Bind(wx.EVT_RADIOBUTTON, self.on_parameter_selection)

		self.cb2=wx.RadioButton(self.panel, -1, "Shots on Target")
		self.cb2.Bind(wx.EVT_RADIOBUTTON, self.on_parameter_selection)

		self.cb3=wx.RadioButton(self.panel, -1, "Corners")
		self.cb3.Bind(wx.EVT_RADIOBUTTON, self.on_parameter_selection)	

		self.cb4=wx.RadioButton(self.panel, -1, "Fouls")
		self.cb4.Bind(wx.EVT_RADIOBUTTON, self.on_parameter_selection)

		self.cb5=wx.RadioButton(self.panel, -1, "Offsides")
		self.cb5.Bind(wx.EVT_RADIOBUTTON, self.on_parameter_selection)

		self.cb6=wx.RadioButton(self.panel, -1, "YellowCards")
		self.cb6.Bind(wx.EVT_RADIOBUTTON, self.on_parameter_selection)

		self.cb7=wx.RadioButton(self.panel, -1, "RedCards")
		self.cb7.Bind(wx.EVT_RADIOBUTTON, self.on_parameter_selection)


		self.log = wx.TextCtrl(self.panel, wx.ID_ANY,style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
		self.redir=RedirectText(self.log)
		sys.stdout=self.redir


		self.font = wx.Font(15, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
		self.p_heading = wx.StaticText(self.panel, label="Poisson Model",style=wx.BOLD)
		self.p_heading.SetFont(self.font)
		self.b_heading = wx.StaticText(self.panel, label="Bayesian Model",style=wx.ALIGN_CENTER)
		self.b_heading.SetFont(self.font)
		self.m_heading = wx.StaticText(self.panel, label="MLR Model",style=wx.ALIGN_CENTER)
		self.m_heading.SetFont(self.font)
		self.mixed_heading = wx.StaticText(self.panel, label="Mixed Model",style=wx.ALIGN_CENTER)
		self.mixed_heading.SetFont(self.font)
		self.a_heading = wx.StaticText(self.panel, label="Team Analysis",style=wx.ALIGN_CENTER)
		self.a_heading.SetFont(self.font)
		self.season_heading = wx.StaticText(self.panel, label="Enter Season",style=wx.ALIGN_CENTER)
		self.season_heading.SetFont(self.font)
		self.team_heading = wx.StaticText(self.panel, label="Enter Team",style=wx.ALIGN_CENTER)
		self.team_heading.SetFont(self.font)
		
        
        #
        # Layout with box sizers
        #
		flags = wx.ALIGN_LEFT | wx.ALL | wx.ALIGN_CENTER_VERTICAL
		self.vbox = wx.BoxSizer(wx.VERTICAL)
		self.hbox = wx.BoxSizer(wx.HORIZONTAL)
		self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)

		self.vbox2 = wx.BoxSizer(wx.VERTICAL)
		self.vbox_cp = wx.BoxSizer(wx.VERTICAL)

		self.hbox_po = wx.BoxSizer(wx.HORIZONTAL)

		self.hbox_bay = wx.BoxSizer(wx.HORIZONTAL)

		self.hbox_mlr = wx.BoxSizer(wx.HORIZONTAL)

		self.hbox_mixed = wx.BoxSizer(wx.HORIZONTAL)

		self.hbox_log = wx.BoxSizer(wx.HORIZONTAL)
		self.hbox_log.AddSpacer(10)
		self.hbox_log.Add(self.log, 1, flag=wx.EXPAND)
		self.hbox_log.AddSpacer(10)
		
		self.vbox.AddSpacer(10)
		self.vbox.Add(self.hbox_log, 1, flag=wx.EXPAND)
		self.vbox.AddSpacer(10)
		self.vbox.Add(self.hbox1, 0, flag = wx.ALIGN_LEFT | wx.TOP)

		self.hbox1.Add(self.canvas, 0, wx.LEFT | wx.TOP | wx.GROW)
		self.hbox1.Add(self.vbox_cp, 0, flag = wx.ALIGN_LEFT | wx.TOP)

		self.vbox_cp.Add(self.season_heading, 0, border=3, flag=flags)		
		self.vbox_cp.Add(self.textbox, 0, border=3, flag=flags)
		self.vbox_cp.Add(self.drawbutton, 0, border=3, flag=flags)
		self.vbox_cp.Add(self.team_heading, 0, border=3, flag=flags)
		self.vbox_cp.Add(self.textbox1, 0, border=3, flag=flags)
		self.vbox_cp.Add(self.a_heading, 0, border=3, flag=flags)
		self.vbox_cp.Add(self.cb1)
		self.vbox_cp.Add(self.cb2)
		self.vbox_cp.Add(self.cb3)
		self.vbox_cp.Add(self.cb4)
		self.vbox_cp.Add(self.cb5)
		self.vbox_cp.Add(self.cb6)
		self.vbox_cp.Add(self.cb7)
		self.vbox_cp.Add(self.drawbutton21, 0, border=3, flag=flags)
		self.vbox.AddSpacer(10)
	
		self.vbox.Add(self.vbox2, 0, flag = wx.ALIGN_LEFT | wx.TOP)
		
		
		self.hbox_po.Add(self.drawbutton12, 0, border=3, flag=flags)
		self.hbox_po.Add(self.drawbutton2, 0, border=3, flag=flags)
		self.hbox_po.Add(self.drawbutton3, 0, border=3, flag=flags)
		self.hbox_po.Add(self.drawbutton5, 0, border=3, flag=flags)
		self.hbox_po.Add(self.drawbutton6, 0, border=3, flag=flags)
		self.hbox_po.Add(self.drawbutton13, 0, border=3, flag=flags)
		self.hbox_po.Add(self.drawbutton131, 0, border=3, flag=flags)
		
		self.hbox_bay.Add(self.drawbutton11, 0, border=3, flag=flags)
		self.hbox_bay.Add(self.drawbutton7, 0, border=3, flag=flags)
		self.hbox_bay.Add(self.drawbutton8, 0, border=3, flag=flags)
		self.hbox_bay.Add(self.drawbutton9, 0, border=3, flag=flags)
		self.hbox_bay.Add(self.drawbutton10, 0, border=3, flag=flags)
		self.hbox_bay.Add(self.drawbutton141, 0, border=3, flag=flags)
		
		self.hbox_mlr.Add(self.drawbutton14, 0, border=3, flag=flags)
		self.hbox_mlr.Add(self.drawbutton15, 0, border=3, flag=flags)
		self.hbox_mlr.Add(self.drawbutton16, 0, border=3, flag=flags)
		self.hbox_mlr.Add(self.drawbutton17, 0, border=3, flag=flags)
		self.hbox_mlr.Add(self.drawbutton151, 0, border=3, flag=flags)

		self.hbox_mixed.Add(self.drawbutton18, 0, border=3, flag=flags)
		self.hbox_mixed.Add(self.drawbutton19, 0, border=3, flag=flags)
		self.hbox_mixed.Add(self.drawbutton20, 0, border=3, flag=flags)

		self.vbox2.Add(self.p_heading, 0, flag=flags)		
		self.vbox2.Add(self.hbox_po, 0, flag = wx.ALIGN_LEFT | wx.TOP)
		self.vbox2.Add(self.b_heading, 0, flag=flags)
		self.vbox2.Add(self.hbox_bay, 0, flag = wx.ALIGN_LEFT | wx.TOP)
		self.vbox2.Add(self.m_heading, 0, flag=flags)
		self.vbox2.Add(self.hbox_mlr, 0, flag = wx.ALIGN_LEFT | wx.TOP)
		self.vbox2.Add(self.mixed_heading, 0, flag=flags)
		self.vbox2.Add(self.hbox_mixed, 0, flag = wx.ALIGN_LEFT | wx.TOP)

		#self.hbox.AddSpacer(30)
        
		self.vbox.Add(self.hbox, 0, flag = wx.ALIGN_LEFT | wx.TOP)

		self.panel.SetSizer(self.vbox)

		self.vbox.Fit(self)
    
	def create_status_bar(self):
		self.statusbar = self.CreateStatusBar()

	def draw_figure(self):
		CreateData.season=self.textbox.GetValue()
		CreateData.setSeasonStats()

	def runPoissonModel(self):
		Poisson.RunModel()

	def runBayesianModel(self):
		Bayesian.RunModel()

	def runMixedModel(self):
		Mixed.RunModel()
	
	def runMLRModel(self):
		MLR.RunModel()

	def plotHomeDist(self):
		SeasonAnalysis.getHomeGoalDist()

	def plotAwayDist(self):
		SeasonAnalysis.getAwayGoalDist()

	def plotPPerformance(self):

		P_TeamAnalysis.team = self.textbox1.GetValue()		
		team = self.textbox1.GetValue()
		season = self.textbox.GetValue()
		P_TeamAnalysis.setTeamStats()
		plot_cordinates = P_TeamAnalysis.ShowPerformance()
		y1 = plot_cordinates[0]
		y2 = plot_cordinates[1]
		x = plot_cordinates[2]
		self.axes.cla()
		self.axes.plot(x, y1,color='green',marker='v')
		self.axes.plot(x, y2,color='cyan',marker='o')
		m = plt.scatter(0,0,color='green')
		n = plt.scatter(0,0,color='cyan')
		self.axes.legend((m, n), ('Observed', 'Predictied'), scatterpoints=1, loc='upper left', ncol=3, fontsize=15)
		self.axes.set_ylim([0,max(max(y1),max(y2))])
		self.axes.set_title("Plot to show the performance of "+team+" in "+season+" season")
		self.canvas.draw()

	def plotBPerformance(self):

		B_TeamAnalysis.team = self.textbox1.GetValue()		
		team = self.textbox1.GetValue()
		season = self.textbox.GetValue()
		B_TeamAnalysis.setTeamStats()
		plot_cordinates = B_TeamAnalysis.ShowPerformance()
		y1 = plot_cordinates[0]
		y2 = plot_cordinates[1]
		x = plot_cordinates[2]
		self.axes.cla()
		self.axes.plot(x, y1,color='green',marker='v')
		self.axes.plot(x, y2,color='cyan',marker='o')
		m = plt.scatter(0,0,color='green')
		n = plt.scatter(0,0,color='cyan')
		self.axes.legend((m, n), ('Observed', 'Predictied'), scatterpoints=1, loc='upper left', ncol=3, fontsize=15)
		self.axes.set_ylim([0,max(max(y1),max(y2))])
		self.axes.set_title("Plot to show the performance of "+team+" in "+season+" season")
		self.canvas.draw()

	def plotMPerformance(self):

		M_TeamAnalysis.team = self.textbox1.GetValue()		
		team = self.textbox1.GetValue()
		season = self.textbox.GetValue()
		M_TeamAnalysis.setTeamStats()
		plot_cordinates = M_TeamAnalysis.ShowPerformance()
		y1 = plot_cordinates[0]
		y2 = plot_cordinates[1]
		x = plot_cordinates[2]
		self.axes.cla()
		self.axes.plot(x, y1,color='green',marker='v')
		self.axes.plot(x, y2,color='cyan',marker='o')
		m = plt.scatter(0,0,color='green')
		n = plt.scatter(0,0,color='cyan')
		self.axes.legend((m, n), ('Observed', 'Predictied'), scatterpoints=1, loc='upper left', ncol=3, fontsize=15)
		self.axes.set_ylim([0,max(max(y1),max(y2))])
		self.axes.set_title("Plot to show the performance of "+team+" in "+season+" season")
		self.canvas.draw()

	def plotMiPerformance(self):
		Mixed_TeamAnalysis.team = self.textbox1.GetValue()		
		team = self.textbox1.GetValue()
		season = self.textbox.GetValue()
		Mixed_TeamAnalysis.setTeamStats()
		plot_cordinates = Mixed_TeamAnalysis.ShowPerformance()
		y1 = plot_cordinates[0]
		y2 = plot_cordinates[1]
		x = plot_cordinates[2]
		self.axes.cla()
		self.axes.plot(x, y1,color='green',marker='v')
		self.axes.plot(x, y2,color='cyan',marker='o')
		m = plt.scatter(0,0,color='green')
		n = plt.scatter(0,0,color='cyan')
		self.axes.legend((m, n), ('Observed', 'Predictied'), scatterpoints=1, loc='upper left', ncol=3, fontsize=15)
		self.axes.set_ylim([0,max(max(y1),max(y2))])
		self.axes.set_title("Plot to show the performance of "+team+" in "+season+" season")
		self.canvas.draw()

	def plotAwayProb(self):
		P_TeamAnalysis.team = self.textbox1.GetValue()
		P_TeamAnalysis.setTeamStats()
		P_TeamAnalysis.plotAwayResultProbabilities()

	def plotHomeProb(self):
		P_TeamAnalysis.team = self.textbox1.GetValue()
		P_TeamAnalysis.setTeamStats()
		P_TeamAnalysis.plotHomeResultProbabilities()

	def plotEffect(self):
		ParameterAnalysis.plotEffects()

	def plotHome_Theta(self):
		ParameterAnalysis.plotHomeTheta()

	def plotAway_Theta(self):
		ParameterAnalysis.plotAwayTheta()

	def plotSeasonHomeAnalysis(self):
		SeasonAnalysis.plotAtHome()

	def plotSeasonAwayAnalysis(self):
		SeasonAnalysis.plotAtAway()

	def plotR2(self,model):
		ModelEvaluation.SeasonPerformers(model)
		
	def on_draw_button(self, event):
		label = event.GetEventObject().GetLabel()
		if(label == "Set Season Stats"):
			self.draw_figure()
		elif(label == "Run Poisson Model"):
			self.runPoissonModel()
		elif(label == "Home Goal Distribution"):
			self.plotHomeDist()
		elif(label == "Away Goal Distribution"):
			self.plotAwayDist()
		elif(label == "Plot Home Probabilities"):
			self.plotHomeProb()
		elif(label == "Plot Away Probabilities"):
			self.plotAwayProb()
		elif(label == "Show Poisson Performance"):
			self.plotPPerformance()
		elif(label == "R2 for Poisson"):
			self.plotR2("p")

		elif(label == "Run Bayesian Model"):
			self.runBayesianModel()
		elif(label == "Plot Effects"):
			self.plotEffect()
		elif(label == "Home Scoring Intensity"):
			self.plotHome_Theta()
		elif(label == "Away Scoring Intensity"):
			self.plotAway_Theta()
		elif(label == "Show Bayesian Performance"):
			self.plotBPerformance()
		elif(label == "R2 for Bayesian"):
			self.plotR2("b")

		elif(label == "Run MLR Model"):
			self.runMLRModel()
		elif(label == "Season Home Analysis"):
			self.plotSeasonHomeAnalysis()
		elif(label == "Season Away Analysis"):
			self.plotSeasonAwayAnalysis()
		elif(label == "Show MLR Performance"):
			self.plotMPerformance()
		elif(label == "R2 for MLR"):
			self.plotR2("m")

		elif(label == "Run Mixed Model"):
			self.runMixedModel()
		elif(label == "Show Mixed Performance"):
			self.plotMiPerformance()
		elif(label == "R2 for Mixed"):
			self.plotR2("mixed")

		
	def animate(self):
		DataAnalysis.team = self.textbox1.GetValue()
		team = DataAnalysis.team
		DataAnalysis.season = self.textbox.GetValue()
		season = DataAnalysis.season
		label = self.attr
		attr1 = self.attr.split(' ')
		if len(attr1) > 1:
			str1 = str(attr1[0])
			str2 = str(attr1[-1])
			attr = str1[0]+str2[0]
		else:
			attr = attr1[0][0]
		
		DataAnalysis.attr = attr
		
		plot_cordinates = DataAnalysis.returnValues()
		x = plot_cordinates[0]
		y1 = plot_cordinates[1]
		y2 = plot_cordinates[2]
		sizes = plot_cordinates[3]
		self.axes.cla()
		self.axes.set_xlim(0,37)
		self.axes.set_ylim(0,max(max(y1),max(y2))+100)
		self.axes.grid(True)
		self.axes.set_title("The progression of "+team+" in terms of "+label+" during "+season)
		self.axes.set_xlabel("Match Number")
		self.axes.set_ylabel(attr)
		m = plt.scatter(0,0,color='green')
		n = plt.scatter(0,0,color='cyan')
		self.axes.legend((m, n), ('Home', 'Away'), scatterpoints=1, loc='upper left', ncol=3, fontsize=15)
		for i in range(38):
			self.axes.scatter(x[i],y1[i],s=sizes[i]*10,color='green',marker='o',edgecolors='black')
			self.axes.scatter(x[i],y2[i],s=sizes[i]*10,color='cyan',marker='o',edgecolors='black')
			self.canvas.draw()		
        
    
	def on_text_enter(self, event):
		self.draw_figure()


	def on_parameter_selection(self, e):
		label=e.GetEventObject().GetLabel()
		ch = e.GetEventObject().GetValue()
		if(ch & (label=="Shots")):
			self.attr = label
			self.animate()
		elif(ch & (label=="Shots on Target")):
			self.attr = label
			self.animate()
		elif(ch & (label=="Corners")):
			self.attr = label
			self.animate()
		elif(ch & (label=="Fouls")):
			self.attr = label
			self.animate()
		elif(ch & (label=="Offsides")):
			self.attr = label
			self.animate()
		elif(ch & (label=="YellowCards")):
			self.attr = label
			self.animate()
		elif(ch & (label=="RedCards")):
			self.attr = label
			self.animate()

	def on_save_plot(self, event):
		file_choices = "PNG (*.png)|*.png"
        
		dlg = wx.FileDialog(self, message="Save plot as...", defaultDir=os.getcwd(), defaultFile="plot.png", wildcard=file_choices, style=wx.SAVE)
        
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			self.canvas.print_figure(path)
			print("Figure saved")
			#self.flash_status_message("Saved to %s" % path)

        
	def on_exit(self, event):
		self.Destroy()
        

if __name__ == '__main__':
	app = wx.PySimpleApp(redirect=False)
	app.frame = BarsFrame()
	app.frame.Maximize(True)
	app.frame.Show()
	app.MainLoop()

