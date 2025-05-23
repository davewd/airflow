# sample ipython_config.py
c = get_config()

c.TerminalIPythonApp.display_banner = True
c.InteractiveShellApp.log_level = 20
c.InteractiveShellApp.extensions = [
    'autoreload',
    'ipython_genutils',
    'IPython.extensions.autoreload',
]
c.IPKernelApp.exec_lines = [
    'import os; os.chdir("/app/source")'
]
c.InteractiveShellApp.exec_lines = [
    'import os; os.chdir("/app/source")'
]
c.InteractiveShellApp.exec_files = [
    '/app/source/micap_runtime/sitecustomize.py',
]

c.IPKernelApp.exec_files = [
    '/app/source/micap_runtime/sitecustomize.py',
]
c.InteractiveShell.autoindent = True
c.InteractiveShell.colors = 'LightBG'
c.InteractiveShell.confirm_exit = False
c.InteractiveShell.deep_reload = True
c.InteractiveShell.editor = 'nano'
c.InteractiveShell.xmode = 'Context'

c.PromptManager.in_template  = 'In [\\#]: '
c.PromptManager.in2_template = '   .\\D.: '
c.PromptManager.out_template = 'Out[\\#]: '
c.PromptManager.justify = True

c.PrefilterManager.multi_line_specials = True

c.AliasManager.user_aliases = [
 ('la', 'ls -al')
]