import wx
import analyze_struct

class ImageFrame(wx.Frame):
    def __init__(self, parent, title, result, percent_ferrite, avg_width, avg_height, path_original):
        super().__init__(parent=parent, title=title)
        self.Size = wx.Size(900, 700)
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

        percent_ferrite_label = wx.StaticText(control_panel, label=f"Процент феррита: {percent_ferrite:.2f}%")
        control_sizer.Add(percent_ferrite_label, flag=wx.TOP, border=5)

        avg_size_label = wx.StaticText(
            control_panel,
            label=f"Средняя ширина: {avg_width:.2f} px, высота: {avg_height:.2f} px"
        )
        control_sizer.Add(avg_size_label, flag=wx.TOP, border=5)

        image_panel = wx.ScrolledWindow(main_panel)
        image_panel.SetScrollbars(20, 20, 50, 50)
        image_sizer = wx.BoxSizer(wx.VERTICAL)
        image_panel.SetSizer(image_sizer)

        h, w = self.result.shape[:2]
        bitmap = wx.Bitmap.FromBuffer(w, h, self.result)
        scaled_bitmap = self.resizeImage(bitmap)  # Масштабируем изображение
        self.result_static = wx.StaticBitmap(image_panel, -1, scaled_bitmap)
        image_sizer.Add(self.result_static)

        original = wx.Image(path_original, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        scaled_original = self.resizeImage(original)  # Масштабируем оригинал
        self.original_static = wx.StaticBitmap(image_panel, -1, scaled_original)
        image_sizer.Add(self.original_static)
        self.original_static.Hide()

        main_sizer.Add(control_panel, 0, wx.EXPAND | wx.TOP | wx.LEFT, border=15)
        main_sizer.Add(image_panel, 1, wx.EXPAND | wx.LEFT | wx.TOP, border=20)

    def resizeImage(self, bitmap):
        # Размеры окна
        max_width, max_height = 700, 550

        # Текущие размеры изображения
        w, h = bitmap.GetWidth(), bitmap.GetHeight()

        # Коэффициент масштабирования
        coef_w = max_width / w
        coef_h = max_height / h
        coef = min(coef_w, coef_h)

        # Новые размеры
        new_width, new_height = int(w * coef), int(h * coef)

        # Масштабирование изображения
        scaled_image = bitmap.ConvertToImage().Rescale(new_width, new_height).ConvertToBitmap()
        return scaled_image

    def saveImage(self, event=None):
        with wx.FileDialog(self, "Сохранить изображение", wildcard="PNG и JPG файлы (*.png, *.jpg)|*.png;*.jpg",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     

            pathname = fileDialog.GetPath()

            try:
                analyze_struct.saveImage(pathname, self.result)
                self.was_saved = True
            except:
                wx.LogError(f"Не удалось сохранить файл '{pathname}'.")

    def changeImage(self, event):
        if event.GetEventObject().GetValue() == True:
            self.original_static.Show()
            self.result_static.Hide()
        else:
            self.result_static.Show()
            self.original_static.Hide()

    def onClose(self, event):
        if not self.was_saved:
            msg_save = wx.MessageDialog(
                self, 
                style=wx.YES_NO | wx.YES_DEFAULT, 
                message="Сохранить изображение перед выходом?"
            )
            answer = msg_save.ShowModal()

            if answer == wx.ID_YES:
                self.saveImage()

        self.Destroy()


if __name__ == "__main__":
    app = wx.App()
    img = analyze_struct.openImage(path='C:\\Users\\egora\\Desktop\\Micro\\SNAP-140548-0039.jpg')
    result, avg_width, avg_height = analyze_struct.runProcessing(
        image=img,
        name='SNAP-140548-0039.jpg',
        threshold_contour=1500,
        threshold_pixel=150
    )

    frame = ImageFrame(
        None,
        title="Результаты анализа",
        result=result,
        percent_ferrite=44.2,
        avg_width=avg_width,
        avg_height=avg_height,
        path_original='C:\\Users\\egora\\Desktop\\Micro\\SNAP-140548-0039.jpg'
    )
    frame.Show()

    app.MainLoop()
