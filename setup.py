from subprocess import call
call(['sudo','apt-get','install','python-pandas'])
call(['sudo','apt-get','install','gfortran'])
call(['sudo','apt-get','install','liblapack-dev'])
call(['sudo','apt-get','install','python-sklearn']) 
call(['sudo','easy_install','pymc'])
call(['sudo','apt-get','install','python-wxgtk2.8'])
print("Install complete. Run GUI.py from the ProductFinal package")
