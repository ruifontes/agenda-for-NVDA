# -*- coding: UTF-8 -*-
# Part of Agenda add-on
# Module for add-on settings panel
# written by Abel Passos do Nascimento Jr. <abel.passos@gmail.com>, Rui Fontes <rui.fontes@tiflotecnia.com> and Ângelo Abrantes <ampa4374@gmail.com> and 
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# For update process
from .update import *
from configobj import ConfigObj
# For translation process
addonHandler.initTranslation()

# Read configuration on INI file to know where are the agenda.db files...
dirDatabase = os.path.join(os.path.dirname(__file__), "agenda.db")
firstDatabase = ""
altDatabase = ""
indexDB = 0

try:
	if config.conf[ourAddon.name]["xx"]:
		# index of agenda.db file to use
		indexDB = int(config.conf[ourAddon.name]["xx"])
		if indexDB == 0:
			dirDatabase = 				config.conf[ourAddon.name]["path"]
		else:
			dirDatabase = 				config.conf[ourAddon.name]["altPath"]
		firstDatabase = config.conf[ourAddon.name]["path"]
		altDatabase = config.conf[ourAddon.name]["altPath"]
except:
	# Not registered, so use the default path
	pass


class AgendaSettingsPanel(gui.SettingsPanel):
	# Translators: Title of the Agenda settings dialog in the NVDA settings.
	title = _("Agenda")

	def makeSettings(self, settingsSizer):
		settingsSizerHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

		# Translators: Checkbox name in the configuration dialog
		self.showNextAppointmentsWnd = wx.CheckBox(self, label = _("Show next appointments at startup"))
		self.showNextAppointmentsWnd.SetValue(config.conf[ourAddon.name]["show"])
		settingsSizerHelper.addItem(self.showNextAppointmentsWnd)

		# Translators: Checkbox name in the configuration dialog
		self.shouldUpdateChk = wx.CheckBox(self, label = _("Check for updates at startup"))
		self.shouldUpdateChk.SetValue(config.conf[ourAddon.name]["isUpgrade"])
		settingsSizerHelper.addItem(self.shouldUpdateChk)

		# Translators: Name of combobox with the agenda files path
		pathBoxSizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, label = _("Path of agenda files:"))
		pathBox = pathBoxSizer.GetStaticBox()
		pathGroup = guiHelper.BoxSizerHelper(self, sizer = pathBoxSizer)
		settingsSizerHelper.addItem(pathGroup)

		global firstDatabase
		if firstDatabase == "":
			firstDatabase = dirDatabase
		self.pathList = [firstDatabase, altDatabase]
		self.pathNameCB = pathGroup.addLabeledControl("", wx.Choice, choices = self.pathList)
		self.pathNameCB.SetSelection(indexDB)

		# Translators: This is the label for the button used to add or change a agenda.db location
		changePathBtn = wx.Button(pathBox, label = _("&Select or add a directory"))
		changePathBtn.Bind(wx.EVT_BUTTON,self.OnDirectory)

	def OnDirectory(self, event):
		self.Freeze()
		global dirDatabase, firstDatabase, altDatabase, indexDB
		lastDir = os.path.dirname(__file__)
		dDir = lastDir
		dFile = "agenda.db"
		frame = wx.Frame(None, -1, 'teste')
		frame.SetSize(0,0,200,50)
		dlg = wx.FileDialog(frame, _("Choose where to save the agenda file"), dDir, dFile,
				wildcard = _("Database files (*.db)"),
				style = wx.FD_SAVE)
		if dlg.ShowModal() == wx.ID_OK:
			fname = dlg.GetPath()
			index = self.pathNameCB.GetSelection()
			if index == 0:
				if os.path.exists(fname):
					firstDatabase = fname
				else:
					os.rename(firstDatabase, fname)
					firstDatabase = fname
			else:
				if os.path.exists(fname):
					altDatabase = fname
				else:
					if altDatabase == "":
						altDatabase = fname
					else:
						os.rename(altDatabase, fname)
						altDatabase = fname
			dirDatabase = fname
			self.pathList = [firstDatabase, altDatabase]
		dlg.Close() 
		self.onPanelActivated()
		self._sendLayoutUpdatedEvent()
		self.Thaw()
		event.Skip()

	def onSave (self):
		global dirDatabase, indexDB
		config.conf[ourAddon.name]["show"] = self.showNextAppointmentsWnd.GetValue()
		config.conf[ourAddon.name]["isUpgrade"] = self.shouldUpdateChk.GetValue()
		config.conf[ourAddon.name]["path"] = firstDatabase
		config.conf[ourAddon.name]["altPath"] = altDatabase
		config.conf[ourAddon.name]["xx"] = str(self.pathList.index(self.pathNameCB.GetStringSelection()))
		config.conf.save()
		indexDB = self.pathNameCB.GetSelection()
		dirDatabase = self.pathList[indexDB]

	def terminate(self):
		super(AgendaSettingsPanel, self).terminate()
		pass


