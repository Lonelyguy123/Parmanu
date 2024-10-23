from gi.repository import Adw, Gtk, GLib
import os

@Gtk.Template(resource_path='/org/gnome/parmanu/window.ui')
class ParmanuBuilderWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'ParmanuBuilderWindow'

    # Template Children - matching the IDs from window.ui
    main_stack = Gtk.Template.Child()
    file_conversion_button = Gtk.Template.Child()
    file_splitting_button = Gtk.Template.Child()
    file_merging_button = Gtk.Template.Child()
    back_to_main_conversion = Gtk.Template.Child()
    back_to_main_splitting = Gtk.Template.Child()
    back_to_main_merging = Gtk.Template.Child()

    # Additional template children for images
    file_conversion_image = Gtk.Template.Child()
    file_splitting_image = Gtk.Template.Child()
    file_merging_image = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Connect signals for main action buttons
        self.file_conversion_button.connect('clicked', self.on_file_conversion_clicked)
        self.file_splitting_button.connect('clicked', self.on_file_splitting_clicked)
        self.file_merging_button.connect('clicked', self.on_file_merging_clicked)

        # Connect signals for back buttons
        self.back_to_main_conversion.connect('clicked', self.on_back_clicked)
        self.back_to_main_splitting.connect('clicked', self.on_back_clicked)
        self.back_to_main_merging.connect('clicked', self.on_back_clicked)

        # Load images
        try:
            self.load_images()
        except Exception as e:
            print(f"Failed to load images: {e}")

    def load_images(self):
        """Load images for the main menu buttons"""
        # Using the direct path approach
        conversion_image_path = '/home/shastha-orb/Desktop/parmanu-git/Parmanu/Parmanu-builder/src/Images/file conversion.png'
        splitting_image_path = '/home/shastha-orb/Desktop/parmanu-git/Parmanu/Parmanu-builder/src/Images/file splitting.png'
        merging_image_path = '/home/shastha-orb/Desktop/parmanu-git/Parmanu/Parmanu-builder/src/Images/file merging.png'

        self.file_conversion_image.set_filename(conversion_image_path)
        self.file_splitting_image.set_filename(splitting_image_path)
        self.file_merging_image.set_filename(merging_image_path)

    def on_file_conversion_clicked(self, button):
        """Handle file conversion button click"""
        self.main_stack.set_visible_child_name('file_conversion')

    def on_file_splitting_clicked(self, button):
        """Handle file splitting button click"""
        self.main_stack.set_visible_child_name('file_splitting')

    def on_file_merging_clicked(self, button):
        """Handle file merging button click"""
        self.main_stack.set_visible_child_name('file_merging')

    def on_back_clicked(self, button):
        """Handle back button clicks"""
        self.main_stack.set_visible_child_name('main_menu')

    def show_file_chooser(self, title="Select File", callback=None):
        """Generic file chooser dialog"""
        dialog = Gtk.FileChooserDialog(
            title=title,
            parent=self,
            action=Gtk.FileChooserAction.OPEN
        )

        dialog.add_buttons(
            "_Cancel", Gtk.ResponseType.CANCEL,
            "_Open", Gtk.ResponseType.ACCEPT
        )

        dialog.connect("response", self._handle_file_response, callback)
        dialog.show()

    def _handle_file_response(self, dialog, response, callback):
        """Handle file chooser dialog response"""
        try:
            if response == Gtk.ResponseType.ACCEPT:
                file = dialog.get_file()
                if file:
                    file_path = file.get_path()
                    if callback:
                        callback(file_path)
                    else:
                        print(f"Selected file: {file_path}")
        except Exception as e:
            print(f"Error handling file selection: {e}")
        finally:
            dialog.destroy()
