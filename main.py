import wx
import analyze_struct
from ImageFrame import ImageFrame

class mainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.Size = wx.Size(500, 300)
        self.Center()

        self.path_to_file = ""
        self.name_file = ""
        
        panel = wx.Panel(self)
        main_box = wx.BoxSizer(wx.HORIZONTAL)
        panel.SetSizer(main_box)
        
        left_box = wx.BoxSizer(wx.VERTICAL)

        btn_select_image = wx.Button(panel, label='Выбрать изображение...', size=wx.Size(150, 50))
        self.Bind(wx.EVT_BUTTON, self.openImage, btn_select_image)

        btn_sel_img_sizer = wx.BoxSizer(wx.VERTICAL)
        btn_sel_img_sizer.Add(btn_select_image, flag=wx.TOP, border=20)
        left_box.Add(btn_sel_img_sizer, flag=wx.LEFT | wx.BOTTOM, border=10)

        self.selected_image_label = wx.StaticText(panel, label="Файл не выбран", size=wx.Size(200, 30))
        left_box.Add(self.selected_image_label, flag=wx.TOP | wx.LEFT, border=10)

        main_box.Add(left_box, flag=wx.EXPAND)

        sep = wx.StaticLine(panel, style=wx.LI_VERTICAL)
        main_box.Add(sep, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        right_box = wx.BoxSizer(wx.VERTICAL)

        threshold_pixel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.threshold_pixel = wx.Slider(panel, value=150, minValue=0, maxValue=255, size=wx.Size(250, 20))
        self.Bind(wx.EVT_COMMAND_SCROLL, self.changePixelLabel, self.threshold_pixel)
        self.threshold_pixel_label = wx.StaticText(panel, label="150")

        threshold_pixel_sizer.Add(self.threshold_pixel_label, flag=wx.TOP | wx.RIGHT, border=5)
        threshold_pixel_sizer.Add(self.threshold_pixel)

        self.threshold_contour = wx.SpinCtrl(panel, value='1500', min=0, max=50000, size=wx.Size(150, 20))

        run_button = wx.Button(panel, label='Run', size=wx.Size(150, 40))
        self.Bind(wx.EVT_BUTTON, self.runProcessingImage, run_button)

        right_box.Add(threshold_pixel_sizer, flag=wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, border=15)
        right_box.Add(self.threshold_contour, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, border=10)
        right_box.Add(run_button, flag=wx.EXPAND | wx.ALL, border=10)

        main_box.Add(right_box, wx.ID_ANY)

    def openImage(self, event):
        with wx.FileDialog(parent=self, message="Выберите изображение", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST, 
        wildcard="PNG и JPG файлы (*.png, *.jpg)|*.png;*.jpg") as fileDialog:
           
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            else:
                self.path_to_file = fileDialog.GetPath()
                self.name_file = fileDialog.GetFilename()
                self.selected_image_label.SetLabel(self.name_file)

    def runProcessingImage(self, event):
        if not self.path_to_file:
            wx.MessageBox("Пожалуйста, выберите изображение.", "Ошибка", wx.OK | wx.ICON_ERROR)
            return

        img = analyze_struct.openImage(path=self.path_to_file)
        result, avg_width, avg_height = analyze_struct.runProcessing(
            image=img,
            name=self.name_file,
            threshold_contour=self.threshold_contour.GetValue(),
            threshold_pixel=self.threshold_pixel.GetValue()
        )
        percent_ferrite = analyze_struct.get_percentage_ferrite(result)

        resultFrame = ImageFrame(
            self,
            self.name_file,
            result,
            percent_ferrite,
            avg_width,
            avg_height,
            self.path_to_file
        )
        resultFrame.Show()

    def changePixelLabel(self, event):
        self.threshold_pixel_label.SetLabel(f"{self.threshold_pixel.GetValue()}")


if __name__ == "__main__":
    app = wx.App()

    frame = mainFrame(None, title="Find Ferrite")
    frame.Show()

    app.MainLoop()
