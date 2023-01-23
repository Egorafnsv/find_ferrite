import wx
import analyze_struct
from ImageFrame import ImageFrame

class mainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.path_to_file = ""
        self.name_file = ""
        
        panel = wx.Panel(self)
        main_box = wx.BoxSizer(wx.HORIZONTAL)
        panel.SetSizer(main_box)
        
        left_box = wx.BoxSizer(wx.VERTICAL)

        self.selected_image = wx.StaticText(panel, label="Файл не выбран")
        btn_select_image = wx.Button(panel, label='Выбрать изображение...')
        self.Bind(wx.EVT_BUTTON, self.openImage, btn_select_image)
        left_box.Add(btn_select_image, wx.ID_ANY, wx.ALIGN_TOP)
        left_box.Add(self.selected_image, wx.ID_ANY)

        main_box.Add(left_box, flag=wx.EXPAND)

        sep = wx.StaticLine(panel, style=wx.LI_VERTICAL)
        main_box.Add(sep, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        
        
        right_box = wx.BoxSizer(wx.VERTICAL)


        self.threshold_pixel = wx.Slider(panel, value=150, minValue=0, maxValue=255)
        self.label_threshold_pixel = wx.StaticText(panel, label="150")
        self.Bind(wx.EVT_COMMAND_SCROLL, self.changePixelLabel, self.threshold_pixel)

        self.threshold_contour = wx.SpinCtrl(panel, value='1500', min=0, max=50000)

        run_button = wx.Button(panel, label='Run')
        self.Bind(wx.EVT_BUTTON, self.runProcessingImage, run_button)
        right_box.AddMany([(self.threshold_pixel, 1, wx.EXPAND|wx.TOP, 10), 
            (self.threshold_contour, 2, wx.EXPAND|wx.TOP, 10),
            (self.label_threshold_pixel, 4, wx.TOP, 10),
            (run_button, 3, wx.EXPAND | wx.TOP, 10)])
       
                
                
        main_box.Add(right_box, wx.ID_ANY)



    def openImage(self, event):
        with wx.FileDialog(parent=self, message="Выберите изображение", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST, 
        wildcard="PNG and JPG files (*.png, *,jpg)|*.png;*.jpg") as fileDialog:
           
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            else:
                self.path_to_file = fileDialog.GetPath()
                self.name_file = fileDialog.GetFilename()
                self.selected_image.SetLabel(self.path_to_file)
    
            
    def runProcessingImage(self, event):
        img = analyze_struct.openImage(path=self.path_to_file)
        self.result = analyze_struct.runProcessing(image=img, name=self.name_file, 
                                              threshold_contour=self.threshold_contour.GetValue(), threshold_pixel=self.threshold_pixel.GetValue())
        
        
        myframetest = ImageFrame(self, "test", self.result, self.path_to_file)
        myframetest.Show()  
    

    def changePixelLabel(self, event):
        self.label_threshold_pixel.SetLabel(f"{self.threshold_pixel.GetValue()}")


app = wx.App()

frame = mainFrame(None, title="Hello world!!!")
frame.Show()

app.MainLoop()