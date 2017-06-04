
from collections import namedtuple

from PyQt5.QtCore import QEvent

from plover.gui_qt.add_translation_dialog_ui import Ui_AddTranslationDialog
from plover.gui_qt.add_translation_widget import AddTranslationWidget
from plover.gui_qt.i18n import get_gettext
from plover.gui_qt.tool import Tool


_ = get_gettext()


class AddTranslationDialog(Tool, Ui_AddTranslationDialog):

    ''' Add a new translation to the dictionary. '''

    TITLE = _('Add Translation')
    ICON = ':/translation_add.svg'
    ROLE = 'add_translation'
    SHORTCUT = 'Ctrl+N'

    def __init__(self, engine, dictionary_path=None):
        super(AddTranslationDialog, self).__init__(engine)
        self.setupUi(self)

        add_translation = AddTranslationWidget(engine, dictionary_path)
        self.layout().replaceWidget(self.add_translation, add_translation)
        add_translation.strokes.setFocus()
        self.add_translation = add_translation

        engine.signal_connect('config_changed', self.on_config_changed)
        self.on_config_changed(engine.config)
        self.installEventFilter(self)

        self.restore_state()
        self.finished.connect(self.save_state)

    def eventFilter(self, watched, event):
        if watched == self and event.type() == QEvent.ActivationChange:
            if not self.isActiveWindow():
                self.add_translation.unfocus()
            return False
        return False

    def on_config_changed(self, config_update):
        if 'translation_frame_opacity' in config_update:
            opacity = config_update.get('translation_frame_opacity')
            if opacity is None:
                return
            assert 0 <= opacity <= 100
            self.setWindowOpacity(opacity / 100.0)

    def accept(self):
        self.add_translation.save_entry()
        super(AddTranslationDialog, self).accept()

    def reject(self):
        self.add_translation.reject()
        super(AddTranslationDialog, self).reject()
