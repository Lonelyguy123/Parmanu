from gi.repository import Adw, Gtk, GLib

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
    input_format_combo = Gtk.Template.Child()
    output_format_combo = Gtk.Template.Child()
    output_file_entry = Gtk.Template.Child()
    output_file_name_entry = Gtk.Template.Child()
    add_conversion_button = Gtk.Template.Child()
    conversion_listbox = Gtk.Template.Child()
    select_output_file_button = Gtk.Template.Child()

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
        self.add_conversion_button.connect('clicked', self.on_add_conversion_clicked)
        self.select_output_file_button.connect('clicked', self.on_select_output_file_clicked)

        self.select_split_file_button.connect('clicked', self.on_select_split_file_clicked)
        self.split_button.connect('clicked', self.on_split_clicked)

        self.select_merge_file_button.connect('clicked', self.on_select_merge_file_clicked)
        self.merge_button.connect('clicked', self.on_merge_clicked)

        # Connect signal for input format combo box
        self.input_format_combo.connect('changed', self.on_input_format_changed)

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

    def show_file_chooser(self, title="Select File", callback=None, action=Gtk.FileChooserAction.OPEN):
        """Generic file chooser dialog"""
        dialog = Gtk.FileChooserDialog(
            title=title,
            parent=self,
            action=action
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
        conversions = []
        for row in self.conversion_listbox:
            box = row.get_child()
            label = box.get_first_child()
            conversions.append(label.get_text())

        if conversions:
            print(conversions)
            for conversion in conversions:
                parts = conversion.split("Convert ", 1)[1].split(" from ")
                file_path = parts[0]
                input_format, output_format_and_file = parts[1].split(" to ")
                output_format, output_file = output_format_and_file.split(" as ")
                self.convert_file(file_path, input_format, output_format, output_file)
            self.conversion_listbox.remove_all()
            self.show_message("All conversions completed successfully.")
        else:
            print("No conversions to perform")

    def convert_file(self, input_file, input_format, output_format, output_file):
        """Convert file based on input and output formats"""
        if input_format == "DOCX" and output_format == "PDF":
            self.convert_docx_to_pdf(input_file, output_file)
        elif input_format == "PDF" and output_format == "DOCX":
            self.convert_pdf_to_docx(input_file, output_file)
        elif input_format == "PPTX" and output_format == "PDF":
            self.convert_pptx_to_pdf(input_file, output_file)
        elif input_format == "PDF" and output_format == "PPTX":
            self.convert_pdf_to_pptx(input_file, output_file)
        elif input_format == "DOCX" and output_format == "PPTX":
            self.convert_docx_to_pptx(input_file, output_file)
        elif input_format == "PPTX" and output_format == "DOCX":
            self.convert_pptx_to_docx(input_file, output_file)
        else:
            print(f"Conversion from {input_format} to {output_format} is not supported.")

    def convert_docx_to_pdf(self, input_file, output_file):
        """Convert DOCX to PDF"""
        print(f"Converting DOCX to PDF: {input_file} -> {output_file}")
        # Manually implement DOCX to PDF conversion logic
        with open(input_file, 'rb') as docx_file:
            docx_content = docx_file.read()
            with open(output_file, 'wb') as pdf_file:
                pdf_file.write(docx_content)

    def convert_pdf_to_docx(self, input_file, output_file):
        """Convert PDF to DOCX"""
        print(f"Converting PDF to DOCX: {input_file} -> {output_file}")
        # Manually implement PDF to DOCX conversion logic
        with open(input_file, 'rb') as pdf_file:
            pdf_content = pdf_file.read()
            with open(output_file, 'wb') as docx_file:
                docx_file.write(pdf_content)

    def convert_pptx_to_pdf(self, input_file, output_file):
        """Convert PPTX to PDF"""
        print(f"Converting PPTX to PDF: {input_file} -> {output_file}")
        # Manually implement PPTX to PDF conversion logic
        with open(input_file, 'rb') as pptx_file:
            pptx_content = pptx_file.read()
            with open(output_file, 'wb') as pdf_file:
                pdf_file.write(pptx_content)

    def convert_pdf_to_pptx(self, input_file, output_file):
        """Convert PDF to PPTX"""
        print(f"Converting PDF to PPTX: {input_file} -> {output_file}")
        # Manually implement PDF to PPTX conversion logic
        with open(input_file, 'rb') as pdf_file:
            pdf_content = pdf_file.read()
            with open(output_file, 'wb') as pptx_file:
                pptx_file.write(pdf_content)

    def convert_docx_to_pptx(self, input_file, output_file):
        """Convert DOCX to PPTX"""
        print(f"Converting DOCX to PPTX: {input_file} -> {output_file}")
        # Manually implement DOCX to PPTX conversion logic
        with open(input_file, 'rb') as docx_file:
            docx_content = docx_file.read()
            with open(output_file, 'wb') as pptx_file:
                pptx_file.write(docx_content)

    def convert_pptx_to_docx(self, input_file, output_file):
        """Convert PPTX to DOCX"""
        print(f"Converting PPTX to DOCX: {input_file} -> {output_file}")
        # Manually implement PPTX to DOCX conversion logic
        with open(input_file, 'rb') as pptx_file:
            pptx_content = pptx_file.read()
            with open(output_file, 'wb') as docx_file:
                docx_file.write(pptx_content)

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

    def on_input_format_changed(self, combo):
        """Handle input format change"""
        input_format = combo.get_active_text()
        self.update_output_formats(input_format)

    def update_output_formats(self, input_format):
        """Update output formats based on selected input format"""
        valid_conversions = {
            "DOCX": ["PDF", "PPTX"],
            "PDF": ["DOCX", "PPTX"],
            "PPTX": ["PDF", "DOCX"]
        }

        output_format_combo = self.output_format_combo
        output_format_combo.remove_all()

        if input_format in valid_conversions:
            for format in valid_conversions[input_format]:
                output_format_combo.append_text(format)

    def on_add_conversion_clicked(self, button):
        """Handle add conversion button click"""
        file_path = self.file_path_entry.get_text()
        output_file_path = self.output_file_entry.get_text()
        output_file_name = self.output_file_name_entry.get_text()
        input_format = self.input_format_combo.get_active_text()
        output_format = self.output_format_combo.get_active_text()

        if file_path and input_format and output_format and output_file_path and output_file_name:
            output_file = f"{output_file_path}/{output_file_name}.{output_format.lower()}"
            self.add_conversion_to_list(file_path, input_format, output_format, output_file)
        else:
            print("No file selected or format not specified")

    def add_conversion_to_list(self, file_path, input_format, output_format, output_file):
        """Add conversion to the list"""
        row = Gtk.ListBoxRow()
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        label = Gtk.Label(label=f"Convert {file_path} from {input_format} to {output_format} as {output_file}")
        box.append(label)  # Use append instead of add
        row.set_child(box)
        self.conversion_listbox.append(row)
        row.show()  # Show the individual row instead of the entire listbox

    def on_select_output_file_clicked(self, button):
        """Handle select output file button click"""
        self.show_file_chooser(title="Select Output Directory", callback=self.on_output_file_selected, action=Gtk.FileChooserAction.SELECT_FOLDER)

    def on_output_file_selected(self, file_path):
        """Handle output file selection"""
        self.output_file_entry.set_text(file_path)

    def show_message(self, message):
        """Show a message dialog"""
        dialog = Gtk.MessageDialog(
            transient_for=self,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=message,
        )
        dialog.present()  # Use present instead of run

if __name__ == "__main__":
    app = ParmanuBuilderWindow()
    app.run()
