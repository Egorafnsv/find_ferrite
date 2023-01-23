import wx
import analyze_struct

class ImageFrame(wx.Frame):
    def __init__(self, parent, title, result, path_original):
        super().__init__(parent=parent, title=title)
        self.result = result

        main_panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_panel.SetSizer(main_sizer)

        control_panel = wx.Panel(main_panel)
        control_sizer = wx.BoxSizer()
        control_panel.SetSizer(control_sizer)

        save_btn = wx.Button(control_panel, label='Сохранить...')
        self.Bind(wx.EVT_BUTTON, self.saveImage, save_btn)
        control_sizer.Add(save_btn, flag=wx.LEFT, border=20)

        original_image_radio = wx.RadioButton(control_panel, id=wx.ID_ANY, label='Original Image', name='show_original')
        processed_image_radio = wx.RadioButton(control_panel, id=wx.ID_ANY, label='Processed Image', name='show_processed')
        processed_image_radio.SetValue(True)
        
        control_panel.Bind(wx.EVT_RADIOBUTTON, self.changeImage)


        control_sizer.Add(original_image_radio, flag=wx.LEFT | wx.TOP, border=5)
        control_sizer.Add(processed_image_radio, flag=wx.LEFT | wx.TOP, border=5)

        image_panel = wx.ScrolledWindow(main_panel)
        image_panel.SetScrollbars(20, 20, 50, 50)
        image_sizer = wx.BoxSizer(wx.VERTICAL)
        image_panel.SetSizer(image_sizer)

        h, w = self.result.shape[:2]
        bitmap = wx.Bitmap.FromBuffer(w, h, self.result)
        self.result_static = wx.StaticBitmap(image_panel, -1, bitmap)
        image_sizer.Add(self.result_static)

        original = wx.Image(path_original, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.original_static = wx.StaticBitmap(image_panel, -1, original)
        image_sizer.Add(self.original_static)
        self.original_static.Hide()

        main_sizer.Add(control_panel, 0, wx.EXPAND | wx.ALL, border=10)
        main_sizer.Add(image_panel, 1, wx.EXPAND | wx.ALL, border=10)



    def makeStaticBitmap(self, image):
        
        # image = bitmap.ConvertToImage()
        # image = image.Scale(w//2, h//2, wx.IMAGE_QUALITY_HIGH)
        # image = wx.Bitmap(image)
        return bitmap

    def saveImage(self, event):
        with wx.FileDialog(self, "Save image", wildcard="PNG and JPG files (*.png, *,jpg)|*.png;*.jpg",
                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     

            pathname = fileDialog.GetPath()
            # try:
            analyze_struct.saveImage(pathname, self.result)
            # except:
                # wx.LogError("Cannot save current data in file '%s'." % pathname)
    
    def changeImage(self, event):
        if event.GetEventObject().GetName() == "show_original":
            self.original_static.Show()
            self.result_static.Hide()
        else:
            self.result_static.Show()
            self.original_static.Hide()
            




if __name__ == "__main__":
    app = wx.App()
    img = analyze_struct.openImage(path='C:\\Users\\egora\\Desktop\\Micro\\SNAP-140548-0039.jpg')
    result = analyze_struct.runProcessing(image=img, name='SNAP-140548-0039.jpg', 
                                              threshold_contour=1500, threshold_pixel=150)
    
    frame = ImageFrame(None, title="Result", result=result, path_original='C:\\Users\\egora\\Desktop\\Micro\\SNAP-140548-0039.jpg')
    frame.Show()

    app.MainLoop()