# Making executable/MSI installer

## Tested with environment:
 * Windows 2008 (Not checked with other versions)
 * Python 2.7.9 (There's specific problems with other versions)
 * boto==2.34.0 (There's auth problems on higher versions)
 * cx_Freeze==4.3.3 (Critical bug in 4.3.4)
 * pywin32

## Building:

`python setup.py build`

`robocopy /S /E "C:/Python27/Lib/site-packages/boto" "./build/exe.win32-2.7/boto"`

`python setup.py bdist_msi --add-to-path yes`
