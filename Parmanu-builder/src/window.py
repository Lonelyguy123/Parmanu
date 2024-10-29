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

    # New template children for file conversion, splitting, and merging
    select_file_button = Gtk.Template.Child()
    file_path_entry = Gtk.Template.Child()
    convert_button = Gtk.Template.Child()

    select_split_file_button = Gtk.Template.Child()
    split_file_path_entry = Gtk.Template.Child()
    split_button = Gtk.Template.Child()

    select_merge_file_button = Gtk.Template.Child()
    merge_file_path_entry = Gtk.Template.Child()
    merge_button = Gtk.Template.Child()

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

        # Connect signals for new widgets
        self.select_file_button.connect('clicked', self.on_select_file_clicked)
        self.convert_button.connect('clicked', self.on_convert_clicked)

        self.select_split_file_button.connect('clicked', self.on_select_split_file_clicked)
        self.split_button.connect('clicked', self.on_split_clicked)

        self.select_merge_file_button.connect('clicked', self.on_select_merge_file_clicked)
        self.merge_button.connect('clicked', self.on_merge_clicked)

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

    def on_select_file_clicked(self, button):
        """Handle select file button click"""
        self.show_file_chooser(title="Select File for Conversion", callback=self.on_file_selected)

    def on_file_selected(self, file_path):
        """Handle file selection"""
        self.file_path_entry.set_text(file_path)

    def on_convert_clicked(self, button):
        """Handle convert button click"""
        file_path = self.file_path_entry.get_text()
        if file_path:
            print(f"Converting file: {file_path}")
            # Add your file conversion logic here
        else:
            print("No file selected")

    def on_select_split_file_clicked(self, button):
        """Handle select split file button click"""
        self.show_file_chooser(title="Select File for Splitting", callback=self.on_split_file_selected)

    def on_split_file_selected(self, file_path):
        """Handle split file selection"""
        self.split_file_path_entry.set_text(file_path)

    def on_split_clicked(self, button):
        """Handle split button click"""
        file_path = self.split_file_path_entry.get_text()
        if file_path:
            print(f"Splitting file: {file_path}")
            # Add your file splitting logic here
        else:
            print("No file selected")

    def on_select_merge_file_clicked(self, button):
        """Handle select merge file button click"""
        self.show_file_chooser(title="Select File for Merging", callback=self.on_merge_file_selected)

    def on_merge_file_selected(self, file_path):
        """Handle merge file selection"""
        self.merge_file_path_entry.set_text(file_path)

    def on_merge_clicked(self, button):
        """Handle merge button click"""
        file_path = self.merge_file_path_entry.get_text()
        if file_path:
            print(f"Merging file: {file_path}")
            # Add your file merging logic here
        else:
            print("No file selected")
