import wx
import analyze_struct

class ImageFrame(wx.Frame):
    def __init__(self, parent, title, result, percent_ferrite, path_original):
        super().__init__(parent=parent, title=title)
        self.Size = wx.Size(900, 650)
        self.Center()


        self.result = result
        self.was_saved = False

        self.Bind(wx.EVT_CLOSE, self.onClose, self)

        main_panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_panel.SetSizer(main_sizer)

        control_panel = wx.Panel(main_panel)
        control_sizer = wx.BoxSizer()
        control_panel.SetSizer(control_sizer)

        save_btn = wx.Button(control_panel, label='Сохранить...')
        self.Bind(wx.EVT_BUTTON, self.saveImage, save_btn)
        control_sizer.Add(save_btn, flag=wx.LEFT, border=20)

        change_image = wx.ToggleButton(control_panel, label="Original Image")
        control_panel.Bind(wx.EVT_TOGGLEBUTTON, self.changeImage)
        control_sizer.Add(change_image, flag=wx.LEFT | wx.RIGHT, border=20)

        percent_ferrite_label = wx.StaticText(control_panel, label=f"Процент: %4.2f%%" % (percent_ferrite))
        control_sizer.Add(percent_ferrite_label, flag=wx.TOP, border=5)

        image_panel = wx.ScrolledWindow(main_panel)
        image_panel.SetScrollbars(20, 20, 50, 50)
        image_sizer = wx.BoxSizer(wx.VERTICAL)
        image_panel.SetSizer(image_sizer)

        h, w = self.result.shape[:2]
        bitmap = wx.Bitmap.FromBuffer(w, h, self.result)
        self.resizeImage(bitmap)
        self.result_static = wx.StaticBitmap(image_panel, -1, bitmap)
        image_sizer.Add(self.result_static)

        original = wx.Image(path_original, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.resizeImage(original)
        self.original_static = wx.StaticBitmap(image_panel, -1, original)
        image_sizer.Add(self.original_static)
        self.original_static.Hide()

        main_sizer.Add(control_panel, 0, wx.EXPAND | wx.TOP | wx.LEFT, border=15)
        main_sizer.Add(image_panel, 1, wx.EXPAND | wx.LEFT | wx.TOP, border=20)


    def resizeImage(self, bitmap):
        w, h = bitmap.GetSize()

        if w > 700 and h > 550:
            coef_w = 700/w
            coef_h = 550/h
            coef = coef_h if coef_h > coef_w else coef_w
            wx.Bitmap.Rescale(bitmap, wx.Size(int(w*coef), int(h*coef)))
        

    def saveImage(self, event=None):
        with wx.FileDialog(self, "Save image", wildcard="PNG and JPG files (*.png, *,jpg)|*.png;*.jpg",
                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     

            pathname = fileDialog.GetPath()

            try:
                analyze_struct.saveImage(pathname, self.result)
                self.was_saved = True
            except:
                wx.LogError("Cannot save current data in file '%s'." % pathname)
    
    def changeImage(self, event):
        if event.GetEventObject().GetValue() == True:
            self.original_static.Show()
            self.result_static.Hide()
        else:
            self.result_static.Show()
            self.original_static.Hide()

    def onClose(self, event):
        if not self.was_saved:
            msg_save = wx.MessageDialog(self, style=wx.YES_NO | wx.YES_DEFAULT, message="Сохранить изображение перед выходом?")
            answer = msg_save.ShowModal()

            if answer == wx.ID_YES:
                self.saveImage()
            
            self.Destroy()


            


if __name__ == "__main__":
    app = wx.App()
    img = analyze_struct.openImage(path='C:\\Users\\egora\\Desktop\\Micro\\SNAP-140548-0039.jpg')
    result = analyze_struct.runProcessing(image=img, name='SNAP-140548-0039.jpg', 
                                              threshold_contour=1500, threshold_pixel=150)
    
    frame = ImageFrame(None, title="Result", result=result, percent_ferrite=44.2, path_original='C:\\Users\\egora\\Desktop\\Micro\\SNAP-140548-0039.jpg')
    frame.Show()

    app.MainLoop()