from subprocess import call
call(['sudo','apt-get','install','python-pandas'])
call(['sudo','apt-get','install','gfortran'])
call(['sudo','easy_install','pymc'])
call(['sudo','apt-get','install','python-wxgtk2.8'])
print("Install complete. Run GUI.py from the ProductFinal package")
