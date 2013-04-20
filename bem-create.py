import sublime, sublime_plugin
import os, os.path
import datetime
import re
import webbrowser

S = sublime.load_settings("BEM.sublime-settings")



# @class Scribe Log information
class Scribe():
    def __init__(self):
        # installed_packages_path()
        if os.path.exists(os.path.join(sublime.packages_path(), "BEM")):
            logPath = os.path.join(sublime.packages_path(), "BEM")

            if not os.path.exists(os.path.join(logPath, "log")):
                create_file(logPath, "log")

        self.logFile = open(os.path.join(os.path.join(logPath, "log")), 'a')

    def log(self, line):
        self.logFile.write(datetime.datetime.now().isoformat(' ') + "  " + line + "\n")

    def stop(self):
        self.logFile.write("\n")
        self.logFile.close()



# @method create_file Create a files and log it
#
# @param String 'path' Path to file dir
# @param String 'name' File name with extantion (test.html)
# @param String 'content' Content of created file
def create_file(path, name, content=''):
    try:
        file = open(os.path.join(path, name), 'w')
        file.write(content)
        file.close()

        return "NOTICE: File '%s' was created in '%s'." % (name, path)

    except:
        sublime.status_message("Unable to create file " + name)
        
        return "FAIL: Unable to create file '%s' in '%s'." % (name, path)



# @method create_dir Create a dir and log it
#
# @param String 'path' Path to file dir
# @param String 'name' File name with extantion (test.html)
def create_dir(path, name):
    try:
        os.mkdir(os.path.join(path, name))

        return "NOTICE: Folder '%s' was created in '%s'." % (name, path)

    except:
        sublime.status_message("Unable to create file " + name)

        return "FAIL: Unable to create file '%s' in '%s'." % (block + TECH[t]['filetype'], path)



# BLOCK
# BLOCK_MOD_VAL
# BLOCK__ELEM
# BLOCK__ELEM_MOD_VAL
class BemCreateCommand(sublime_plugin.TextCommand):
    def run(self, view):
        self.Scribe = Scribe()

        self.view.window().show_input_panel("BEM Create:", "", self.get_command, None, None)

    # Generate command object
    def get_command(self, command_line):
        self.Scribe.log("NOTICE: Command '%s' was received." % command_line)

        if re.match('^[a-z0-9-]+$', command_line, flags=re.IGNORECASE):
            unit_type = 'block'

        elif re.match('^[a-z0-9-]+_[a-z0-9-]+_[a-z0-9-]+$', command_line, flags=re.IGNORECASE):
            unit_type = 'mod'

        elif re.match('^[a-z0-9-]+__[a-z0-9-]+$', command_line, flags=re.IGNORECASE):
            unit_type = 'elem'

        elif re.match('^[a-z0-9-]+__[a-z0-9-]+_[a-z0-9-]+_[a-z0-9-]+$', command_line, flags=re.IGNORECASE):
            unit_type = 'elemMod'

        else:
            unit_type = ''

        command = {
            'unit_type': '',
            'units': {}
        }

        if unit_type:
            self.Scribe.log("NOTICE: Trying to create %s." % unit_type)

            command['unit_type'] = unit_type

            # Split command_line on Block and Elem part
            units = re.findall('[^_]+[_]?(?!_)[^_]*[_]?(?!_)[^_]*', command_line, flags=re.IGNORECASE)

            blockUnit = re.findall('[^_]+', units[0], flags=re.IGNORECASE)
            command['units']['block'] = blockUnit[0]

            # MOD
            try:
                command['units']['mod'] = { blockUnit[1]: blockUnit[2] }

            except:
                pass

            # ELEM
            try:
                elemUnit = re.findall('[^_]+', units[1], flags=re.IGNORECASE)
                command['units']['elem'] = elemUnit[0]

                # ELEMMOD
                try:
                    command['units']['elemMod'] = { elemUnit[1]: elemUnit[2] }

                except:
                    pass

            except:
                pass

            self.generate_files(command)

        else:
            sublime.message_dialog("Error: Incorrect command format.\n\nLearn more at https://github.com/ahtohbi4/bem#readme")
            self.Scribe.log("FAIL: Incorrect command format. Learn more information on page https://github.com/ahtohbi4/bem#readme\n")
            self.Scribe.stop()

    # Generate files
    def generate_files(self, command):
        message = "Success!"
        error_message = ""

        BLOCKS_PATH = S.get("blocks_path")
        block = command['units']['block']
        blockPath = os.path.join(BLOCKS_PATH, block)

        TECH_FILES_CONTENT = S.get('tech_files_content')
        TECH = S.get('tech')

        # BLOCK
        if command['unit_type'] == 'block':
            if not os.path.exists(blockPath):
                self.Scribe.log(create_dir(BLOCKS_PATH, block))

                for t in TECH_FILES_CONTENT['block']:
                    content = TECH_FILES_CONTENT['block'][t].format(block = block, dep = "")
                    self.Scribe.log(create_file(blockPath, block + TECH[t]['filetype'], content))

                message = message + "\n\nBlock '%s' was created." % block
                self.Scribe.log("NOTICE: Block '%s' was created." % block)

            else:
                error_message = "Alert!\n\nBlock '%s' already exists." % block
                self.Scribe.log("FAIL: Block '%s' already exists." % block)

        # MOD
        elif command['unit_type'] == 'mod':
            mod = command['units']['mod'].keys()[0]
            value = command['units']['mod'].values()[0]

            if not os.path.exists(blockPath):
                self.Scribe.log(create_dir(BLOCKS_PATH, block))

                dep_content = TECH_FILES_CONTENT['block']['deps'].format(dep = "\n        {\n            mods: { " + mod + ": '" + value + "' }\n        }\n    ")
                self.Scribe.log(create_file(blockPath, block + TECH['deps']['filetype'], dep_content))
                self.view.window().open_file(os.path.join(blockPath, block + TECH['deps']['filetype']), sublime.TRANSIENT)

            modPath = os.path.join(blockPath, "_" + mod)

            if not os.path.exists(modPath):
                self.Scribe.log(create_dir(blockPath, "_" + mod))

                for t in TECH_FILES_CONTENT['mod']:
                    content = TECH_FILES_CONTENT['mod'][t].format(block = block, mod = mod, value = value)
                    self.Scribe.log(create_file(modPath, block + "_" + mod + "_" + value + TECH[t]['filetype'], content))

                message = message + "\n\nMod '%s' with Value '%s' for Block '%s' was created." % (mod, value, block)
                self.Scribe.log("NOTICE: Mod '%s' with Value '%s' for Block '%s' was created." % block)

            else:
                error_message = "Alert!\n\nMod '%s' for Block '%s' already exists." % (mod, block)
                self.Scribe.log("FAIL: Mod '%s' with Value '%s' for Block '%s' already exists." % (mod, value, block))

        # ELEM
        elif command['unit_type'] == 'elem':
            elem = command['units']['elem']

            if not os.path.exists(blockPath):
                self.Scribe.log(create_dir(BLOCKS_PATH, block))

                dep_content = TECH_FILES_CONTENT['block']['deps'].format(dep = "\n        { elem: '" + elem + "' }\n    ")
                self.Scribe.log(create_file(blockPath, block + TECH['deps']['filetype'], dep_content))
                self.view.window().open_file(os.path.join(blockPath, block + TECH['deps']['filetype']), sublime.TRANSIENT)

            elemPath = os.path.join(blockPath, "__" + elem)

            if not os.path.exists(elemPath):
                self.Scribe.log(create_dir(blockPath, "__" + elem))

                for t in TECH_FILES_CONTENT['elem']:
                    content = TECH_FILES_CONTENT['elem'][t].format(block = block, elem = elem)
                    self.Scribe.log(create_file(elemPath, block + "__" + elem + TECH[t]['filetype'], content))

                message = message + "\n\nElem '%s' for Block '%s' was created." % (elem, block)
                self.Scribe.log("NOTICE: Elem '%s' for Block '%s' was created." % (elem, block))

            else:
                error_message = "Alert!" + "\n\nElem '%s' for Block '%s' already exists." % (elem, block)
                self.Scribe.log("FAIL: Elem '%s' for Block '%s' already exists." % (elem, block))

        # ELEMMOD
        elif command['unit_type'] == 'elemMod':
            elem = command['units']['elem']
            elemMod = command['units']['elemMod'].keys()[0]
            value = command['units']['elemMod'].values()[0]

            if not os.path.exists(blockPath):
                self.Scribe.log(create_dir(BLOCKS_PATH, block))

                dep_content = TECH_FILES_CONTENT['block']['deps'].format(dep = "\n        {\n            elem: '" + elem + "',\n            mods: { " + elemMod + ": '" + value + "' }\n        }\n    ")
                self.Scribe.log(create_file(blockPath, block + TECH['deps']['filetype'], dep_content))
                self.view.window().open_file(os.path.join(blockPath, block + TECH['deps']['filetype']), sublime.TRANSIENT)

            elemPath = os.path.join(blockPath, "__" + elem)

            if not os.path.exists(elemPath):
                self.Scribe.log(create_dir(blockPath, "__" + elem))

            elemModPath = os.path.join(elemPath, "_" + elemMod)

            if not os.path.exists(elemModPath):
                self.Scribe.log(create_dir(elemPath, "_" + elemMod))

                for t in TECH_FILES_CONTENT['elemMod']:
                    content = TECH_FILES_CONTENT['elemMod'][t].format(block = block, elem = elem, elemMod = elemMod, value = value)
                    self.Scribe.log(create_file(elemModPath, block + "__" + elem + "_" + elemMod + "_" + value + TECH[t]['filetype'], content))

                message = message + "\n\nMod '%s' with Value '%s' for Elem '%s' in Block '%s' was created." % (elemMod, value, elem, block)
                self.Scribe.log("NOTICE: Mod '%s' with Value '%s' for Elem '%s' in Block '%s' was created." % (elemMod, value, elem, block))

            else:
                error_message = "Alert!" + "\n\nMod '%s' with Value '%s' for Elem '%s' in Block '%s' already exists." % (elemMod, value, elem, block)
                self.Scribe.log("ERROR: Mod '%s' with Value '%s' for Elem '%s' in Block '%s' already exists." % (elemMod, value, elem, block))

        # Messages and refresh dir
        if error_message != "":
            sublime.error_message(error_message)

        else:
            self.view.window().run_command("refresh_folder_list")
            sublime.message_dialog(message)

        self.Scribe.stop()



class BemHelpCommand(sublime_plugin.TextCommand):
    def run(self, view):
        webbrowser.open_new_tab('https://github.com/ahtohbi4/bem#readme')
