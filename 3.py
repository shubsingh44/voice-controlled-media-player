import wx
import wx.media
import os
import time
#import speech_recognition as sr

class Main(wx.Frame):
        def __init__(self,parent,title):

                wx.Frame.__init__(self,None,title=title,size=(800,650))
                panel=wx.Panel(self)
              
                self.mplay = wx.media.MediaCtrl(self,-1,"", wx.Point(0,0),wx.Size(800,450)) #media constructor
                menubar=wx.MenuBar()#create a Menubar object mtlb upar wali line
          
                Mediamenu=wx.Menu()#create a menu object mtlb line ka first option
                Mediafirst=Mediamenu.Append(wx.ID_OPEN,'Open File','Open Media File')#first option ka pehla part
                Mediasecond=Mediamenu.Append(wx.ID_ANY,'Open Playlist','Open Your Playlist')
                Mediathird=Mediamenu.Append(wx.ID_ANY,'Open Disc','Open disc in system')
                Mediafourth=Mediamenu.Append(wx.ID_EXIT,'Quit','Quit Application')

                Playback=wx.Menu()
                Playfirst=Playback.Append(wx.ID_ANY,'Play','Play your Media File')
                Playsecond=Playback.Append(wx.ID_ANY,'Pause','Stop your Media File')
                Playthird=Playback.Append(wx.ID_ANY,'Stop','Play previous Media File')
                Playfourth=Playback.Append(wx.ID_ANY,'Next','Play next Media File')

                submenu=wx.Menu()#creating a submenu
                submenu1 = submenu.Append(wx.ID_ANY,"0.25")#creating 1 submenu
                submenu2 = submenu.Append(wx.ID_ANY,"0.50")#creating 2 submenu
                submenu3 = submenu.Append(wx.ID_ANY,"NORMAL")#creating 3 submenu
                submenu4 = submenu.Append(wx.ID_ANY,"1.25")#creating 4 submenu
                submenu5 = submenu.Append(wx.ID_ANY,"1.50")#creating 5 submenu
                submenu6=  submenu.Append(wx.ID_ANY,"2.0")#creating 6 submenu
                Playback.AppendMenu(wx.ID_ANY, "Speed", submenu)#submenu of Speed
        
                Sp=wx.Menu()
  
                Spfirst=Sp.Append(wx.ID_ANY,'Start Listening','Enable Listener')
                Spsecond=Sp.Append(wx.ID_ANY,'Stop Listening','Disable Listener')

                Sub=wx.Menu()
                Addsub=Sub.Append(wx.ID_ANY,'Add subtitle file','Add subtitles')

                menubar.Append(Mediamenu,'&Media')
                menubar.Append(Playback,'&Playback')
                menubar.Append(Sp,'&Speech')
                menubar.Append(Sub,'&Subtitle')
                
                Hel=wx.Menu()
                hel=Hel.Append(wx.ID_ANY,'Help','Help')
                About=Hel.Append(wx.ID_ANY,'About','About')

                menubar.Append(Hel,'&Help')

                self.SetMenuBar(menubar)
                self.CreateStatusBar()   #To create the bottom bar
                self.StatusBar.SetBackgroundColour((220,220,220))


                #adding sizers
                mainSizer=wx.BoxSizer(wx.VERTICAL)
                sliderSizer=wx.BoxSizer(wx.HORIZONTAL)

                
                #play button
                
                pic=wx.Image("play.bmp",wx.BITMAP_TYPE_BMP).ConvertToBitmap()
                self.button=wx.BitmapButton(self,-1,pic,pos=(400,500),size=(40,40))
                self.Bind(wx.EVT_BUTTON,self.on_pause,self.button)
                mainSizer.Add(self.button,1,wx.ALL,5)
                if self.mplay.GetState()==2:
                   self.button.Hide()

                 #pause butoon

                pic1=wx.Image("pause.bmp",wx.BITMAP_TYPE_BMP).ConvertToBitmap()
                self.button1=wx.BitmapButton(self,-1,pic1,pos=(400,500),size=(40,40))
                self.Bind(wx.EVT_BUTTON,self.on_pause,self.button1)
                mainSizer.Add(self.button1,1,wx.ALL,5)
                if self.mplay.GetState()==1:
                   self.button1.Hide()

                 #forward button
                   
                pic2=wx.Image("for.bmp",wx.BITMAP_TYPE_BMP).ConvertToBitmap()
                self.button2=wx.BitmapButton(self,-1,pic2,pos=(450,500),size=(40,40))
                self.Bind(wx.EVT_BUTTON,self.on_forward,self.button2)
                mainSizer.Add(self.button2,1,wx.ALL,5)

                #backward button
                   
                pic3=wx.Image("back.bmp",wx.BITMAP_TYPE_BMP).ConvertToBitmap()
                self.button3=wx.BitmapButton(self,-1,pic3,pos=(350,500),size=(40,40))
                self.Bind(wx.EVT_BUTTON,self.on_backward,self.button3)
                mainSizer.Add(self.button3,1,wx.ALL,5)
                
                # create volume control
                self.volumeCtrl = wx.Slider(self,value=90,minValue=0,maxValue=100,pos=(600,500),style = wx.SL_HORIZONTAL|wx.SL_LABELS)
                self.volumeCtrl.Bind(wx.EVT_SLIDER,self.on_set_volume)
                sliderSizer.Add(self.volumeCtrl,1,wx.ALL,5)

                #voice
                pic4=wx.Image("speech.bmp",wx.BITMAP_TYPE_BMP).ConvertToBitmap()
                self.button4=wx.BitmapButton(self,-1,pic4,pos=(200,500),size=(40,40))
                self.Bind(wx.EVT_BUTTON,self.Onlisten,self.button4)
                
                

                #create track counter
                self.trackCounter = wx.StaticText(self, label="00:00",pos=(5,480))
                sliderSizer.Add(self.trackCounter,1, wx.ALL|wx.CENTER, 5)


                #set up playback timer
                self.playbackTimer = wx.Timer(self)
                self.Bind(wx.EVT_TIMER,self.onTimer)
                #self.timer.Start(100)



                self.slider=wx.Slider(self,pos=(0,455),size=(800,25),style = wx.SL_HORIZONTAL)
                #self.slider.SetRange(0,self.mplay.Length())
                #sliderSizer.Add(self.slider,1, wx.ALL|wx.EXPAND, 5)
                self.slider.Bind(wx.EVT_SLIDER, self.on_Seek)
                self.slider.SetPageSize(5000)
                sliderSizer.Add(self.slider,1,wx.ALL,5)
                
                
                mainSizer.Add(self.mplay,1,wx.ALL,5)
                self.mplay.GetBestSize()
                #self.SetSizer( mainSizer )

                
                self.Bind(wx.EVT_MENU,self.OnQuit,Mediafourth)
                self.Bind(wx.EVT_MENU,self.OnOpen,Mediafirst)
                self.Bind(wx.EVT_MENU,self.OnPlay,Playfirst)
                self.Bind(wx.EVT_MENU,self.OnPause,Playsecond)
                self.Bind(wx.EVT_MENU,self.OnStop,Playthird)
                self.Bind(wx.EVT_MENU,self.Onlisten,Spfirst)
                self.Bind(wx.EVT_MENU,self.Onclose,Spfirst)
                self.Bind(wx.EVT_MENU,self.SpeedChange,submenu1)
                self.Bind(wx.EVT_MENU,self.SpeedChange1,submenu2)
                self.Bind(wx.EVT_MENU,self.SpeedChange2,submenu3)
                self.Bind(wx.EVT_MENU,self.SpeedChange3,submenu4)
                self.Bind(wx.EVT_MENU,self.SpeedChange4,submenu5)
                self.Bind(wx.EVT_MENU,self.SpeedChange5,submenu6)
                self.Show()

        def SpeedChange(self,evt):
                self.mplay.SetPlaybackRate(0.25)
                self.mplay.Play()
        def SpeedChange1(self,evt):
                self.mplay.SetPlaybackRate(0.50)
                self.mplay.Play()
        def SpeedChange2(self,evt):
                self.mplay.SetPlaybackRate(1.0)
                self.mplay.Play()
        def SpeedChange3(self,evt):
                self.mplay.SetPlaybackRate(1.25)
                self.mplay.Play()
        def SpeedChange4(self,evt):
                self.mplay.SetPlaybackRate(1.50)
                self.mplay.Play()
        def SpeedChange5(self,evt):
                self.mplay.SetPlaybackRate(2.0)
                self.mplay.Play()
                
        def OnQuit(self,evt):
                self.Close()
                self.mplay.Quit()


        def OnOpen(self,evt):
                dial=wx.FileDialog(self,"Choose a Media File",os.getcwd(),"","",wx.OPEN | wx.CHANGE_DIR)
                if dial.ShowModal()== wx.ID_OK :
                        path=dial.GetPath()
                        if  self.mplay.Load(path):
                                folder, filen =os.path.split(path)
                                #self.ShowPlayerControls(flags = wx.media.MEDIACTRLPLAYERCONTROLS_STEP)   
                        
                                #print self.mplay.Length()
                                
                                self.playbackTimer.Start(100)
                                
                dial.Destroy()  
        
        def OnPlay(self,evt):
                self.mplay.Play()
                self.slider.SetRange(0,self.mplay.Length())
                self.button1.Show()
                self.button.Hide()

        def OnPause(self,evt):
                self.mplay.Pause()
                self.slider.SetRange(0,self.mplay.Length())
                self.button.Show()
                self.button1.Hide()

        def OnStop(self,evt):
                self.mplay.Stop()
                self.button.Show()
                self.button1.Hide()
        def on_set_volume(self, event):
                self.currentVolume = self.volumeCtrl.GetValue()
                self.mplay.SetVolume((self.currentVolume)*.01)
        
        def Onclose(self,evt):
                print "hi"
                evt.Skip()
        def on_pause(self, event):
        #self.mpc.Pause()
          if self.mplay.GetState()==wx.media.MEDIASTATE_PLAYING:
           self.mplay.Pause()
           self.button.Show()
           self.button1.Hide()
          else:
            self.mplay.Play()
            self.button.Hide()
            self.button1.Show()
            self.slider.SetRange(0,self.mplay.Length())

        def on_Seek(self, evt):
            offset=self.slider.GetValue()
            self.mplay.Seek(offset,0)
        def onTimer(self, evt):
            offset = self.mplay.Tell()
            self.slider.SetValue(offset)
            secsPlayed = time.strftime('%H:%M:%S', gmtime(offset*.001))
            self.trackCounter.SetLabel(secsPlayed)
        def on_forward(self,evt):
            temp=self.mplay.Tell()
            temp=temp+5000
            if temp>self.mplay.Length():
               temp=self.mplay.Length()
            self.mplay.Seek(temp,0)
        def on_backward(self,evt):
            temp=self.mplay.Tell()
            temp=temp-5000
            if temp<0:
               temp=0
            self.mplay.Seek(temp,0)
app=wx.App()
frame=Main(None,"Media Player")
app.MainLoop()
