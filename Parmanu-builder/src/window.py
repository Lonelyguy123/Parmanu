from gi.repository import Adw, Gtk, GdkPixbuf, GLib
import os

@Gtk.Template(resource_path='/org/gnome/parmanu/window.ui')
class ParmanuBuilderWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'ParmanuBuilderWindow'

    file_conversion_button = Gtk.Template.Child()
    file_splitting_button = Gtk.Template.Child()
    file_merging_button = Gtk.Template.Child()
    file_conversion_image = Gtk.Template.Child()
    file_splitting_image = Gtk.Template.Child()
    file_merging_image = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.file_conversion_button.connect('clicked', self.on_file_conversion_clicked)
        self.file_splitting_button.connect('clicked', self.on_file_splitting_clicked)
        self.file_merging_button.connect('clicked', self.on_file_merging_clicked)

        self.load_images()

    def load_images(self):
        # Replace these paths with the actual paths to your images
        conversion_image_path = '/home/shastha-orb/Desktop/parmanu-git/Parmanu/Parmanu-builder/src/Images/file conversion.png'
        splitting_image_path = '/home/shastha-orb/Desktop/parmanu-git/Parmanu/Parmanu-builder/src/Images/file splitting.png'
        merging_image_path = '/home/shastha-orb/Desktop/parmanu-git/Parmanu/Parmanu-builder/src/Images/file merging.png'

        self.file_conversion_image.set_filename(conversion_image_path)
        self.file_splitting_image.set_filename(splitting_image_path)
        self.file_merging_image.set_filename(merging_image_path)

    def on_file_conversion_clicked(self, button):
        print("File conversion clicked")
        # Add your file conversion logic here

    def on_file_splitting_clicked(self, button):
        print("File splitting clicked")
        # Add your file splitting logic here

    def on_file_merging_clicked(self, button):
        print("File merging clicked")
        # Add your file merging logic here
