"""
Simple Object Reader 2 (SOR2)
"""
import sys

from SOR2Lib import SO

class SOR2:

  _args: list[str]


  def __init__(self, *args) -> None:
    self._args = list[str](args)


  def main(self) -> None:
    """
    Hello, World!
    """
    if len(self._args) != 3: raise IndexError('Wrong argument amount for SOR2. (Needed 3 arguments in command line: '
                                              'python3 (SOR2.py path) <file to be read> <operation (try print)>)')

    mySO: SO = SO()
    #try:
    mySO.getfrom_str(open(self._args[1], 'r').read())
    #except:
    #  raise FileNotFoundError(f'Error attempting to read file \"{self._args[1]}\". (It may be a syntax error.)')

    print(f'SOR: Read file \"{self._args[1]}\".\nExecuting: \"{self._args[2]}\".')

    if self._args[2] == 'print':
      print(mySO.get_data())
    elif self._args[2] == 'print-json':
      print(mySO.get_json(indent=2))
    elif self._args[2] == 'print-filecontent':
      print(open(self._args[1], 'r').read())
    else:
      raise NotImplementedError(f'{self._args[2]} is not a SOR2 operation.')



if __name__ == '__main__':
    SOR2(*sys.argv).main()
